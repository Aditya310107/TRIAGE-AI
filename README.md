# TRIAGE-AI  🏥
## Intelligent Emergency Patient Prioritisation & Clinical Decision Support

A professional, AI-assisted web application for emergency patient triage,
built with **Streamlit**, **Python**, **SQLite**, and **Plotly**.

---

### 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

---

### 📁 Project Structure

```
triage-ai/
├── app.py               # Main Streamlit application (all UI pages)
├── config.py            # Clinical constants, symptom library, rules
├── database.py          # SQLite database layer
├── triage_engine.py     # Rule-based clinical decision engine
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── triage_ai.db         # SQLite database (auto-created on first run)
```

---

### 🏥 Features

| Feature | Description |
|---------|-------------|
| **Patient Registration** | Capture demographics, allergies, medical history, arrival mode |
| **Triage Assessment** | Symptom selection, vital signs entry, pain & consciousness scoring |
| **AI Decision Engine** | Rule-based urgency scoring with 5-level triage classification |
| **Differential Diagnosis** | Pattern-matched possible conditions with confidence levels |
| **Red-Flag Detection** | Automatic escalation for dangerous symptom combinations |
| **Priority Dashboard** | Real-time patient board sorted by clinical urgency |
| **Analytics** | Plotly charts for triage distribution, patient flow, and workload |
| **Patient History** | Full assessment timeline with audit trail |
| **Reassessment** | Update vitals/symptoms and re-triage existing patients |

---

### 🔴🟠🟡🟢🔵 Triage Categories

| Level | Name | Max Wait | Description |
|-------|------|----------|-------------|
| 1 | RESUSCITATION | Immediate | Life-threatening, requires resuscitation |
| 2 | EMERGENT | ≤ 10 min | Potentially life-threatening |
| 3 | URGENT | ≤ 30 min | Serious but currently stable |
| 4 | LESS URGENT | ≤ 60 min | Standard priority |
| 5 | NON-URGENT | ≤ 120 min | Minor condition |

---

### ⚠️ Disclaimer

**This application is a decision-support demonstration tool only.**
It is designed for educational and conference presentation purposes.
All clinical decisions must be made by qualified healthcare professionals.
This tool does not replace professional medical judgement.

---

### 📋 Requirements

- Python 3.10 or higher
- Streamlit ≥ 1.28.0
- Pandas ≥ 2.0.0
- Plotly ≥ 5.18.0
