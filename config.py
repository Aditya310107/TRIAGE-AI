"""
TRIAGE-AI Configuration
========================
Central configuration for triage categories, symptom definitions,
vital sign ranges, red flags, and clinical pattern rules.
"""

# ──────────────────────────────────────────────────────────────
# TRIAGE CATEGORIES (based on Manchester / ESI systems)
# ──────────────────────────────────────────────────────────────
TRIAGE_CATEGORIES = {
    1: {
        "name": "RESUSCITATION",
        "color": "#DC2626",
        "bg_color": "#FEE2E2",
        "emoji": "🔴",
        "description": "Immediate life-threatening condition requiring resuscitation",
        "max_wait": "Immediate (0 min)",
        "action": "Immediate physician assessment and intervention",
    },
    2: {
        "name": "EMERGENT",
        "color": "#EA580C",
        "bg_color": "#FFEDD5",
        "emoji": "🟠",
        "description": "Potentially life-threatening condition or risk of deterioration",
        "max_wait": "≤ 10 minutes",
        "action": "Rapid physician assessment",
    },
    3: {
        "name": "URGENT",
        "color": "#CA8A04",
        "bg_color": "#FEF9C3",
        "emoji": "🟡",
        "description": "Serious condition that is currently stable",
        "max_wait": "≤ 30 minutes",
        "action": "Physician assessment within 30 minutes",
    },
    4: {
        "name": "LESS URGENT",
        "color": "#16A34A",
        "bg_color": "#DCFCE7",
        "emoji": "🟢",
        "description": "Condition requiring attention but not time-critical",
        "max_wait": "≤ 60 minutes",
        "action": "Standard assessment when available",
    },
    5: {
        "name": "NON-URGENT",
        "color": "#2563EB",
        "bg_color": "#DBEAFE",
        "emoji": "🔵",
        "description": "Minor condition suitable for routine care",
        "max_wait": "≤ 120 minutes",
        "action": "Routine assessment; consider GP referral",
    },
}

