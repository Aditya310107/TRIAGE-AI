"""
TRIAGE-AI — Intelligent Clinical Decision Support & Prioritisation
High-Tech Cyber-Clinical Dark Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import uuid
import json

from config import (
    TRIAGE_CATEGORIES,
    SYMPTOM_CATEGORIES,
    VITAL_SIGN_RANGES,
    GENDER_OPTIONS,
    BLOOD_TYPE_OPTIONS,
    CONSCIOUSNESS_LEVELS,
    PAIN_LEVELS,
    ARRIVAL_MODES,
)
from database import TriageDatabase
from triage_engine import TriageEngine

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="TRIAGE-AI | Emergency Clinical Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "db" not in st.session_state:
    st.session_state.db = TriageDatabase()
if "engine" not in st.session_state:
    st.session_state.engine = TriageEngine()

db: TriageDatabase = st.session_state.db
engine: TriageEngine = st.session_state.engine

# ═══════════════════════════════════════════════════════════════
# HIGH-TECH DARK CLINICAL CSS (Cyber-Medical Theme)
# ═══════════════════════════════════════════════════════════════
def apply_dark_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"], .stMarkdown {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #F1F5F9 !important;
    }
    .stApp {
        background: radial-gradient(circle at top right, #0F172A 0%, #090D16 100%) !important;
    }
    .main .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1240px !important;
    }

    /* Top App Header Banner */
    .dark-hero {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 14px;
        padding: 22px 28px;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5), 0 0 15px rgba(56, 189, 248, 0.05);
    }
    .dark-hero h2 {
        margin: 0 !important;
        font-size: 1.55rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.025em;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .dark-hero p {
        margin: 4px 0 0 0 !important;
        font-size: 0.88rem !important;
        color: #94A3B8 !important;
        font-weight: 500;
    }
    .dark-live-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.12);
        color: #34D399 !important;
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.15);
    }
    .pulse-dot-dark {
        width: 8px;
        height: 8px;
        background-color: #34D399;
        border-radius: 50%;
        box-shadow: 0 0 8px #34D399;
    }

    /* Metric Cards - Glowing Dark */
    .dark-stat-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .dark-stat-card:hover {
        transform: translateY(-2px);
        border-color: #374151;
        box-shadow: 0 8px 16px -2px rgba(0, 0, 0, 0.5);
    }
    .glow-strip {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }
    .dark-stat-card .m-label {
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    .dark-stat-card .m-val {
        font-size: 2.15rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.03em;
        line-height: 1;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .dark-stat-card .m-sub {
        font-size: 0.76rem;
        color: #64748B;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Empty state box */
    .empty-state-box {
        background: #111827;
        border: 1px dashed #334155;
        border-radius: 12px;
        padding: 40px 20px;
        text-align: center;
        color: #94A3B8;
        margin-top: 10px;
    }
    .empty-state-box .icon {
        font-size: 2rem;
        margin-bottom: 8px;
    }

    /* Sidebar Dark Styling */
    section[data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid #1E293B !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        background-color: #111827 !important;
        border: 1px solid #1F2937 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        color: #CBD5E1 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: all 0.15s ease !important;
        margin-bottom: 4px;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: #1E293B !important;
        border-color: #38BDF8 !important;
        color: #38BDF8 !important;
    }
    section[data-testid="stSidebar"] .stRadio [data-testid="stRadioButtonCustom"] {
        display: none !important;
    }

    /* Triage Badges in Dark Mode */
    .t-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 11px;
        border-radius: 6px;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .badge-c1 { background: rgba(239, 68, 68, 0.15); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.4); box-shadow: 0 0 10px rgba(239, 68, 68, 0.2); }
    .badge-c2 { background: rgba(249, 115, 22, 0.15); color: #FB923C; border: 1px solid rgba(249, 115, 22, 0.4); }
    .badge-c3 { background: rgba(251, 191, 36, 0.15); color: #FBBF24; border: 1px solid rgba(251, 191, 36, 0.4); }
    .badge-c4 { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.4); }
    .badge-c5 { background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.4); }
    .badge-c0 { background: rgba(148, 163, 184, 0.15); color: #94A3B8; border: 1px solid rgba(148, 163, 184, 0.3); }

    /* Dark Patient Queue Card */
    .dark-patient-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-left-width: 4.5px;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        transition: all 0.15s ease;
    }
    .dark-patient-card:hover {
        border-color: #374151;
        box-shadow: 0 6px 14px rgba(0,0,0,0.4);
    }
    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .card-title {
        font-weight: 700;
        font-size: 0.98rem;
        color: #F8FAFC;
    }
    .card-meta {
        font-size: 0.82rem;
        color: #94A3B8;
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
    }

    /* Dark Form Box */
    div[data-testid="stForm"] {
        background: #111827 !important;
        border: 1px solid #1F2937 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }

    button[kind="primary"] {
        background: linear-gradient(135deg, #0284C7 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.4rem !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35) !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0369A1 0%, #1D4ED8 100%) !important;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.5) !important;
    }

    input, textarea, select {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    .triage-hero-box {
        border-radius: 12px;
        padding: 22px;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    #MainMenu, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

apply_dark_theme()

# ═══════════════════════════════════════════════════════════════
# UI HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def render_hero(title: str, subtitle: str, status_text: str = "SYSTEM ONLINE"):
    st.markdown(f"""
    <div class="dark-hero">
        <div>
            <h2>🩺 {title}</h2>
            <p>{subtitle}</p>
        </div>
        <div class="dark-live-pill">
            <span class="pulse-dot-dark"></span>
            {status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_pill(level: int) -> str:
    cls = f"badge-c{level}" if level in range(0, 6) else "badge-c0"
    if level == 0:
        return f'<span class="t-badge {cls}">⚪ Unassessed</span>'
    cat = TRIAGE_CATEGORIES.get(level, {})
    return f'<span class="t-badge {cls}">{cat.get("emoji","")} Cat {level} · {cat.get("name","")}</span>'

def render_stat(label: str, value: int, stripe_hex: str, sub: str):
    return f"""
    <div class="dark-stat-card">
        <div class="glow-strip" style="background-color: {stripe_hex}; box-shadow: 0 0 10px {stripe_hex};"></div>
        <div class="m-label">{label}</div>
        <div class="m-val">{value}</div>
        <div class="m-sub">{sub}</div>
    </div>
    """

def generate_patient_id() -> str:
    return "PT-" + uuid.uuid4().hex[:8].upper()

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚡ **TRIAGE-AI**")
    st.caption("Cyber-Clinical Emergency Prioritisation")
    st.write("")

    page = st.radio(
        "Navigation",
        [
            "⚡ Overview",
            "📋 Register Patient",
            "🩺 Triage Assessment",
            "📊 Priority Board",
            "📜 Patient Directory",
            "🔄 Reassessment",
        ],
        index=0,
    )

    st.write("")
    st.markdown("---")

    stats = db.get_dashboard_stats()
    st.markdown("###### **Department Acuity**")
    cw, ct = st.columns(2)
    with cw:
        st.metric("Waiting", stats["waiting"])
    with ct:
        st.metric("Treating", stats["being_treated"])

    st.caption(f"Active Census: **{stats['total_patients'] - stats['discharged']}** patients")
    st.caption("Standard: Manchester / ESI Emergency")

# ═══════════════════════════════════════════════════════════════
# 1. OVERVIEW PAGE
# ═══════════════════════════════════════════════════════════════
if page == "⚡ Overview":
    render_hero("Emergency Command Center", "Live clinical throughput, acuity distribution, and triage status")

    stats = db.get_dashboard_stats()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(render_stat("Total Admitted", stats["total_patients"], "#38BDF8", "Current clinical shift"), unsafe_allow_html=True)
    with c2:
        st.markdown(render_stat("Awaiting Care", stats["waiting"], "#F97316", "Priority queue in triage"), unsafe_allow_html=True)
    with c3:
        st.markdown(render_stat("Under Treatment", stats["being_treated"], "#10B981", "Active in trauma bays"), unsafe_allow_html=True)
    with c4:
        st.markdown(render_stat("Discharged", stats["discharged"], "#64748B", "Stabilized & transitioned"), unsafe_allow_html=True)

    st.write("")

    col_chart1, col_chart2 = st.columns([1.1, 1])

    with col_chart1:
        st.markdown("##### **Acuity Breakdown (ESI / Manchester)**")
        triage_data = stats["triage_counts"]
        if any(triage_data.values()):
            labels = [f"Cat {k}: {TRIAGE_CATEGORIES[k]['name']}" for k in triage_data]
            colors = ["#EF4444", "#F97316", "#FBBF24", "#10B981", "#38BDF8"]
            fig_pie = px.pie(
                names=labels,
                values=list(triage_data.values()),
                color_discrete_sequence=colors,
                hole=0.55,
                template="plotly_dark",
            )
            fig_pie.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=290,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.markdown("""
            <div class="empty-state-box">
                <div class="icon">📊</div>
                <div>No patient data logged. Register and triage patients to generate analytics.</div>
            </div>
            """, unsafe_allow_html=True)

    with col_chart2:
        st.markdown("##### **Clinical Workflow Pipeline**")
        status_data = {
            "Waiting": stats["waiting"],
            "Under Treatment": stats["being_treated"],
            "Discharged": stats["discharged"],
        }
        if any(status_data.values()):
            fig_bar = px.bar(
                x=list(status_data.keys()),
                y=list(status_data.values()),
                color=list(status_data.keys()),
                color_discrete_map={
                    "Waiting": "#F97316",
                    "Under Treatment": "#10B981",
                    "Discharged": "#64748B",
                },
                template="plotly_dark",
            )
            fig_bar.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=290,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                xaxis_title="",
                yaxis_title="Patient Volume",
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.markdown("""
            <div class="empty-state-box">
                <div class="icon">🏥</div>
                <div>Queue is clear. 0 patients currently admitted.</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.markdown("##### **Triage Urgency Protocol Matrix**")
    ref_cols = st.columns(5)
    for i, (level, info) in enumerate(TRIAGE_CATEGORIES.items()):
        with ref_cols[i]:
            neon_border = ["#EF4444", "#F97316", "#FBBF24", "#10B981", "#38BDF8"][i]
            st.markdown(
                f"""<div style="background:#111827; border: 1px solid #1F2937; border-top: 3px solid {neon_border};
                    border-radius:10px; padding:14px; min-height:140px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:800; color:{neon_border}; font-size:0.92rem;">{info['emoji']} Cat {level}</span>
                        <span style="font-size:0.75rem; font-weight:700; color:#CBD5E1;">{info['max_wait']}</span>
                    </div>
                    <div style="font-weight:700; font-size:0.83rem; color:#F8FAFC; margin:5px 0 3px 0;">{info['name']}</div>
                    <div style="font-size:0.75rem; color:#94A3B8; line-height:1.35;">{info['description']}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.write("")
    with st.expander("⚙️ Admin Reset"):
        if st.button("Reset Database Records", type="secondary"):
            db.reset_database()
            st.success("All patient records successfully deleted.")
            st.rerun()

# ═══════════════════════════════════════════════════════════════
# 2. REGISTER PATIENT
# ═══════════════════════════════════════════════════════════════
elif page == "📋 Register Patient":
    render_hero("Patient Intake Registration", "Capture patient demographics, allergies, and arrival logistics")

    with st.form("patient_registration_form", clear_on_submit=True):
        st.markdown("##### **1. Personal Identification**")
        c1, c2, c3 = st.columns([1, 1.5, 1.5])
        with c1:
            patient_id = st.text_input("Patient Identifier", value=generate_patient_id())
        with c2:
            first_name = st.text_input("First Name *")
        with c3:
            last_name = st.text_input("Last Name *")

        st.markdown("##### **2. Clinical Demographics**")
        c4, c5, c6, c7 = st.columns(4)
        with c4:
            age = st.number_input("Age (Years) *", 0, 120, 35)
        with c5:
            gender = st.selectbox("Gender *", GENDER_OPTIONS)
        with c6:
            blood_type = st.selectbox("Blood Group", BLOOD_TYPE_OPTIONS)
        with c7:
            arrival_mode = st.selectbox("Arrival Logistics", ARRIVAL_MODES)

        contact = st.text_input("Emergency Contact Number", placeholder="e.g. +91 98765 43210")

        st.markdown("##### **3. Clinical History & Allergies**")
        ca, cb = st.columns(2)
        with ca:
            allergies = st.text_area("Documented Allergies", placeholder="Penicillin, NSAIDs, Latex, or NKDA (No Known Drug Allergies)", height=80)
        with cb:
            history = st.text_area("Pre-existing Medical History", placeholder="Type 2 Diabetes, Essential Hypertension, CAD, Asthma...", height=80)

        st.write("")
        submit = st.form_submit_button("Complete Patient Registration", type="primary", use_container_width=True)

        if submit:
            if not first_name.strip() or not last_name.strip():
                st.error("First Name and Last Name are required.")
            elif db.patient_id_exists(patient_id):
                st.error(f"Identifier {patient_id} already exists.")
            else:
                db.add_patient({
                    "patient_id": patient_id,
                    "first_name": first_name.strip(),
                    "last_name": last_name.strip(),
                    "age": age,
                    "gender": gender,
                    "blood_type": blood_type,
                    "contact_number": contact.strip(),
                    "allergies": allergies.strip(),
                    "medical_history": history.strip(),
                    "arrival_mode": arrival_mode,
                })
                st.success(f"✓ Patient {first_name} {last_name} ({patient_id}) successfully registered. Proceed to Triage Assessment.")

# ═══════════════════════════════════════════════════════════════
# 3. TRIAGE ASSESSMENT
# ═══════════════════════════════════════════════════════════════
elif page == "🩺 Triage Assessment":
    render_hero("Clinical Triage Assessment", "Objective physiological vitals, symptoms analysis, and urgency classification")

    patients = db.get_all_patients()
    if not patients:
        st.warning("No registered patients found. Please complete Patient Registration first.")
        st.stop()

    lookup = {
        f"{p['patient_id']} — {p['first_name']} {p['last_name']} ({p['age']}y, {p['gender']})": p["patient_id"]
        for p in patients
    }
    sel_label = st.selectbox("Select Patient to Assess", list(lookup.keys()))
    sel_pid = lookup[sel_label]
    pt = db.get_patient(sel_pid)

    st.markdown(f"""
    <div style="background:#111827; border:1px solid #1F2937; border-radius:10px; padding:14px 18px; margin-bottom:1.25rem;">
        <div style="font-weight:800; color:#F8FAFC; font-size:1.05rem;">{pt['first_name']} {pt['last_name']} <span style="font-weight:500; color:#38BDF8;">({pt['patient_id']})</span></div>
        <div style="color:#94A3B8; font-size:0.84rem; margin-top:4px;">
            Age: <strong style="color:#F1F5F9;">{pt['age']}</strong> &nbsp;|&nbsp; Gender: <strong style="color:#F1F5F9;">{pt['gender']}</strong> &nbsp;|&nbsp;
            Blood Group: <strong style="color:#F1F5F9;">{pt['blood_type']}</strong> &nbsp;|&nbsp; Mode: <strong style="color:#F1F5F9;">{pt['arrival_mode']}</strong> &nbsp;|&nbsp;
            Allergies: <strong style="color:#F1F5F9;">{pt['allergies'] or 'NKDA'}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("triage_eval_form"):
        complaint = st.text_input("Chief Presenting Complaint", placeholder="e.g. Acute retrosternal chest pain radiating to jaw and left arm")

        st.markdown("##### **Physiological Vital Signs**")
        v1, v2, v3, v4 = st.columns(4)
        with v1:
            hr = st.number_input("Heart Rate (bpm)", 30, 250, 78)
            sbp = st.number_input("Systolic BP (mmHg)", 40, 300, 120)
        with v2:
            dbp = st.number_input("Diastolic BP (mmHg)", 20, 200, 80)
            rr = st.number_input("Respiratory Rate (/min)", 0, 60, 16)
        with v3:
            spo2 = st.number_input("Oxygen Saturation SpO₂ (%)", 50, 100, 98)
            temp = st.number_input("Body Temp (°C)", 30.0, 45.0, 37.0, step=0.1, format="%.1f")
        with v4:
            gcs = st.number_input("Glasgow Coma Scale (3-15)", 3, 15, 15)
            consc = st.selectbox("Consciousness Level", CONSCIOUSNESS_LEVELS)

        st.markdown("##### **Symptom Inventory by System**")
        selected_symptoms: list[str] = []
        sym_tabs = st.tabs(list(SYMPTOM_CATEGORIES.keys()))
        for tab, (category, symptoms) in zip(sym_tabs, SYMPTOM_CATEGORIES.items()):
            with tab:
                chosen = st.multiselect(
                    f"{category} Symptoms",
                    [s["name"] for s in symptoms],
                    key=f"sym_{category}",
                    label_visibility="collapsed",
                )
                selected_symptoms.extend(chosen)

        st.markdown("##### **Pain Severity & Assessor**")
        p1, p2 = st.columns([2, 1])
        with p1:
            pain = st.slider("Visual Analog Pain Scale (0 = None, 10 = Max)", 0, 10, 2)
        with p2:
            clinician = st.text_input("Triage Clinician", value="Attending Emergency Physician")

        st.write("")
        submit_triage = st.form_submit_button("Execute Decision Support Engine", type="primary", use_container_width=True)

    if submit_triage:
        vitals = {
            "heart_rate": hr,
            "systolic_bp": sbp,
            "diastolic_bp": dbp,
            "respiratory_rate": rr,
            "spo2": spo2,
            "temperature": temp,
            "gcs": gcs,
        }

        with st.spinner("Analyzing clinical parameters..."):
            res = engine.assess(
                symptoms=selected_symptoms,
                vital_signs=vitals,
                pain_level=pain,
                consciousness=consc,
                age=pt["age"],
                chief_complaint=complaint,
            )

        db.add_assessment({
            "patient_id": sel_pid,
            "symptoms": selected_symptoms,
            "vital_signs": vitals,
            "pain_level": pain,
            "consciousness_level": consc,
            "chief_complaint": complaint,
            "triage_category": res["triage_category"],
            "urgency_score": res["urgency_score"],
            "possible_diagnoses": res["possible_diagnoses"],
            "red_flags_found": res["red_flags_found"],
            "reasoning": res["reasoning"],
            "assessed_by": clinician,
        })

        cat = res["triage_category"]
        info = TRIAGE_CATEGORIES[cat]
        glow_color = ["#EF4444", "#F97316", "#FBBF24", "#10B981", "#38BDF8"][cat - 1]

        st.markdown(f"""
        <div class="triage-hero-box" style="background:#111827; border: 2px solid {glow_color}; box-shadow: 0 0 20px {glow_color}33;">
            <h2 style="color:{glow_color}; margin:0; font-size:1.85rem;">
                {info['emoji']} CATEGORY {cat} — {info['name']}
            </h2>
            <p style="color:#CBD5E1; font-size:1.05rem; margin:6px 0 2px 0;">{info['description']}</p>
            <div style="font-weight:700; color:{glow_color}; font-size:0.95rem;">Target Physician Time: {info['max_wait']}</div>
        </div>
        """, unsafe_allow_html=True)

        cg, calerts = st.columns([1, 1.5])
        with cg:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=res["urgency_score"],
                title={"text": "Acuity Score (0-100)"},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#94A3B8"},
                    "bar": {"color": glow_color},
                    "steps": [
                        {"range": [0, 15], "color": "#1E293B"},
                        {"range": [15, 30], "color": "#064E3B"},
                        {"range": [30, 50], "color": "#78350F"},
                        {"range": [50, 70], "color": "#7C2D12"},
                        {"range": [70, 100], "color": "#7F1D1D"},
                    ],
                },
            ))
            gauge.update_layout(height=240, margin=dict(t=30, b=10, l=15, r=15), paper_bgcolor="rgba(0,0,0,0)", template="plotly_dark")
            st.plotly_chart(gauge, use_container_width=True)

        with calerts:
            if res["red_flags_found"]:
                st.error("🚨 **Clinical Red Flags Triggered**")
                for rf in res["red_flags_found"]:
                    st.markdown(f"• **{rf}**")
            if res["vital_sign_alerts"]:
                st.warning("⚠️ **Physiological Boundary Alerts**")
                for va in res["vital_sign_alerts"]:
                    st.markdown(f"• {va}")
            if not res["red_flags_found"] and not res["vital_sign_alerts"]:
                st.success("✓ Normal vital sign parameters. No critical red-flags triggered.")

        if res["possible_diagnoses"]:
            st.markdown("##### **Differential Diagnoses & Confidence**")
            df_diag = pd.DataFrame(res["possible_diagnoses"])
            df_diag.columns = ["Condition", "Confidence (%)", "Correlated Symptoms"]
            fig_bar = px.bar(
                df_diag,
                x="Confidence (%)",
                y="Condition",
                orientation="h",
                color="Confidence (%)",
                color_continuous_scale=["#38BDF8", "#EF4444"],
                range_color=[0, 100],
                template="plotly_dark",
            )
            fig_bar.update_layout(
                height=210,
                margin=dict(t=5, b=5, l=5, r=5),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis={"autorange": "reversed"},
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with st.expander("Clinical Decision Reasoning", expanded=True):
            st.markdown(res["reasoning"])

# ═══════════════════════════════════════════════════════════════
# 4. PRIORITY BOARD
# ═══════════════════════════════════════════════════════════════
elif page == "📊 Priority Board":
    render_hero("Emergency Priority Board", "Active queue sequencing sorted by clinical acuity")

    active = db.get_active_patients_sorted()

    if not active:
        st.markdown("""
        <div class="empty-state-box">
            <div class="icon">📋</div>
            <div>No active patients in queue. Admitted patients will appear here sorted by triage category.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for level in range(0, 6):
            pts_in_level = [p for p in active if p["current_triage"] == level]
            if not pts_in_level:
                continue

            border_c = ["#EF4444", "#F97316", "#FBBF24", "#10B981", "#38BDF8"][level - 1] if level > 0 else "#64748B"
            cat_name = f"Cat {level} — {TRIAGE_CATEGORIES[level]['name']}" if level > 0 else "Unassessed Queue"

            st.markdown(f"###### **{cat_name}**")

            for p in pts_in_level:
                latest = db.get_latest_assessment(p["patient_id"])
                dx_text = ""
                if latest and latest["possible_diagnoses"]:
                    dx_text = f"· Top Dx: <strong style='color:#F1F5F9;'>{latest['possible_diagnoses'][0]['condition']}</strong> ({latest['possible_diagnoses'][0]['confidence']}%)"

                st.markdown(f"""
                <div class="dark-patient-card" style="border-left-color: {border_c}; box-shadow: 0 0 10px {border_c}22;">
                    <div class="card-top">
                        <span class="card-title">{p['first_name']} {p['last_name']} <span style="font-weight:400; color:#38BDF8;">({p['patient_id']})</span></span>
                        <span>{render_pill(p['current_triage'])}</span>
                    </div>
                    <div class="card-meta">
                        <span>Status: <strong style="color:#F1F5F9;">{p['status']}</strong></span>
                        <span>{p['age']}y ({p['gender']})</span>
                        <span>Mode: {p['arrival_mode']}</span>
                        <span>{dx_text}</span>
                        <span>Admitted: {p['registered_at'][:16].replace('T', ' ')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.write("")
        st.markdown("---")
        st.markdown("##### **Update Care Status**")
        update_map = {f"{p['patient_id']} — {p['first_name']} {p['last_name']}": p["patient_id"] for p in active}
        u1, u2, u3 = st.columns([2.5, 1.5, 1])
        with u1:
            sel_u = st.selectbox("Select Patient", list(update_map.keys()))
        with u2:
            st_choice = st.selectbox("New Care Status", ["Waiting", "Being Treated", "Discharged"])
        with u3:
            st.write("")
            st.write("")
            if st.button("Apply Transition", type="primary", use_container_width=True):
                pid = update_map[sel_u]
                db.update_patient_status(pid, st_choice)
                st.success(f"Status updated for {pid} → {st_choice}")
                st.rerun()

# ═══════════════════════════════════════════════════════════════
# 5. PATIENT RECORDS DIRECTORY
# ═══════════════════════════════════════════════════════════════
elif page == "📜 Patient Directory":
    render_hero("Patient Records Directory", "Search patient files, historical triage assessments, and audit logs")

    q = st.text_input("🔍 Search patient directory (ID, name, or status)", placeholder="e.g. PT-A109 or Sharma")
    all_pts = db.search_patients(q) if q else db.get_all_patients()

    if not all_pts:
        st.markdown("""
        <div class="empty-state-box">
            <div class="icon">🔍</div>
            <div>No matching patient records found in database.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        df = pd.DataFrame(all_pts)
        display_cols = ["patient_id", "first_name", "last_name", "age", "gender", "current_triage", "status", "arrival_mode", "registered_at"]
        display_cols = [c for c in display_cols if c in df.columns]

        st.dataframe(
            df[display_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "patient_id": "Patient ID",
                "first_name": "First Name",
                "last_name": "Last Name",
                "age": "Age",
                "gender": "Gender",
                "current_triage": st.column_config.NumberColumn("Triage Cat", format="%d"),
                "status": "Care Status",
                "arrival_mode": "Arrival Mode",
                "registered_at": "Registered At",
            },
        )

        st.write("")
        st.markdown("##### **Detailed Clinical Dossier**")
        pt_map = {f"{p['patient_id']} — {p['first_name']} {p['last_name']}": p["patient_id"] for p in all_pts}
        sel_rec = st.selectbox("Select Patient to Inspect", list(pt_map.keys()))
        rec_id = pt_map[sel_rec]
        target_pt = db.get_patient(rec_id)

        if target_pt:
            c_info, c_audit = st.columns([1.5, 1])
            with c_info:
                st.markdown(f"#### {target_pt['first_name']} {target_pt['last_name']}")
                st.markdown(render_pill(target_pt["current_triage"]), unsafe_allow_html=True)
                st.markdown(f"""
                - **ID:** `{target_pt['patient_id']}`
                - **Demographics:** {target_pt['age']} years | {target_pt['gender']}
                - **Blood Group:** {target_pt['blood_type']}
                - **Allergies:** {target_pt['allergies'] or 'NKDA'}
                - **Medical History:** {target_pt['medical_history'] or 'None recorded'}
                """)
            with c_audit:
                st.markdown("###### System Audit Trail")
                audit = db.get_audit_log(rec_id)
                if audit:
                    df_a = pd.DataFrame(audit)[["timestamp", "action", "details", "performed_by"]]
                    st.dataframe(df_a, use_container_width=True, hide_index=True)
                else:
                    st.caption("No audit history recorded.")

            history = db.get_assessments(rec_id)
            st.markdown(f"###### Assessment Progression ({len(history)} recorded)")
            for i, ass in enumerate(history):
                c_level = ass["triage_category"]
                meta = TRIAGE_CATEGORIES.get(c_level, {})
                with st.expander(f"Assessment #{len(history)-i} · Category {c_level} ({meta.get('name','')}) · {ass['assessed_at'][:16].replace('T',' ')}", expanded=(i==0)):
                    st.markdown(render_pill(c_level), unsafe_allow_html=True)
                    st.write(f"**Urgency Index:** {ass['urgency_score']} / 100 &nbsp;|&nbsp; **Pain:** {ass['pain_level']}/10 &nbsp;|&nbsp; **Consciousness:** {ass['consciousness_level']}")
                    st.write(f"**Chief Complaint:** {ass.get('chief_complaint') or 'None'}")
                    st.write(f"**Symptoms:** {', '.join(ass['symptoms']) if ass['symptoms'] else 'None'}")
                    if ass["possible_diagnoses"]:
                        st.write("**Differential Diagnoses:**")
                        for d in ass["possible_diagnoses"]:
                            st.write(f"- {d['condition']} ({d['confidence']}%)")
                    st.markdown(ass.get("reasoning", ""))

# ═══════════════════════════════════════════════════════════════
# 6. REASSESSMENT
# ═══════════════════════════════════════════════════════════════
elif page == "🔄 Reassessment":
    render_header("Patient Reassessment", "Re-evaluate clinical trajectory and escalate or de-escalate triage status")

    active_pts = [p for p in db.get_all_patients() if p["status"] != "Discharged"]
    if not active_pts:
        st.markdown("""
        <div class="empty-state-box">
            <div class="icon">🔄</div>
            <div>No active non-discharged patients available for reassessment.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        re_map = {f"{p['patient_id']} — {p['first_name']} {p['last_name']} (Cat {p['current_triage']})": p["patient_id"] for p in active_pts}
        sel_re = st.selectbox("Select Patient to Reassess", list(re_map.keys()))
        re_pid = re_map[sel_re]
        pt = db.get_patient(re_pid)
        latest = db.get_latest_assessment(re_pid)

        if latest:
            st.info(f"**Current Baseline:** {render_pill(latest['triage_category'])} &nbsp;|&nbsp; "
                    f"Urgency Score: **{latest['urgency_score']}/100** &nbsp;|&nbsp; "
                    f"Pain: **{latest['pain_level']}/10**", icon="⚡")

        with st.form("reassessment_form"):
            notes = st.text_input("Clinical Evolution Notes", placeholder="e.g. Chest pain relieved post nitroglycerin; respiratory rate returned to normal")

            st.markdown("##### **Current Vital Signs**")
            prev = latest["vital_signs"] if latest else {}
            r1, r2, r3, r4 = st.columns(4)
            with r1:
                hr = st.number_input("Heart Rate (bpm)", 30, 250, value=int(prev.get("heart_rate", 75)))
                sbp = st.number_input("Systolic BP (mmHg)", 40, 300, value=int(prev.get("systolic_bp", 120)))
            with r2:
                dbp = st.number_input("Diastolic BP (mmHg)", 20, 200, value=int(prev.get("diastolic_bp", 80)))
                rr = st.number_input("Respiratory Rate (/min)", 0, 60, value=int(prev.get("respiratory_rate", 16)))
            with r3:
                spo2 = st.number_input("SpO₂ (%)", 50, 100, value=int(prev.get("spo2", 98)))
                temp = st.number_input("Temp (°C)", 30.0, 45.0, value=float(prev.get("temperature", 37.0)), step=0.1, format="%.1f")
            with r4:
                gcs = st.number_input("GCS", 3, 15, value=int(prev.get("gcs", 15)))
                consc = st.selectbox(
                    "Consciousness",
                    CONSCIOUSNESS_LEVELS,
                    index=CONSCIOUSNESS_LEVELS.index(latest["consciousness_level"]) if (latest and latest["consciousness_level"] in CONSCIOUSNESS_LEVELS) else 0,
                )

            st.markdown("##### **Presenting Symptoms**")
            selected_symptoms: list[str] = []
            sym_tabs = st.tabs(list(SYMPTOM_CATEGORIES.keys()))
            prev_syms = latest["symptoms"] if latest else []
            for tab, (category, symptoms) in zip(sym_tabs, SYMPTOM_CATEGORIES.items()):
                with tab:
                    s_names = [s["name"] for s in symptoms]
                    defaults = [s for s in s_names if s in prev_syms]
                    chosen = st.multiselect(category, s_names, default=defaults, key=f"re_s_{category}", label_visibility="collapsed")
                    selected_symptoms.extend(chosen)

            pain = st.slider("Current Pain Score", 0, 10, value=int(latest["pain_level"]) if latest else 0)
            re_by = st.text_input("Reassessing Clinician", value="Attending Emergency Physician")

            st.write("")
            re_submit = st.form_submit_button("Submit Reassessment", type="primary", use_container_width=True)

        if re_submit:
            vitals = {
                "heart_rate": hr,
                "systolic_bp": sbp,
                "diastolic_bp": dbp,
                "respiratory_rate": rr,
                "spo2": spo2,
                "temperature": temp,
                "gcs": gcs,
            }

            with st.spinner("Calculating trajectory..."):
                res = engine.assess(
                    symptoms=selected_symptoms,
                    vital_signs=vitals,
                    pain_level=pain,
                    consciousness=consc,
                    age=pt["age"],
                    chief_complaint=notes,
                )

            db.add_assessment({
                "patient_id": re_pid,
                "symptoms": selected_symptoms,
                "vital_signs": vitals,
                "pain_level": pain,
                "consciousness_level": consc,
                "chief_complaint": notes,
                "triage_category": res["triage_category"],
                "urgency_score": res["urgency_score"],
                "possible_diagnoses": res["possible_diagnoses"],
                "red_flags_found": res["red_flags_found"],
                "reasoning": res["reasoning"],
                "assessed_by": re_by,
            })

            cat = res["triage_category"]
            info = TRIAGE_CATEGORIES[cat]
            glow_color = ["#EF4444", "#F97316", "#FBBF24", "#10B981", "#38BDF8"][cat - 1]

            if latest:
                prev_cat = latest["triage_category"]
                if cat < prev_cat:
                    st.error(f"🚨 **ESCALATION:** Patient urgency increased from Category {prev_cat} → Category {cat}")
                elif cat > prev_cat:
                    st.success(f"✓ **DE-ESCALATION:** Patient condition improved from Category {prev_cat} → Category {cat}")
                else:
                    st.info(f"↔ **STABLE:** Urgency remains Category {cat}")

            st.markdown(f"""
            <div class="triage-hero-box" style="background:#111827; border: 2px solid {glow_color}; box-shadow: 0 0 20px {glow_color}33;">
                <h2 style="color:{glow_color}; margin:0;">
                    {info['emoji']} CATEGORY {cat} — {info['name']}
                </h2>
                <p style="margin:4px 0 0 0; color:#CBD5E1;">Updated Urgency Score: <strong>{res['urgency_score']}/100</strong></p>
            </div>
            """, unsafe_allow_html=True)
