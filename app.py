"""
SalesPulse AI — Main Entrypoint (No Login Demo Mode)
------------------------------------------------------
Auto-redirects to Pipeline Analytics on load.
"""

import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(__file__))

from components.styles import inject_custom_css

st.set_page_config(
    page_title="SalesPulse AI — Sales Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()

# Auto-redirect to Pipeline Analytics home page
st.switch_page("pages/1_Pipeline_Analytics.py")
