"""
SalesPulse Shared Sidebar
--------------------------
Renders the dark navy sidebar with logo, navigation links, and page switcher.
Call render_sidebar() at the top of every page.
"""

import streamlit as st


def render_sidebar(active_page: str = ""):
    """
    Renders the SalesPulse dark navy sidebar.
    active_page: pass the current page name to highlight the active nav item,
                 e.g. "Pipeline Analytics"
    """
    nav_pages = [
        ("📊", "Pipeline Analytics",  "pages/1_Pipeline_Analytics.py"),
        ("📈", "Sales Performance",   "pages/2_Sales_Performance.py"),
        ("🥧", "Win/Loss Analysis",   "pages/3_Win_Loss_Analysis.py"),
        ("🧠", "Behaviour Analytics", "pages/4_Behaviour_Analytics.py"),
        ("👥", "Team Performance",    "pages/5_Team_Performance.py"),
    ]

    with st.sidebar:
        # ── Logo ──────────────────────────────────────────────────────────
        st.markdown("""
        <div class="sp-sidebar-logo">
            <div class="sp-logo-mark">⚡</div>
            <div>
                <div class="sp-logo-wordmark">SalesPulse</div>
                <div class="sp-logo-sub">AI Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Navigation ────────────────────────────────────────────────────
        st.markdown('<div class="sp-nav-label">Navigation</div>', unsafe_allow_html=True)

        for icon, label, page_path in nav_pages:
            is_active = label == active_page
            active_cls = " active" if is_active else ""
            # Render styled nav item
            st.markdown(f"""
            <div class="sp-nav-item{active_cls}" id="nav-{label.replace(' ', '-').lower()}">
                <span class="sp-nav-icon">{icon}</span>
                <span>{label}</span>
            </div>
            """, unsafe_allow_html=True)
            # Invisible button for actual navigation
            btn_key = f"nav_btn_{page_path}"
            if st.button(label, key=btn_key, use_container_width=True,
                         help=f"Go to {label}",
                         disabled=is_active):
                st.switch_page(page_path)

        # ── Divider ───────────────────────────────────────────────────────
        st.markdown("""
        <style>
        /* Hide the button text — keep only the nav-item div as visual */
        div[data-testid="stSidebar"] .stButton button {
            position: relative;
            margin-top: -42px;
            opacity: 0;
            height: 42px;
            cursor: pointer;
        }
        </style>
        """, unsafe_allow_html=True)
