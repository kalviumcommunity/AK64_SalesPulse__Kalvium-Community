"""
SalesPulse AI - PRD v1.0.0 Main Entrypoint & Authentication Engine
------------------------------------------------------------------
Powers 5 core sales intelligence views with JWT authentication and role-based access control.
Dark navy sidebar with icon-based navigation and authenticated user chip.
"""

import streamlit as st
import os
import sys
import importlib

sys.path.append(os.path.dirname(__file__))

from components.styles import inject_custom_css
from components.login import render_login_page

st.set_page_config(
    page_title="SalesPulse AI — Sales Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()

# ── Session State Init ────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state["user"] = None
if "jwt_token" not in st.session_state:
    st.session_state["jwt_token"] = None

# ── Dark Navy Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    # Logo Header
    st.markdown("""
    <div class="sp-sidebar-logo">
        <div class="sp-logo-mark">⚡</div>
        <div>
            <div class="sp-logo-wordmark">SalesPulse</div>
            <div class="sp-logo-sub">AI Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    u = st.session_state.get("user")

    if u:
        # Navigation Label
        st.markdown('<div class="sp-nav-label">Navigation</div>', unsafe_allow_html=True)

        # Nav Items — active page detection via query params or simple links
        nav_pages = [
            ("📊", "Pipeline Analytics",  "1_Pipeline_Analytics"),
            ("📈", "Sales Performance",   "2_Sales_Performance"),
            ("🥧", "Win/Loss Analysis",   "3_Win_Loss_Analysis"),
            ("🧠", "Behaviour Analytics", "4_Behaviour_Analytics"),
            ("👥", "Team Performance",    "5_Team_Performance"),
        ]

        for icon, label, page_key in nav_pages:
            st.markdown(f"""
            <a href="/{page_key.replace('_', '_')}" target="_self" style="text-decoration:none;">
                <div class="sp-nav-item">
                    <span class="sp-nav-icon">{icon}</span>
                    <span>{label}</span>
                </div>
            </a>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sp-nav-label" style="margin-top:20px;">Account</div>', unsafe_allow_html=True)

        # User chip
        initials = "".join([n[0] for n in u["name"].split()[:2]])
        role_disp = u.get("role", "rep").upper()
        st.markdown(f"""
        <div style="padding: 8px 10px;">
            <div class="sp-user-chip">
                <div class="sp-user-avatar">{initials}</div>
                <div>
                    <div class="sp-user-name">{u['name']}</div>
                    <div class="sp-user-role">{role_disp}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔒 Sign Out", use_container_width=True, key="sidebar_signout"):
            st.session_state["user"] = None
            st.session_state["jwt_token"] = None
            st.rerun()

    else:
        st.markdown("""
        <div style="padding: 20px 16px;">
            <div style="font-size:13px; color:#64748B; line-height:1.5;">
                🔐 Sign in to access your<br>sales intelligence dashboard.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Main Render ───────────────────────────────────────────────────────────────
if st.session_state["user"] is None:
    render_login_page()
else:
    pipeline_module = importlib.import_module("pages.1_Pipeline_Analytics")
