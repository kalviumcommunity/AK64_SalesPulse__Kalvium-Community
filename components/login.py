"""
SalesPulse AI — Premium Login & Authentication Portal
------------------------------------------------------
PRD v1.0.0 compliant: FR-01 (Registration), FR-02 (JWT Auth),
FR-03 (Role-Based Access), FR-04 (Session Management).
Features:
  - Full-bleed hero banner with gradient + animated badges
  - Persona quick-access cards with hover effects
  - Clean JWT email/password form
  - Account registration form
  - JWT token inspector
"""

import streamlit as st
from auth_manager import authenticate_user, register_new_user


def _persona_card(emoji, role_label, name, description):
    """Returns HTML for a styled persona card."""
    return f"""
    <div class="sp-persona-card">
        <span class="sp-persona-emoji">{emoji}</span>
        <div class="sp-persona-role">{role_label}</div>
        <div class="sp-persona-name">{name}</div>
        <div class="sp-persona-desc">{description}</div>
    </div>
    """


def _do_login(email, password, label):
    ok, res = authenticate_user(email, password)
    if ok:
        st.session_state["user"] = res
        st.session_state["jwt_token"] = res["token"]
        st.toast(f"✅ Logged in as {res['name']} · {label}", icon="⚡")
        st.rerun()
    else:
        st.error(f"❌ {res}")


