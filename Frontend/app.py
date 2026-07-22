"""
SalesPulse AI — Streamlit Main Application Entrypoint.
AI-Powered Sales Behaviour Intelligence Platform for B2B Organizations.
"""

import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="SalesPulse AI — Sales Behaviour Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Premium Google Fonts & Comprehensive Custom CSS Design System
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    h1, h2, h3, h4, .stHeader {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Main Canvas Background */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1380px;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* Radio Button Navigation Styling */
    div[row-widget="radio"] > div {
        gap: 8px;
    }
    div[row-widget="radio"] label {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 10px 14px;
        cursor: pointer;
        transition: all 0.25 ease;
        font-weight: 600;
        font-size: 0.92rem;
        display: flex;
        align-items: center;
    }
    div[row-widget="radio"] label:hover {
        background: rgba(99, 102, 241, 0.15) !important;
        border-color: #6366f1 !important;
        color: #ffffff !important;
    }

    /* Dataframe & Table Styling */
    [data-testid="stDataFrame"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 15px -3px rgba(15, 23, 42, 0.03) !important;
        background: #ffffff !important;
    }

    /* Metric Override */
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
    }

    /* Primary & Secondary Buttons */
    .stButton>button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15) !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.25) !important;
    }

    /* Input Controls */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* Expander Card */
    .streamlit-expanderHeader {
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1rem !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. View Imports & Helper Renderers
from Frontend.utils.components import render_top_navbar
from Frontend.views.auth import render_auth_page
from Frontend.views.performance import render_performance_view
from Frontend.views.pipeline import render_pipeline_view
from Frontend.views.win_loss import render_win_loss_view
from Frontend.views.behaviour import render_behaviour_view
from Frontend.views.team import render_team_view
from Frontend.views.recommendations import render_recommendations_view
from Frontend.views.crm import render_crm_view
from Frontend.views.settings import render_settings_view

# 4. Authentication Guard
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    render_auth_page()
    st.stop()

user = st.session_state.get("user", {"name": "Sales User", "role": "Sales Representative"})
user_role = user.get("role", "Sales Representative")

# 5. Render Top Header Navbar
render_top_navbar()

# 6. Sidebar Navigation Drawer
with st.sidebar:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 0.85rem; padding-bottom: 1.25rem; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 1.25rem;'>
            <div style='
                background: linear-gradient(135deg, #6366f1, #4f46e5);
                color: white;
                width: 42px;
                height: 42px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.3rem;
                font-weight: bold;
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
            '>
                ⚡
            </div>
            <div>
                <h3 style='color: #ffffff; margin: 0; font-weight: 800; font-size: 1.25rem; font-family: Outfit, sans-serif;'>SalesPulse AI</h3>
                <p style='color: #94a3b8; font-size: 0.78rem; margin: 0; font-weight: 500;'>Behaviour Intelligence</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Active Role Box
    st.markdown(f"""
        <div style='
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.08);
            padding: 0.75rem 0.9rem;
            border-radius: 12px;
            margin-bottom: 1.25rem;
        '>
            <div style='font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.6px; font-weight: 700;'>Workspace Scope</div>
            <div style='font-size: 0.92rem; color: #60a5fa; font-weight: 800; margin-top: 2px; font-family: Outfit, sans-serif;'>{user_role}</div>
        </div>
    """, unsafe_allow_html=True)

    # Navigation Menu Options
    nav_options = [
        "📊 Sales Performance",
        "📈 Pipeline Analytics",
        "🏆 Win / Loss Analysis",
        "⚡ Behaviour Analytics"
    ]

    if user_role in ["Sales Manager", "VP of Sales / Admin"]:
        nav_options.append("👥 Team Performance")

    nav_options.extend([
        "💡 AI Coaching Tips",
        "📧 CRM & Email Upload",
        "⚙️ System Settings"
    ])

    selected_page = st.radio("NAVIGATION", nav_options, index=0)

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
    if st.button("Sign Out", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.rerun()

# 7. Page Routing
if selected_page == "📊 Sales Performance":
    render_performance_view()
elif selected_page == "📈 Pipeline Analytics":
    render_pipeline_view()
elif selected_page == "🏆 Win / Loss Analysis":
    render_win_loss_view()
elif selected_page == "⚡ Behaviour Analytics":
    render_behaviour_view()
elif selected_page == "👥 Team Performance":
    render_team_view()
elif selected_page == "💡 AI Coaching Tips":
    render_recommendations_view()
elif selected_page == "📧 CRM & Email Upload":
    render_crm_view()
elif selected_page == "⚙️ System Settings":
    render_settings_view()
