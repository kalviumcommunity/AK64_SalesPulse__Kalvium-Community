"""
SalesPulse Page Top Bar
------------------------
Renders the page title strip + date/segment filter controls.
No user/login/session-user logic.
"""

import streamlit as st
from datetime import date


def render_top_bar(page_title: str, subtitle: str = "Real-time AI-powered sales intelligence"):
    st.markdown(f"""
    <div style="padding: 4px 0 0 0;">
        <h1 class="sp-page-title">{page_title}</h1>
        <div class="sp-page-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<hr class="sp-hr">', unsafe_allow_html=True)