# ──────────────────────────────────────────────────────────────
# SYMPTOM LIBRARY with severity weights (0-10)
# ──────────────────────────────────────────────────────────────
SYMPTOM_CATEGORIES = {
    "Cardiovascular": [
        {"name": "Chest pain", "weight": 9, "red_flag": True},
        {"name": "Palpitations", "weight": 5, "red_flag": False},
        {"name": "Syncope (fainting)", "weight": 8, "red_flag": True},
        {"name": "Leg swelling (unilateral)", "weight": 7, "red_flag": True},
        {"name": "Cyanosis (blue lips/fingers)", "weight": 9, "red_flag": True},
    ],
    "Respiratory": [
        {"name": "Shortness of breath", "weight": 8, "red_flag": True},
        {"name": "Wheezing", "weight": 5, "red_flag": False},
        {"name": "Cough", "weight": 2, "red_flag": False},
        {"name": "Coughing up blood", "weight": 9, "red_flag": True},
        {"name": "Stridor (noisy breathing)", "weight": 9, "red_flag": True},
        {"name": "Unable to speak full sentences", "weight": 9, "red_flag": True},
    ],
    "Neurological": [
        {"name": "Severe headache (sudden onset)", "weight": 9, "red_flag": True},
        {"name": "Seizures", "weight": 9, "red_flag": True},
        {"name": "Confusion / altered mental status", "weight": 8, "red_flag": True},
        {"name": "Weakness (one-sided)", "weight": 9, "red_flag": True},
        {"name": "Speech difficulty", "weight": 9, "red_flag": True},
        {"name": "Vision loss (sudden)", "weight": 9, "red_flag": True},
        {"name": "Dizziness", "weight": 3, "red_flag": False},
        {"name": "Numbness / tingling", "weight": 4, "red_flag": False},
        {"name": "Neck stiffness", "weight": 7, "red_flag": True},
    ],
    "Gastrointestinal": [
        {"name": "Abdominal pain (severe)", "weight": 7, "red_flag": True},
        {"name": "Abdominal pain (mild/moderate)", "weight": 3, "red_flag": False},
        {"name": "Vomiting blood", "weight": 9, "red_flag": True},
        {"name": "Blood in stool", "weight": 7, "red_flag": True},
        {"name": "Nausea / vomiting", "weight": 3, "red_flag": False},
        {"name": "Diarrhoea", "weight": 2, "red_flag": False},
        {"name": "Inability to keep fluids down", "weight": 6, "red_flag": False},
    ],
    "Trauma / Injury": [
        {"name": "Major trauma / RTA", "weight": 10, "red_flag": True},
        {"name": "Uncontrolled bleeding", "weight": 10, "red_flag": True},
        {"name": "Suspected fracture", "weight": 5, "red_flag": False},
        {"name": "Head injury with LOC", "weight": 9, "red_flag": True},
        {"name": "Burns (large area / airway)", "weight": 9, "red_flag": True},
        {"name": "Penetrating wound", "weight": 9, "red_flag": True},
        {"name": "Minor laceration", "weight": 2, "red_flag": False},
        {"name": "Sprain / strain", "weight": 2, "red_flag": False},
    ],
    "Allergic / Immune": [
        {"name": "Anaphylaxis signs (swelling, rash, SOB)", "weight": 10, "red_flag": True},
        {"name": "Allergic reaction (mild)", "weight": 4, "red_flag": False},
        {"name": "Urticaria (hives)", "weight": 3, "red_flag": False},
    ],
    "General / Systemic": [
        {"name": "Fever (> 38.5°C)", "weight": 4, "red_flag": False},
        {"name": "High fever (> 40°C)", "weight": 7, "red_flag": True},
        {"name": "Hypothermia (< 35°C)", "weight": 8, "red_flag": True},
        {"name": "Severe dehydration signs", "weight": 7, "red_flag": True},
        {"name": "Fatigue / malaise", "weight": 1, "red_flag": False},
        {"name": "Rash (non-specific)", "weight": 2, "red_flag": False},
        {"name": "Weight loss (unintentional)", "weight": 3, "red_flag": False},
    ],
    "Psychiatric / Behavioural": [
        {"name": "Suicidal ideation", "weight": 10, "red_flag": True},
        {"name": "Self-harm", "weight": 9, "red_flag": True},
        {"name": "Acute psychosis", "weight": 8, "red_flag": True},
        {"name": "Severe agitation", "weight": 7, "red_flag": True},
        {"name": "Anxiety / panic attack", "weight": 4, "red_flag": False},
    ],
    "Obstetric / Gynaecological": [
        {"name": "Vaginal bleeding (pregnant)", "weight": 9, "red_flag": True},
        {"name": "Severe pelvic pain", "weight": 7, "red_flag": True},
        {"name": "Imminent delivery", "weight": 10, "red_flag": True},
    ],
    "Urological": [
        {"name": "Urinary retention", "weight": 6, "red_flag": False},
        {"name": "Haematuria (blood in urine)", "weight": 5, "red_flag": False},
        {"name": "Flank pain (severe, colicky)", "weight": 6, "red_flag": False},
    ],
}

# Flatten all symptoms for easy lookup
ALL_SYMPTOMS = {}
for category, symptoms in SYMPTOM_CATEGORIES.items():
    for symptom in symptoms:
        ALL_SYMPTOMS[symptom["name"]] = {
            "category": category,
            "weight": symptom["weight"],
            "red_flag": symptom["red_flag"],
        }

# ──────────────────────────────────────────────────────────────
# VITAL SIGN NORMAL RANGES (adult defaults)
# ──────────────────────────────────────────────────────────────
VITAL_SIGN_RANGES = {
    "heart_rate": {
        "label": "Heart Rate (bpm)",
        "min": 30,
        "max": 250,
        "normal_low": 60,
        "normal_high": 100,
        "critical_low": 40,
        "critical_high": 150,
        "unit": "bpm",
    },
    "systolic_bp": {
        "label": "Systolic BP (mmHg)",
        "min": 40,
        "max": 300,
        "normal_low": 90,
        "normal_high": 140,
        "critical_low": 80,
        "critical_high": 200,
        "unit": "mmHg",
    },
    "diastolic_bp": {
        "label": "Diastolic BP (mmHg)",
        "min": 20,
        "max": 200,
        "normal_low": 60,
        "normal_high": 90,
        "critical_low": 40,
        "critical_high": 130,
        "unit": "mmHg",
    },
    "spo2": {
        "label": "SpO₂ (%)",
        "min": 50,
        "max": 100,
        "normal_low": 95,
        "normal_high": 100,
        "critical_low": 90,
        "critical_high": 101,  # no upper critical
        "unit": "%",
    },
    "respiratory_rate": {
        "label": "Respiratory Rate (breaths/min)",
        "min": 0,
        "max": 60,
        "normal_low": 12,
        "normal_high": 20,
        "critical_low": 8,
        "critical_high": 30,
        "unit": "breaths/min",
    },
    "temperature": {
        "label": "Temperature (°C)",
        "min": 30.0,
        "max": 45.0,
        "normal_low": 36.1,
        "normal_high": 37.5,
        "critical_low": 35.0,
        "critical_high": 40.0,
        "unit": "°C",
    },
    "gcs": {
        "label": "Glasgow Coma Scale (3-15)",
        "min": 3,
        "max": 15,
        "normal_low": 15,
        "normal_high": 15,
        "critical_low": 9,
        "critical_high": 16,  # no upper critical
        "unit": "",
    },
}

