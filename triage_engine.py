"""
TRIAGE-AI Clinical Decision Engine
====================================
Rule-based triage engine that analyses symptoms and vital signs to produce
an urgency category (1-5), possible differential diagnoses, red-flag
warnings, and human-readable clinical reasoning.
"""

from config import (
    ALL_SYMPTOMS,
    VITAL_SIGN_RANGES,
    RED_FLAG_COMBINATIONS,
    DIAGNOSIS_RULES,
    TRIAGE_CATEGORIES,
)


class TriageEngine:
    """
    Core clinical decision-support engine.

    Usage
    -----
    >>> engine = TriageEngine()
    >>> result = engine.assess(
    ...     symptoms=["Chest pain", "Shortness of breath"],
    ...     vital_signs={"heart_rate": 130, "spo2": 88, ...},
    ...     pain_level=8,
    ...     consciousness="Alert and oriented",
    ...     age=65,
    ... )
    >>> result["triage_category"]   # 1
    >>> result["reasoning"]         # human-readable explanation
    """

    # ── public entry point ─────────────────────────────────────
    def assess(
        self,
        symptoms: list[str],
        vital_signs: dict,
        pain_level: int = 0,
        consciousness: str = "Alert and oriented",
        age: int = 40,
        chief_complaint: str = "",
    ) -> dict:
        """
        Run a full triage assessment and return a result dict containing:
          - triage_category (int 1-5)
          - urgency_score (float 0-100)
          - possible_diagnoses (list of dicts)
          - red_flags_found (list of strings)
          - reasoning (str)
          - vital_sign_alerts (list of strings)
        """
        # Step 1: Analyse vital signs
        vital_analysis = self._analyse_vitals(vital_signs, age)

        # Step 2: Analyse symptoms
        symptom_analysis = self._analyse_symptoms(symptoms)

        # Step 3: Detect red-flag combinations
        red_flags = self._detect_red_flags(symptoms, vital_signs)

        # Step 4: Analyse consciousness level
        consciousness_score = self._score_consciousness(consciousness)

        # Step 5: Factor in pain level
        pain_score = self._score_pain(pain_level)

        # Step 6: Calculate combined urgency
        urgency_score, triage_category = self._calculate_urgency(
            vital_score=vital_analysis["score"],
            symptom_score=symptom_analysis["score"],
            red_flag_count=len(red_flags),
            consciousness_score=consciousness_score,
            pain_score=pain_score,
        )

        # Step 7: Check if red-flag patterns force an escalation
        for flag in red_flags:
            if flag.get("escalate_to") and flag["escalate_to"] < triage_category:
                triage_category = flag["escalate_to"]

        # Step 8: Generate differential diagnoses
        diagnoses = self._generate_diagnoses(symptoms, vital_signs)

        # Step 9: Build reasoning narrative
        reasoning = self._build_reasoning(
            triage_category,
            vital_analysis,
            symptom_analysis,
            red_flags,
            diagnoses,
            consciousness,
            pain_level,
        )

        return {
            "triage_category": triage_category,
            "urgency_score": round(urgency_score, 1),
            "possible_diagnoses": diagnoses,
            "red_flags_found": [f["name"] for f in red_flags],
            "vital_sign_alerts": vital_analysis["alerts"],
            "reasoning": reasoning,
        }

    # ── vital-sign analysis ────────────────────────────────────
    def _analyse_vitals(self, vitals: dict, age: int) -> dict:
        """Score vital signs and generate alerts."""
        alerts: list[str] = []
        score = 0.0  # higher = more abnormal (0-40 range)

        for key, value in vitals.items():
            if key not in VITAL_SIGN_RANGES or value is None:
                continue

            ref = VITAL_SIGN_RANGES[key]
            label = ref["label"]

            # Critical ranges
            if key == "spo2":
                if value < ref["critical_low"]:
                    alerts.append(f"⚠️ CRITICAL: {label} = {value}{ref['unit']} (dangerously low)")
                    score += 10
                elif value < ref["normal_low"]:
                    alerts.append(f"⚠️ LOW: {label} = {value}{ref['unit']}")
                    score += 5
            elif key == "gcs":
                if value <= ref["critical_low"]:
                    alerts.append(f"⚠️ CRITICAL: {label} = {value} (severe impairment)")
                    score += 10
                elif value < ref["normal_low"]:
                    alerts.append(f"⚠️ REDUCED: {label} = {value}")
                    score += 6
            else:
                if value <= ref["critical_low"]:
                    alerts.append(f"⚠️ CRITICAL LOW: {label} = {value}{ref['unit']}")
                    score += 10
                elif value >= ref["critical_high"]:
                    alerts.append(f"⚠️ CRITICAL HIGH: {label} = {value}{ref['unit']}")
                    score += 10
                elif value < ref["normal_low"]:
                    alerts.append(f"⚠️ Below normal: {label} = {value}{ref['unit']}")
                    score += 4
                elif value > ref["normal_high"]:
                    alerts.append(f"⚠️ Above normal: {label} = {value}{ref['unit']}")
                    score += 4

        # Age adjustment: elderly and very young are higher risk
        if age >= 70 or age <= 5:
            score += 3

        return {"score": min(score, 40), "alerts": alerts}

    # ── symptom analysis ───────────────────────────────────────
    def _analyse_symptoms(self, symptoms: list[str]) -> dict:
        """Score symptoms by summing their severity weights."""
        score = 0.0
        details: list[str] = []
        red_flag_symptoms: list[str] = []

        for s in symptoms:
            info = ALL_SYMPTOMS.get(s)
            if info:
                score += info["weight"]
                details.append(f"{s} (weight {info['weight']}, category: {info['category']})")
                if info["red_flag"]:
                    red_flag_symptoms.append(s)

        # Cap at 40
        return {
            "score": min(score, 40),
            "details": details,
            "red_flag_symptoms": red_flag_symptoms,
        }

    # ── red-flag combinations ──────────────────────────────────
    def _detect_red_flags(self, symptoms: list[str], vitals: dict) -> list[dict]:
        """Check for known dangerous symptom combinations."""
        found = []
        symptom_set = set(symptoms)

        for combo in RED_FLAG_COMBINATIONS:
            required = set(combo["symptoms"])
            if required.issubset(symptom_set):
                found.append({
                    "name": combo["name"],
                    "escalate_to": combo.get("escalate_to"),
                    "diagnosis": combo.get("diagnosis", ""),
                })

        # Also flag individual critical vitals as red flags
        for key, value in vitals.items():
            if key not in VITAL_SIGN_RANGES or value is None:
                continue
            ref = VITAL_SIGN_RANGES[key]
            if key == "spo2" and value < ref["critical_low"]:
                found.append({"name": f"Critical SpO₂ ({value}%)", "escalate_to": 1, "diagnosis": ""})
            elif key == "gcs" and value <= ref["critical_low"]:
                found.append({"name": f"Severely reduced GCS ({value})", "escalate_to": 1, "diagnosis": ""})
            elif key not in ("spo2", "gcs"):
                if value <= ref["critical_low"] or value >= ref["critical_high"]:
                    found.append({
                        "name": f"Critical {ref['label']} ({value}{ref['unit']})",
                        "escalate_to": 2,
                        "diagnosis": "",
                    })

        return found

    # ── consciousness scoring ──────────────────────────────────
    def _score_consciousness(self, level: str) -> float:
        """Map consciousness level to a numeric score (0-10)."""
        mapping = {
            "Alert and oriented": 0,
            "Responds to voice": 4,
            "Responds to pain": 8,
            "Unresponsive": 10,
        }
        return mapping.get(level, 0)

    # ── pain scoring ───────────────────────────────────────────
    def _score_pain(self, pain: int) -> float:
        """Normalise 0-10 pain scale to 0-5 contribution."""
        return min(pain / 2, 5)

    # ── urgency calculation ────────────────────────────────────
    def _calculate_urgency(
        self,
        vital_score: float,
        symptom_score: float,
        red_flag_count: int,
        consciousness_score: float,
        pain_score: float,
    ) -> tuple[float, int]:
        """
        Combine sub-scores into a total urgency score (0-100) and map to
        a triage category (1-5).

        Weighting:
          - Vital signs:   35%
          - Symptoms:       30%
          - Red flags:      15%  (each flag adds ~5 points)
          - Consciousness:  12%
          - Pain:            8%
        """
        raw = (
            (vital_score / 40) * 35
            + (symptom_score / 40) * 30
            + min(red_flag_count * 5, 15)
            + (consciousness_score / 10) * 12
            + (pain_score / 5) * 8
        )
        urgency = min(raw, 100)

        # Map score to category
        if urgency >= 70:
            category = 1
        elif urgency >= 50:
            category = 2
        elif urgency >= 30:
            category = 3
        elif urgency >= 15:
            category = 4
        else:
            category = 5

        return urgency, category

    # ── differential diagnosis ─────────────────────────────────
    def _generate_diagnoses(self, symptoms: list[str], vitals: dict) -> list[dict]:
        """
        Match symptom+vital-sign patterns against the diagnosis rule base
        and return a ranked list of possible conditions with confidence %.
        """
        symptom_set = set(symptoms)
        candidates: list[dict] = []

        for rule in DIAGNOSIS_RULES:
            required = set(rule["required"])
            if not required.issubset(symptom_set):
                continue  # required symptoms not present

            # Base confidence from required match
            confidence = 0.40

            # Add confidence for each supporting symptom present
            supporting = set(rule.get("supporting", []))
            matched_supporting = supporting & symptom_set
            if supporting:
                confidence += 0.35 * (len(matched_supporting) / len(supporting))

            # Add confidence for matching vital-sign patterns
            confidence += rule.get("confidence_boost", 0)

            # Check vital sign alignment
            vs_rules = rule.get("vital_signs", {})
            for vs_key, expected in vs_rules.items():
                value = vitals.get(vs_key)
                if value is None or vs_key not in VITAL_SIGN_RANGES:
                    continue
                ref = VITAL_SIGN_RANGES[vs_key]
                if expected == "high" and value > ref["normal_high"]:
                    confidence += 0.05
                elif expected == "low" and value < ref["normal_low"]:
                    confidence += 0.05
                elif expected == "abnormal" and (
                    value < ref["normal_low"] or value > ref["normal_high"]
                ):
                    confidence += 0.05

            confidence = min(confidence, 0.95)

            candidates.append({
                "condition": rule["condition"],
                "confidence": round(confidence * 100, 1),
                "matched_symptoms": list(required | matched_supporting),
            })

        # Also add diagnoses from red-flag combinations
        for combo in RED_FLAG_COMBINATIONS:
            if set(combo["symptoms"]).issubset(symptom_set) and combo.get("diagnosis"):
                # Check it's not already in candidates
                existing = {c["condition"] for c in candidates}
                if combo["diagnosis"] not in existing:
                    candidates.append({
                        "condition": combo["diagnosis"],
                        "confidence": 70.0,
                        "matched_symptoms": combo["symptoms"],
                    })

        # Sort by confidence descending, take top 5
        candidates.sort(key=lambda x: x["confidence"], reverse=True)
        return candidates[:5]

    # ── reasoning narrative ────────────────────────────────────
    def _build_reasoning(
        self,
        category: int,
        vital_analysis: dict,
        symptom_analysis: dict,
        red_flags: list[dict],
        diagnoses: list[dict],
        consciousness: str,
        pain_level: int,
    ) -> str:
        """Build a human-readable explanation of the triage decision."""
        cat_info = TRIAGE_CATEGORIES[category]
        lines: list[str] = []

        lines.append(
            f"**Triage Category {category} — {cat_info['name']}** "
            f"({cat_info['description']})"
        )
        lines.append("")

        # Vital sign findings
        if vital_analysis["alerts"]:
            lines.append("**Vital Sign Findings:**")
            for alert in vital_analysis["alerts"]:
                lines.append(f"  • {alert}")
            lines.append("")

        # Red-flag warnings
        if red_flags:
            lines.append("**🚨 Red-Flag Warnings:**")
            for flag in red_flags:
                msg = f"  • {flag['name']}"
                if flag.get("diagnosis"):
                    msg += f" → Consider {flag['diagnosis']}"
                lines.append(msg)
            lines.append("")

        # Symptom severity
        if symptom_analysis["red_flag_symptoms"]:
            lines.append("**High-Severity Symptoms Present:**")
            for s in symptom_analysis["red_flag_symptoms"]:
                lines.append(f"  • {s}")
            lines.append("")

        # Consciousness and pain
        if consciousness != "Alert and oriented":
            lines.append(f"**Consciousness Level:** {consciousness}")
        if pain_level >= 7:
            lines.append(f"**Pain Level:** {pain_level}/10 (severe)")
        elif pain_level >= 4:
            lines.append(f"**Pain Level:** {pain_level}/10 (moderate)")
        lines.append("")

        # Differential diagnoses
        if diagnoses:
            lines.append("**Possible Diagnoses for Clinician Consideration:**")
            for i, d in enumerate(diagnoses, 1):
                lines.append(
                    f"  {i}. {d['condition']} "
                    f"(confidence: {d['confidence']}%)"
                )
            lines.append("")

        # Recommended action
        lines.append(f"**Recommended Action:** {cat_info['action']}")
        lines.append(f"**Maximum Acceptable Wait:** {cat_info['max_wait']}")

        # Disclaimer
        lines.append("")
        lines.append(
            "*This is a decision-support tool only. All clinical decisions "
            "must be confirmed by a qualified healthcare professional.*"
        )

        return "\n".join(lines)
