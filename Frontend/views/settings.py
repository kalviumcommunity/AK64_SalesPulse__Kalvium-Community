"""
Settings View for SalesPulse AI Streamlit Frontend.
Manages user profile, active role scoping, and backend API endpoints.
"""

import streamlit as st
from Frontend.utils.api import NODE_BACKEND_URL, FASTAPI_AI_URL, check_backend_status
from Frontend.utils.components import render_section_header

def render_settings_view():
    render_section_header("System & User Settings", "Configure user profile, role-based navigation scoping, and backend endpoints.")

    user = st.session_state.get("user", {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style='background: white; padding: 1.25rem; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03); margin-bottom: 1rem;'>
                <h3 style='font-size: 1.15rem; font-weight: 800; color: #0f172a; margin: 0 0 0.85rem 0; font-family: Outfit, sans-serif;'>User Profile & Workspace Role</h3>
        """, unsafe_allow_html=True)
        st.text_input("Full Name", value=user.get("name", "Aditya Kulkarni"), disabled=True)
        st.text_input("Email Address", value=user.get("email", "aditya@salespulse.ai"), disabled=True)
        
        current_role = user.get("role", "Sales Representative")
        new_role = st.selectbox(
            "Active Workspace Role Scoping",
            ["Sales Representative", "Sales Manager", "VP of Sales / Admin"],
            index=["Sales Representative", "Sales Manager", "VP of Sales / Admin"].index(current_role) if current_role in ["Sales Representative", "Sales Manager", "VP of Sales / Admin"] else 0
        )

        if st.button("Update Workspace Role"):
            st.session_state["user"]["role"] = new_role
            st.success(f"Workspace role updated to '{new_role}'. Sidebar navigation updated.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='background: white; padding: 1.25rem; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03); margin-bottom: 1rem;'>
                <h3 style='font-size: 1.15rem; font-weight: 800; color: #0f172a; margin: 0 0 0.85rem 0; font-family: Outfit, sans-serif;'>Backend Infrastructure Status</h3>
        """, unsafe_allow_html=True)
        backend_online = check_backend_status()

        if backend_online:
            st.success("🟢 Node.js Backend: Connected (http://localhost:5000)")
        else:
            st.info("🟡 Node.js Backend: Offline (Running in Standalone Demo Mode with local analytics engine)")

        st.text_input("Node.js Backend URL", value=NODE_BACKEND_URL)
        st.text_input("FastAPI AI Service URL", value=FASTAPI_AI_URL)

        if st.button("Sign Out"):
            st.session_state["authenticated"] = False
            st.session_state["user"] = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