# ──────────────────────────────────────────────────────────────
# RED-FLAG COMBINATIONS (symptom patterns that escalate urgency)
# ──────────────────────────────────────────────────────────────
RED_FLAG_COMBINATIONS = [
    {
        "name": "Acute Coronary Syndrome Pattern",
        "symptoms": ["Chest pain", "Shortness of breath"],
        "escalate_to": 1,
        "diagnosis": "Possible Acute Coronary Syndrome (ACS)",
    },
    {
        "name": "Stroke Pattern (FAST)",
        "symptoms": ["Weakness (one-sided)", "Speech difficulty"],
        "escalate_to": 1,
        "diagnosis": "Possible Cerebrovascular Accident (Stroke)",
    },
    {
        "name": "Meningitis Pattern",
        "symptoms": ["Severe headache (sudden onset)", "Neck stiffness"],
        "escalate_to": 1,
        "diagnosis": "Possible Meningitis",
    },
    {
        "name": "Subarachnoid Haemorrhage Pattern",
        "symptoms": ["Severe headache (sudden onset)", "Syncope (fainting)"],
        "escalate_to": 1,
        "diagnosis": "Possible Subarachnoid Haemorrhage",
    },
    {
        "name": "Pulmonary Embolism Pattern",
        "symptoms": ["Shortness of breath", "Leg swelling (unilateral)", "Chest pain"],
        "escalate_to": 1,
        "diagnosis": "Possible Pulmonary Embolism",
    },
    {
        "name": "Sepsis Pattern",
        "symptoms": ["High fever (> 40°C)", "Confusion / altered mental status"],
        "escalate_to": 1,
        "diagnosis": "Possible Sepsis",
    },
    {
        "name": "GI Haemorrhage Pattern",
        "symptoms": ["Vomiting blood", "Blood in stool"],
        "escalate_to": 2,
        "diagnosis": "Possible Upper GI Haemorrhage",
    },
    {
        "name": "Ectopic Pregnancy Pattern",
        "symptoms": ["Vaginal bleeding (pregnant)", "Severe pelvic pain"],
        "escalate_to": 1,
        "diagnosis": "Possible Ectopic Pregnancy",
    },
    {
        "name": "Diabetic Emergency Pattern",
        "symptoms": ["Confusion / altered mental status", "Severe dehydration signs"],
        "escalate_to": 2,
        "diagnosis": "Possible Diabetic Ketoacidosis / Hypoglycaemia",
    },
]

