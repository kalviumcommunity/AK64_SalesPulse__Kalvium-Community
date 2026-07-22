"""
SalesPulse AI — Streamlit Application Root Entry Point.
Run with: python -m streamlit run app.py
"""

import sys
import os

# Ensure the project root is on the Python path so all imports resolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

# ── 1. Page Config (must be the FIRST st call) ────────────────────────────────
st.set_page_config(
    page_title="SalesPulse AI — Sales Behaviour Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 2. Premium Design System ─────────────────────────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
    h1, h2, h3, h4 { font-family: 'Outfit', sans-serif !important; }

    /* Hide default streamlit header/footer */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* App background */
    .stApp { background-color: #f8fafc; color: #0f172a; }

    /* Container */
    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1400px;
    }

    /* Sidebar dark theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b0f19 0%, #111827 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.07) !important;
    }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }

    /* Sidebar radio nav */
    [data-testid="stSidebar"] .stRadio > div { gap: 4px !important; }
    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px;
        padding: 9px 14px;
        cursor: pointer;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        margin-bottom: 2px !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(99,102,241,0.15) !important;
        border-color: #6366f1 !important;
    }

    /* Metric values */
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        color: #0f172a !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover { transform: translateY(-1px); }

    /* Inputs */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* DataFrame */
    [data-testid="stDataFrame"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }
    </style>
""", unsafe_allow_html=True)

# ── 3. Lazy imports (after set_page_config) ───────────────────────────────────
from Frontend.views.auth import render_auth_page
from Frontend.views.performance import render_performance_view
from Frontend.views.pipeline import render_pipeline_view
from Frontend.views.win_loss import render_win_loss_view
from Frontend.views.behaviour import render_behaviour_view
from Frontend.views.team import render_team_view
from Frontend.views.recommendations import render_recommendations_view
from Frontend.views.crm import render_crm_view
from Frontend.views.settings import render_settings_view
from Frontend.utils.components import render_top_navbar, render_stat_card

# ── 4. Auth Guard ─────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated", False):
    render_auth_page()
    st.stop()

user = st.session_state.get("user", {"name": "Sales User", "role": "Sales Representative"})
user_role = user.get("role", "Sales Representative")

# ── 5. Top Navbar ─────────────────────────────────────────────────────────────
render_top_navbar()

# ── 6. Sidebar Navigation ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='display:flex; align-items:center; gap:0.75rem; padding-bottom:1.1rem;
                    border-bottom:1px solid rgba(255,255,255,0.08); margin-bottom:1.1rem;'>
            <div style='background:linear-gradient(135deg,#6366f1,#4f46e5); color:#fff;
                        width:40px; height:40px; border-radius:10px; display:flex;
                        align-items:center; justify-content:center; font-size:1.2rem;
                        box-shadow:0 4px 14px rgba(99,102,241,0.4); font-weight:bold;'>
                ⚡
            </div>
            <div>
                <div style='color:#fff; font-weight:800; font-size:1.15rem;
                            font-family:Outfit,sans-serif; line-height:1.2;'>SalesPulse AI</div>
                <div style='color:#94a3b8; font-size:0.75rem; font-weight:500;'>Behaviour Intelligence</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Role badge
    st.markdown(f"""
        <div style='background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.08);
                    padding:0.65rem 0.9rem; border-radius:10px; margin-bottom:1.1rem;'>
            <div style='font-size:0.7rem; color:#94a3b8; text-transform:uppercase;
                        letter-spacing:0.6px; font-weight:700;'>Active Workspace</div>
            <div style='font-size:0.9rem; color:#60a5fa; font-weight:800; margin-top:2px;
                        font-family:Outfit,sans-serif;'>{user_role}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#94a3b8; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.8px; font-weight:700; margin-bottom:6px;'>Navigation</p>", unsafe_allow_html=True)

    nav_options = [
        "📊 Sales Performance",
        "📈 Pipeline Analytics",
        "🏆 Win / Loss Analysis",
        "⚡ Behaviour Analytics",
    ]
    if user_role in ["Sales Manager", "VP of Sales / Admin", "VP of Sales"]:
        nav_options.append("👥 Team Performance")
    nav_options += ["💡 AI Coaching Tips", "📧 CRM & Email Upload", "⚙️ Settings"]

    selected_page = st.radio("nav", nav_options, index=0, label_visibility="collapsed")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.07); margin:1.2rem 0;'>", unsafe_allow_html=True)

    if st.button("🚪 Sign Out", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ── 7. Page Router ────────────────────────────────────────────────────────────
page_map = {
    "📊 Sales Performance":   render_performance_view,
    "📈 Pipeline Analytics":  render_pipeline_view,
    "🏆 Win / Loss Analysis": render_win_loss_view,
    "⚡ Behaviour Analytics": render_behaviour_view,
    "👥 Team Performance":    render_team_view,
    "💡 AI Coaching Tips":    render_recommendations_view,
    "📧 CRM & Email Upload":  render_crm_view,
    "⚙️ Settings":            render_settings_view,
}

render_fn = page_map.get(selected_page)
if render_fn:
    render_fn()
