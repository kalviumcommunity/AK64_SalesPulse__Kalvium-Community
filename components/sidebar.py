"""
SalesPulse Shared Sidebar
--------------------------
Renders the dark navy sidebar with logo and navigation buttons.
No authentication required.
"""

import streamlit as st


def render_sidebar(active_page: str = ""):
    """
    Renders the SalesPulse sidebar with brand logo and nav buttons.
    active_page: name of current page to highlight (e.g. "Pipeline Analytics").
    """
    nav_pages = [
        ("📊", "Pipeline Analytics",  "pages/1_Pipeline_Analytics.py"),
        ("📈", "Sales Performance",   "pages/2_Sales_Performance.py"),
        ("🥧", "Win/Loss Analysis",   "pages/3_Win_Loss_Analysis.py"),
        ("🧠", "Behaviour Analytics", "pages/4_Behaviour_Analytics.py"),
        ("👥", "Team Performance",    "pages/5_Team_Performance.py"),
    ]

    with st.sidebar:
        # ── Logo ──────────────────────────────────────────────────────────────
        st.markdown("""
        <div class="sp-sidebar-logo">
            <div class="sp-logo-mark">⚡</div>
            <div>
                <div class="sp-logo-wordmark">SalesPulse</div>
                <div class="sp-logo-sub">AI Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Navigation Buttons ─────────────────────────────────────────────────
        for icon, label, page_path in nav_pages:
            is_current = label == active_page
            if st.button(f"{icon}  {label}", key=f"nav_{page_path}",
                         use_container_width=True, disabled=is_current):
                st.switch_page(page_path)
