"""
SalesPulse Shared Sidebar
--------------------------
Renders the dark navy sidebar with logo, navigation links, and page switcher.
Call render_sidebar() at the top of every page.
"""

import streamlit as st


def render_sidebar(active_page: str = ""):
    """
    Renders the SalesPulse dark navy sidebar brand logo header.
    Streamlit native sidebar handles page switching automatically.
    """
    with st.sidebar:
        st.markdown("""
        <div class="sp-sidebar-logo">
            <div class="sp-logo-mark">⚡</div>
            <div>
                <div class="sp-logo-wordmark">SalesPulse</div>
                <div class="sp-logo-sub">AI Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

