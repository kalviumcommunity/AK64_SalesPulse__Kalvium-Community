"""
SalesPulse Page Top Bar
------------------------
Renders the page title strip (compact h1 + subtitle line).
No user/login/session-user logic.
"""

import streamlit as st


def render_top_bar(page_title: str, subtitle: str = "Real-time AI-powered sales intelligence"):
    st.markdown(f"""
    <div style="padding: 2px 0 0 0; margin-bottom: 4px;">
        <h1 class="sp-page-title">{page_title}</h1>
        <div class="sp-page-sub">{subtitle}</div>
    </div>
    <hr class="sp-hr" style="margin-top: 10px; margin-bottom: 14px;">
    """, unsafe_allow_html=True)
