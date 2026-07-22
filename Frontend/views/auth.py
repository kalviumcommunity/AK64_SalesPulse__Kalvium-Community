"""
Authentication View for SalesPulse AI Streamlit Frontend.
Provides user Login and Registration with role-based JWT session handling.
"""

import streamlit as st
from Frontend.utils.api import login_user, register_user

def render_auth_page():
    st.markdown("""
        <div style='text-align: center; padding-bottom: 2rem;'>
            <h1 style='color: #4f46e5; margin-bottom: 0.5rem;'>SalesPulse AI</h1>
            <p style='color: #64748b; font-size: 1.1rem;'>AI-Powered Sales Behaviour Intelligence Platform</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔒 Secure Login", "📝 Create Account"])

        with tab1:
            st.subheader("Welcome back")
            st.caption("Sign in with your SalesPulse credentials")

            email = st.text_input("Email Address", value="aditya@salespulse.ai", key="login_email")
            password = st.text_input("Password", value="••••••••", type="password", key="login_pass")
            role_select = st.selectbox(
                "Select Role / View Scoping",
                ["Sales Representative", "Sales Manager", "VP of Sales / Admin"],
                key="login_role_override"
            )

            if st.button("Sign In to SalesPulse", type="primary", use_container_width=True):
                if email and password:
                    res = login_user(email, password)
                    if res.get("success"):
                        st.session_state["authenticated"] = True
                        st.session_state["user"] = res.get("user", {
                            "name": email.split("@")[0].capitalize(),
                            "email": email,
                            "role": role_select,
                            "token": res.get("token")
                        })
                        st.session_state["user"]["role"] = role_select
                        st.success(f"Logged in successfully as {st.session_state['user']['name']}!")
                        st.rerun()
                    else:
                        st.error(res.get("message", "Invalid email or password."))
                else:
                    st.warning("Please enter your email and password.")

        with tab2:
            st.subheader("Register New Account")
            st.caption("Join your B2B sales team workspace")

            new_name = st.text_input("Full Name", placeholder="e.g. Meera Nair", key="reg_name")
            new_email = st.text_input("Work Email", placeholder="meera@company.com", key="reg_email")
            new_pass = st.text_input("Create Password", type="password", key="reg_pass")
            new_role = st.selectbox("Role", ["Sales Representative", "Sales Manager", "VP of Sales / Admin"], key="reg_role")

            if st.button("Create Account", type="primary", use_container_width=True):
                if new_name and new_email and new_pass:
                    res = register_user(new_name, new_email, new_pass, new_role)
                    if res.get("success"):
                        st.success(res.get("message"))
                        st.info("You can now switch to the 'Secure Login' tab to log in.")
                    else:
                        st.error(res.get("message", "Registration failed."))
                else:
                    st.warning("Please fill out all required fields.")
