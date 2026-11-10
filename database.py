"""
TRIAGE-AI Database Layer
=========================
SQLite database for patient records, triage assessments, and audit logs.
"""

import sqlite3
import json
import os
from datetime import datetime


class TriageDatabase:
    """Manages all database operations for the TRIAGE-AI system."""

    def __init__(self, db_path="triage_ai.db"):
        self.db_path = db_path
        self.init_db()

    # ── helpers ────────────────────────────────────────────────
    def _connect(self):
        """Create a database connection with row_factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    # ── schema ─────────────────────────────────────────────────
    def init_db(self):
        """Initialise database tables if they do not exist."""
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id      TEXT    UNIQUE NOT NULL,
                first_name      TEXT    NOT NULL,
                last_name       TEXT    NOT NULL,
                age             INTEGER NOT NULL,
                gender          TEXT    NOT NULL,
                blood_type      TEXT    DEFAULT 'Unknown',
                contact_number  TEXT    DEFAULT '',
                allergies       TEXT    DEFAULT '',
                medical_history TEXT    DEFAULT '',
                arrival_mode    TEXT    DEFAULT 'Walk-in',
                current_triage  INTEGER DEFAULT 0,
                status          TEXT    DEFAULT 'Waiting',
                registered_at   TEXT    NOT NULL,
                updated_at      TEXT    NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id          TEXT    NOT NULL,
                symptoms            TEXT    NOT NULL,
                vital_signs         TEXT    NOT NULL,
                pain_level          INTEGER DEFAULT 0,
                consciousness_level TEXT    DEFAULT 'Alert and oriented',
                chief_complaint     TEXT    DEFAULT '',
                triage_category     INTEGER NOT NULL,
                urgency_score       REAL    NOT NULL,
                possible_diagnoses  TEXT    DEFAULT '[]',
                red_flags_found     TEXT    DEFAULT '[]',
                reasoning           TEXT    DEFAULT '',
                assessed_by         TEXT    DEFAULT 'System',
                assessed_at         TEXT    NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id  TEXT    NOT NULL,
                action      TEXT    NOT NULL,
                details     TEXT    DEFAULT '',
                performed_by TEXT   DEFAULT 'System',
                timestamp   TEXT    NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
            )
        """)

        conn.commit()
        conn.close()

    # ── patient CRUD ───────────────────────────────────────────
    def add_patient(self, data: dict) -> str:
        """Insert a new patient. Returns the patient_id."""
        now = datetime.now().isoformat()
        conn = self._connect()
        try:
            conn.execute(
                """INSERT INTO patients
                   (patient_id, first_name, last_name, age, gender,
                    blood_type, contact_number, allergies, medical_history,
                    arrival_mode, registered_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    data["patient_id"],
                    data["first_name"],
                    data["last_name"],
                    data["age"],
                    data["gender"],
                    data.get("blood_type", "Unknown"),
                    data.get("contact_number", ""),
                    data.get("allergies", ""),
                    data.get("medical_history", ""),
                    data.get("arrival_mode", "Walk-in"),
                    now,
                    now,
                ),
            )
            conn.commit()

            # audit
            self._log(conn, data["patient_id"], "REGISTERED",
                       f"Patient registered via {data.get('arrival_mode', 'Walk-in')}")
            conn.commit()
            return data["patient_id"]
        finally:
            conn.close()

    def get_patient(self, patient_id: str) -> dict | None:
        """Return a single patient record as a dict, or None."""
        conn = self._connect()
        row = conn.execute(
            "SELECT * FROM patients WHERE patient_id = ?", (patient_id,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    def get_all_patients(self) -> list[dict]:
        """Return every patient record, newest first."""
        conn = self._connect()
        rows = conn.execute(
            "SELECT * FROM patients ORDER BY registered_at DESC"
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_patients_by_status(self, status: str) -> list[dict]:
        """Filter patients by status (Waiting, Being Treated, Discharged)."""
        conn = self._connect()
        rows = conn.execute(
            "SELECT * FROM patients WHERE status = ? ORDER BY current_triage ASC",
            (status,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_patient(self, patient_id: str, updates: dict):
        """Update fields on a patient record."""
        now = datetime.now().isoformat()
        updates["updated_at"] = now
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [patient_id]

        conn = self._connect()
        conn.execute(
            f"UPDATE patients SET {set_clause} WHERE patient_id = ?", values
        )
        conn.commit()

        changes = ", ".join(f"{k}={v}" for k, v in updates.items() if k != "updated_at")
        self._log(conn, patient_id, "UPDATED", changes)
        conn.commit()
        conn.close()

    def update_patient_triage(self, patient_id: str, triage_category: int):
        """Convenience: update the current triage level."""
        self.update_patient(patient_id, {"current_triage": triage_category})

    def update_patient_status(self, patient_id: str, status: str):
        """Update patient status (Waiting / Being Treated / Discharged)."""
        self.update_patient(patient_id, {"status": status})

    def patient_id_exists(self, patient_id: str) -> bool:
        conn = self._connect()
        row = conn.execute(
            "SELECT 1 FROM patients WHERE patient_id = ?", (patient_id,)
        ).fetchone()
        conn.close()
        return row is not None

    # ── assessment CRUD ────────────────────────────────────────
    def add_assessment(self, data: dict) -> int:
        """Insert a triage assessment. Returns the new row id."""
        now = datetime.now().isoformat()
        conn = self._connect()
        try:
            cursor = conn.execute(
                """INSERT INTO assessments
                   (patient_id, symptoms, vital_signs, pain_level,
                    consciousness_level, chief_complaint,
                    triage_category, urgency_score,
                    possible_diagnoses, red_flags_found,
                    reasoning, assessed_by, assessed_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    data["patient_id"],
                    json.dumps(data.get("symptoms", [])),
                    json.dumps(data.get("vital_signs", {})),
                    data.get("pain_level", 0),
                    data.get("consciousness_level", "Alert and oriented"),
                    data.get("chief_complaint", ""),
                    data["triage_category"],
                    data["urgency_score"],
                    json.dumps(data.get("possible_diagnoses", [])),
                    json.dumps(data.get("red_flags_found", [])),
                    data.get("reasoning", ""),
                    data.get("assessed_by", "System"),
                    now,
                ),
            )
            conn.commit()

            # Also update patient's current triage level
            conn.execute(
                "UPDATE patients SET current_triage = ?, updated_at = ? WHERE patient_id = ?",
                (data["triage_category"], now, data["patient_id"]),
            )
            conn.commit()

            self._log(
                conn,
                data["patient_id"],
                "ASSESSED",
                f"Triage category: {data['triage_category']} | Score: {data['urgency_score']:.1f}",
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def get_assessments(self, patient_id: str) -> list[dict]:
        """Return all assessments for a patient, newest first."""
        conn = self._connect()
        rows = conn.execute(
            "SELECT * FROM assessments WHERE patient_id = ? ORDER BY assessed_at DESC",
            (patient_id,),
        ).fetchall()
        conn.close()

        results = []
        for r in rows:
            d = dict(r)
            d["symptoms"] = json.loads(d["symptoms"])
            d["vital_signs"] = json.loads(d["vital_signs"])
            d["possible_diagnoses"] = json.loads(d["possible_diagnoses"])
            d["red_flags_found"] = json.loads(d["red_flags_found"])
            results.append(d)
        return results

    def get_latest_assessment(self, patient_id: str) -> dict | None:
        """Return the most recent assessment for a patient."""
        assessments = self.get_assessments(patient_id)
        return assessments[0] if assessments else None

    # ── audit log ──────────────────────────────────────────────
    def _log(self, conn, patient_id: str, action: str, details: str = "",
             performed_by: str = "System"):
        """Internal: write an audit log entry using an existing connection."""
        conn.execute(
            "INSERT INTO audit_log (patient_id, action, details, performed_by, timestamp) VALUES (?, ?, ?, ?, ?)",
            (patient_id, action, details, performed_by, datetime.now().isoformat()),
        )

    def add_audit_entry(self, patient_id: str, action: str, details: str = "",
                        performed_by: str = "System"):
        """Public: write an audit log entry."""
        conn = self._connect()
        self._log(conn, patient_id, action, details, performed_by)
        conn.commit()
        conn.close()

    def get_audit_log(self, patient_id: str) -> list[dict]:
        """Return the full audit trail for a patient."""
        conn = self._connect()
        rows = conn.execute(
            "SELECT * FROM audit_log WHERE patient_id = ? ORDER BY timestamp DESC",
            (patient_id,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    # ── dashboard / analytics ──────────────────────────────────
    def get_dashboard_stats(self) -> dict:
        """Return aggregate statistics for the dashboard."""
        conn = self._connect()

        total = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
        waiting = conn.execute(
            "SELECT COUNT(*) FROM patients WHERE status = 'Waiting'"
        ).fetchone()[0]
        treating = conn.execute(
            "SELECT COUNT(*) FROM patients WHERE status = 'Being Treated'"
        ).fetchone()[0]
        discharged = conn.execute(
            "SELECT COUNT(*) FROM patients WHERE status = 'Discharged'"
        ).fetchone()[0]

        # Count by triage level
        triage_counts = {}
        for level in range(1, 6):
            count = conn.execute(
                "SELECT COUNT(*) FROM patients WHERE current_triage = ? AND status != 'Discharged'",
                (level,),
            ).fetchone()[0]
            triage_counts[level] = count

        # Unassessed patients (triage = 0)
        unassessed = conn.execute(
            "SELECT COUNT(*) FROM patients WHERE current_triage = 0 AND status != 'Discharged'"
        ).fetchone()[0]

        conn.close()

        return {
            "total_patients": total,
            "waiting": waiting,
            "being_treated": treating,
            "discharged": discharged,
            "triage_counts": triage_counts,
            "unassessed": unassessed,
        }

    def get_active_patients_sorted(self) -> list[dict]:
        """Return non-discharged patients sorted by urgency (category 1 first)."""
        conn = self._connect()
        rows = conn.execute(
            """SELECT * FROM patients
               WHERE status != 'Discharged'
               ORDER BY
                 CASE WHEN current_triage = 0 THEN 6 ELSE current_triage END ASC,
                 registered_at ASC"""
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def search_patients(self, query: str) -> list[dict]:
        """Search patients by ID, name, or status."""
        conn = self._connect()
        like = f"%{query}%"
        rows = conn.execute(
            """SELECT * FROM patients
               WHERE patient_id LIKE ? OR first_name LIKE ?
                  OR last_name LIKE ? OR status LIKE ?
               ORDER BY registered_at DESC""",
            (like, like, like, like),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def delete_patient(self, patient_id: str):
        """Remove a patient and all related records (for demo/reset)."""
        conn = self._connect()
        conn.execute("DELETE FROM audit_log WHERE patient_id = ?", (patient_id,))
        conn.execute("DELETE FROM assessments WHERE patient_id = ?", (patient_id,))
        conn.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
        conn.commit()
        conn.close()

    def reset_database(self):
        """Drop all data (for demo resets)."""
        conn = self._connect()
        conn.execute("DELETE FROM audit_log")
        conn.execute("DELETE FROM assessments")
        conn.execute("DELETE FROM patients")
        conn.commit()
        conn.close()