def render_login_page():
    """Renders the full-screen SalesPulse premium login portal."""

    # ── Hero Banner ────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="sp-login-hero">
        <div style="position: relative; z-index: 1;">
            <div style="
                width: 72px; height: 72px;
                background: rgba(255,255,255,0.2);
                border: 2px solid rgba(255,255,255,0.4);
                border-radius: 50%;
                display: inline-flex; align-items: center; justify-content: center;
                font-size: 36px; margin-bottom: 20px;
                backdrop-filter: blur(8px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            ">⚡</div>
            <h1 style="
                font-size: 40px; font-weight: 800; color: white;
                margin: 0 0 8px 0; letter-spacing: -1px;
            ">SalesPulse <span style="color: #93C5FD;">AI</span></h1>
            <p style="font-size: 16px; color: rgba(255,255,255,0.75); margin: 0 0 24px 0; font-weight: 400;">
                AI-Powered Sales Behaviour Intelligence Platform for B2B Organizations
            </p>
            <div>
                <span class="sp-hero-badge">🧠 ML Deal Scoring</span>
                <span class="sp-hero-badge">📧 Email NLP</span>
                <span class="sp-hero-badge">📊 Behaviour Analytics</span>
                <span class="sp-hero-badge">🤖 AI Coaching</span>
                <span class="sp-hero-badge">🔐 JWT Auth</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────────────────
    tab_personas, tab_login, tab_register = st.tabs([
        "⚡ Quick Access — Personas",
        "🔐 Sign In",
        "📝 Create Account",
    ])

    # ── Tab 1: Persona Quick-Access ────────────────────────────────────────────
    with tab_personas:
        st.markdown("""
        <div style="text-align: center; padding: 8px 0 24px 0;">
            <p style="font-size: 15px; color: #475569; font-weight: 500; margin: 0;">
                Choose a PRD persona to instantly access its authenticated dashboard view
            </p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4, gap="medium")

        with c1:
            st.markdown(_persona_card(
                "👩‍💼", "Sales Rep",
                "Aditya Kulkarni",
                "Understand what to do differently to close deals faster with targeted AI coaching tips."
            ), unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("Enter as Sales Rep", type="primary", use_container_width=True, key="btn_p1"):
                _do_login("aditya@salespulse.ai", "password123", "Sales Rep")

        with c2:
            st.markdown(_persona_card(
                "👩‍💻", "Sales Manager",
                "Meera Nair",
                "Identify which reps and behaviours are blocking deal closures and assign coaching."
            ), unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("Enter as Sales Manager", type="primary", use_container_width=True, key="btn_p2"):
                _do_login("meera@salespulse.ai", "password123", "Sales Manager")

        with c3:
            st.markdown(_persona_card(
                "👔", "VP of Sales",
                "Rohan Bhatt",
                "High-level executive view of team performance, pipeline health and revenue trends."
            ), unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("Enter as VP of Sales", type="primary", use_container_width=True, key="btn_p3"):
                _do_login("rohan@salespulse.ai", "password123", "VP of Sales")

        with c4:
            st.markdown(_persona_card(
                "⚙️", "RevOps Analyst",
                "Ishita Ghosh",
                "Ensure CRM & email data is clean, structured and reliably feeding ML pipelines."
            ), unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("Enter as RevOps Analyst", type="primary", use_container_width=True, key="btn_p4"):
                _do_login("ishita@salespulse.ai", "password123", "RevOps Analyst")

        # Feature highlights strip
        st.markdown("""
        <div style="
            margin-top: 32px;
            padding: 20px 28px;
            background: linear-gradient(135deg, #EFF6FF, #F0FDF4);
            border: 1px solid #BFDBFE;
            border-radius: 14px;
            display: flex;
            justify-content: space-around;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        ">
            <div style="text-align:center;">
                <div style="font-size:28px;font-weight:800;color:#1D4ED8">4</div>
                <div style="font-size:12px;color:#64748B;font-weight:500">PRD Personas</div>
            </div>
            <div style="width:1px;height:40px;background:#E2E8F0;"></div>
            <div style="text-align:center;">
                <div style="font-size:28px;font-weight:800;color:#1D4ED8">6</div>
                <div style="font-size:12px;color:#64748B;font-weight:500">Backend Modules</div>
            </div>
            <div style="width:1px;height:40px;background:#E2E8F0;"></div>
            <div style="text-align:center;">
                <div style="font-size:28px;font-weight:800;color:#16A34A">5</div>
                <div style="font-size:12px;color:#64748B;font-weight:500">Dashboard Views</div>
            </div>
            <div style="width:1px;height:40px;background:#E2E8F0;"></div>
            <div style="text-align:center;">
                <div style="font-size:28px;font-weight:800;color:#7C3AED">JWT</div>
                <div style="font-size:12px;color:#64748B;font-weight:500">Secured Sessions</div>
            </div>
            <div style="width:1px;height:40px;background:#E2E8F0;"></div>
            <div style="text-align:center;">
                <div style="font-size:28px;font-weight:800;color:#DC2626">ML</div>
                <div style="font-size:12px;color:#64748B;font-weight:500">Deal Predictor</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tab 2: Email / Password Login ──────────────────────────────────────────
    with tab_login:
        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 1.6, 1])
        with col:
            st.markdown("""
            <div style="
                background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px;
                padding: 36px 36px 28px 36px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.07);
            ">
                <div style="text-align:center; margin-bottom: 24px;">
                    <div style="
                        width: 52px; height: 52px; background: linear-gradient(135deg, #2563EB, #1D4ED8);
                        border-radius: 50%; display: inline-flex; align-items: center;
                        justify-content: center; font-size: 24px; margin-bottom: 12px;
                        box-shadow: 0 4px 14px rgba(37,99,235,0.3);
                    ">🔐</div>
                    <h2 style="font-size:22px; font-weight:700; color:#0F172A; margin:0 0 4px 0;">Welcome back</h2>
                    <p style="font-size:13px; color:#64748B; margin:0;">Sign in with your SalesPulse account</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.form("jwt_login_form"):
                email = st.text_input("📧 Work Email", value="aditya@salespulse.ai", placeholder="you@company.com")
                password = st.text_input("🔒 Password", type="password", value="password123", placeholder="••••••••")
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    submit = st.form_submit_button("Sign In →", type="primary", use_container_width=True)
                with col_b:
                    st.form_submit_button("Cancel", use_container_width=True)

                if submit:
                    if not email or not password:
                        st.error("Please fill in all fields.")
                    else:
                        ok, res = authenticate_user(email, password)
                        if ok:
                            st.session_state["user"] = res
                            st.session_state["jwt_token"] = res["token"]
                            st.toast(f"✅ Authenticated as {res['name']}", icon="⚡")
                            st.rerun()
                        else:
                            st.error(f"❌ {res}")

            st.markdown("""
            <div style="text-align:center; margin-top: 16px;">
                <p style="font-size: 12px; color: #94A3B8;">
                    🔐 Secured with JWT · SHA-256 password hashing · PRD v1.0.0
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 3: Registration ─────────────────────────────────────────────────────
    with tab_register:
        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 1.6, 1])
        with col:
            st.markdown("""
            <div style="
                background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px;
                padding: 36px 36px 28px 36px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.07);
            ">
                <div style="text-align:center; margin-bottom: 24px;">
                    <div style="
                        width: 52px; height: 52px; background: linear-gradient(135deg, #16A34A, #15803D);
                        border-radius: 50%; display: inline-flex; align-items: center;
                        justify-content: center; font-size: 24px; margin-bottom: 12px;
                        box-shadow: 0 4px 14px rgba(22,163,74,0.3);
                    ">📝</div>
                    <h2 style="font-size:22px; font-weight:700; color:#0F172A; margin:0 0 4px 0;">Create Account</h2>
                    <p style="font-size:13px; color:#64748B; margin:0;">Register for SalesPulse AI access (FR-01)</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.form("prd_register_form"):
                name = st.text_input("👤 Full Name", placeholder="e.g. Aditya Kulkarni")
                reg_email = st.text_input("📧 Work Email", placeholder="you@company.com")
                reg_password = st.text_input("🔒 Create Password", type="password", placeholder="Min 8 characters")
                role_sel = st.selectbox(
                    "🎯 Role Assignment (FR-03)",
                    ["Sales Representative (rep)", "Sales Team Manager (manager)", "VP / RevOps (admin)"]
                )
                reg_submit = st.form_submit_button("Create Account & Sign In →", type="primary", use_container_width=True)

                if reg_submit:
                    if not name or not reg_email or not reg_password:
                        st.error("All fields are required.")
                    elif len(reg_password) < 6:
                        st.warning("Password should be at least 6 characters.")
                    else:
                        role_code = (
                            "rep" if "Representative" in role_sel
                            else "manager" if "Manager" in role_sel
                            else "admin"
                        )
                        ok, res = register_new_user(name, reg_email, reg_password, role_code)
                        if ok:
                            st.session_state["user"] = res
                            st.session_state["jwt_token"] = res["token"]
                            st.toast(f"🎉 Welcome, {name}! Account created.", icon="✅")
                            st.rerun()
                        else:
                            st.error(f"❌ {res}")