# ──────────────────────────────────────────────────────────────
# DIFFERENTIAL DIAGNOSIS RULES (symptom → possible conditions)
# ──────────────────────────────────────────────────────────────
DIAGNOSIS_RULES = [
    {
        "condition": "Acute Coronary Syndrome (ACS)",
        "required": ["Chest pain"],
        "supporting": ["Shortness of breath", "Palpitations", "Syncope (fainting)", "Nausea / vomiting"],
        "vital_signs": {"heart_rate": "abnormal", "systolic_bp": "abnormal"},
        "confidence_boost": 0.15,
    },
    {
        "condition": "Cerebrovascular Accident (Stroke)",
        "required": ["Weakness (one-sided)"],
        "supporting": ["Speech difficulty", "Vision loss (sudden)", "Severe headache (sudden onset)", "Confusion / altered mental status"],
        "vital_signs": {"systolic_bp": "high"},
        "confidence_boost": 0.15,
    },
    {
        "condition": "Pulmonary Embolism",
        "required": ["Shortness of breath"],
        "supporting": ["Chest pain", "Leg swelling (unilateral)", "Coughing up blood", "Palpitations"],
        "vital_signs": {"heart_rate": "high", "spo2": "low"},
        "confidence_boost": 0.10,
    },
    {
        "condition": "Pneumonia",
        "required": ["Cough"],
        "supporting": ["Fever (> 38.5°C)", "Shortness of breath", "Chest pain"],
        "vital_signs": {"temperature": "high", "respiratory_rate": "high"},
        "confidence_boost": 0.10,
    },
    {
        "condition": "Asthma Exacerbation",
        "required": ["Wheezing"],
        "supporting": ["Shortness of breath", "Unable to speak full sentences", "Cough"],
        "vital_signs": {"respiratory_rate": "high", "spo2": "low"},
        "confidence_boost": 0.10,
    },
    {
        "condition": "Anaphylaxis",
        "required": ["Anaphylaxis signs (swelling, rash, SOB)"],
        "supporting": ["Shortness of breath", "Urticaria (hives)"],
        "vital_signs": {"heart_rate": "high", "systolic_bp": "low"},
        "confidence_boost": 0.20,
    },
    {
        "condition": "Meningitis",
        "required": ["Neck stiffness"],
        "supporting": ["Severe headache (sudden onset)", "High fever (> 40°C)", "Confusion / altered mental status", "Rash (non-specific)"],
        "vital_signs": {"temperature": "high", "heart_rate": "high"},
        "confidence_boost": 0.15,
    },
    {
        "condition": "Acute Appendicitis",
        "required": ["Abdominal pain (severe)"],
        "supporting": ["Nausea / vomiting", "Fever (> 38.5°C)"],
        "vital_signs": {"temperature": "high"},
        "confidence_boost": 0.10,
    },
    {
        "condition": "Renal Colic",
        "required": ["Flank pain (severe, colicky)"],
        "supporting": ["Haematuria (blood in urine)", "Nausea / vomiting"],
        "vital_signs": {},
        "confidence_boost": 0.10,
    },
    {
        "condition": "Seizure Disorder",
        "required": ["Seizures"],
        "supporting": ["Confusion / altered mental status"],
        "vital_signs": {},
        "confidence_boost": 0.10,
    },
    {
        "condition": "Upper GI Bleed",
        "required": ["Vomiting blood"],
        "supporting": ["Blood in stool", "Abdominal pain (severe)", "Syncope (fainting)"],
        "vital_signs": {"heart_rate": "high", "systolic_bp": "low"},
        "confidence_boost": 0.15,
    },
    {
        "condition": "Tension Headache / Migraine",
        "required": ["Severe headache (sudden onset)"],
        "supporting": ["Nausea / vomiting", "Vision loss (sudden)"],
        "vital_signs": {},
        "confidence_boost": 0.05,
    },
    {
        "condition": "Deep Vein Thrombosis (DVT)",
        "required": ["Leg swelling (unilateral)"],
        "supporting": [],
        "vital_signs": {},
        "confidence_boost": 0.05,
    },
    {
        "condition": "Acute Psychiatric Emergency",
        "required": ["Suicidal ideation"],
        "supporting": ["Self-harm", "Acute psychosis", "Severe agitation"],
        "vital_signs": {},
        "confidence_boost": 0.15,
    },
    {
        "condition": "Gastroenteritis",
        "required": ["Diarrhoea"],
        "supporting": ["Nausea / vomiting", "Abdominal pain (mild/moderate)", "Fever (> 38.5°C)", "Severe dehydration signs"],
        "vital_signs": {},
        "confidence_boost": 0.05,
    },
]

# ──────────────────────────────────────────────────────────────
# UI CONFIGURATION
# ──────────────────────────────────────────────────────────────
GENDER_OPTIONS = ["Male", "Female", "Other", "Prefer not to say"]
BLOOD_TYPE_OPTIONS = ["Unknown", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
CONSCIOUSNESS_LEVELS = [
    "Alert and oriented",
    "Responds to voice",
    "Responds to pain",
    "Unresponsive",
]
PAIN_LEVELS = list(range(0, 11))  # 0-10 scale

ARRIVAL_MODES = [
    "Walk-in",
    "Ambulance",
    "Helicopter / Air ambulance",
    "Police escort",
    "Referred from another facility",
    "Other",
]
