"""
High-End UI Design System and Component Renderers for SalesPulse AI Streamlit Frontend.
Provides glassmorphic cards, gradient KPI badges, styled tables, and interactive navbar elements.
"""

import streamlit as st

def render_top_navbar():
    """Renders a top header navbar with glassmorphism, search bar, status indicator, and user profile."""
    user = st.session_state.get("user", {})
    name = user.get("name", "Aditya Kulkarni")
    role = user.get("role", "Sales Representative")
    initials = "".join([n[0] for n in name.split()]).upper()[:2] if name else "SP"

    st.markdown(f"""
        <div style='
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid #e2e8f0;
            padding: 0.85rem 1.6rem;
            margin-bottom: 1.8rem;
            border-radius: 16px;
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
        '>
            <!-- Left: Brand & Search Bar -->
            <div style='display: flex; align-items: center; gap: 1.5rem;'>
                <div style='display: flex; align-items: center; gap: 0.6rem;'>
                    <span style='
                        background: #10b981;
                        width: 8px;
                        height: 8px;
                        border-radius: 50%;
                        display: inline-block;
                        box-shadow: 0 0 10px #10b981;
                    '></span>
                    <span style='font-size: 0.8rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.5px;'>Live Intelligence Sync</span>
                </div>

                <div style='
                    background: #f1f5f9;
                    border: 1px solid #cbd5e1;
                    padding: 0.45rem 1rem;
                    border-radius: 12px;
                    font-size: 0.85rem;
                    color: #475569;
                    font-weight: 500;
                    display: flex;
                    align-items: center;
                    gap: 0.8rem;
                    min-width: 280px;
                '>
                    <span>🔍</span>
                    <span style='color: #94a3b8; flex-grow: 1;'>Search reps, deals, accounts...</span>
                    <span style='
                        background: #ffffff;
                        border: 1px solid #cbd5e1;
                        padding: 2px 7px;
                        border-radius: 6px;
                        font-size: 0.7rem;
                        color: #475569;
                        font-weight: 700;
                        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                    '>⌘K</span>
                </div>
            </div>

            <!-- Right: Role Pill & User Profile -->
            <div style='display: flex; align-items: center; gap: 1.2rem;'>
                <div style='
                    background: linear-gradient(135deg, #eff6ff, #dbeafe);
                    border: 1px solid #bfdbfe;
                    color: #1d4ed8;
                    padding: 0.35rem 0.85rem;
                    border-radius: 9999px;
                    font-size: 0.78rem;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    gap: 0.4rem;
                '>
                    <span>🛡️</span> {role}
                </div>

                <div style='height: 24px; width: 1px; background: #e2e8f0;'></div>

                <div style='display: flex; align-items: center; gap: 0.8rem;'>
                    <div style='text-align: right;'>
                        <div style='font-size: 0.92rem; font-weight: 800; color: #0f172a; line-height: 1.2; font-family: Outfit, sans-serif;'>{name}</div>
                        <div style='font-size: 0.75rem; color: #64748b; font-weight: 500;'>Enterprise Sales</div>
                    </div>
                    <div style='
                        width: 42px;
                        height: 42px;
                        background: linear-gradient(135deg, #6366f1, #4f46e5);
                        color: #ffffff;
                        font-weight: 800;
                        font-size: 1rem;
                        border-radius: 12px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
                        font-family: Outfit, sans-serif;
                    '>
                        {initials}
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_stat_card(title, value, helper="", icon="📈", tone="indigo"):
    """Renders a rich stat card with glowing gradient icon container and smooth typography."""
    color_map = {
        "indigo": {"bg": "linear-gradient(135deg, #6366f1, #4f46e5)", "shadow": "rgba(99, 102, 241, 0.25)", "text": "#4f46e5"},
        "emerald": {"bg": "linear-gradient(135deg, #10b981, #059669)", "shadow": "rgba(16, 185, 129, 0.25)", "text": "#059669"},
        "amber": {"bg": "linear-gradient(135deg, #f59e0b, #d97706)", "shadow": "rgba(245, 158, 11, 0.25)", "text": "#d97706"},
        "rose": {"bg": "linear-gradient(135deg, #f43f5e, #e11d48)", "shadow": "rgba(244, 63, 94, 0.25)", "text": "#e11d48"},
        "cyan": {"bg": "linear-gradient(135deg, #06b6d4, #0891b2)", "shadow": "rgba(6, 182, 212, 0.25)", "text": "#0891b2"},
    }
    c = color_map.get(tone, color_map["indigo"])

    st.markdown(f"""
        <div style='
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.35rem 1.4rem;
            box-shadow: 0 4px 15px -3px rgba(15, 23, 42, 0.04);
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        '>
            <div>
                <p style='color: #64748b; font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin: 0;'>{title}</p>
                <h2 style='color: #0f172a; font-size: 1.9rem; font-weight: 800; margin: 0.4rem 0 0.25rem 0; font-family: Outfit, sans-serif;'>{value}</h2>
                <p style='color: #64748b; font-size: 0.8rem; margin: 0; font-weight: 500;'>{helper}</p>
            </div>
            <div style='
                background: {c["bg"]};
                color: #ffffff;
                width: 44px;
                height: 44px;
                border-radius: 12px;
                font-size: 1.3rem;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 12px {c["shadow"]};
            '>
                {icon}
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_badge(text, tone="indigo"):
    """Renders a pill badge."""
    tones_css = {
        "indigo": "background: #eff6ff; color: #3b82f6; border: 1px solid #bfdbfe;",
        "emerald": "background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0;",
        "amber": "background: #fffbebf; color: #d97706; border: 1px solid #fde68a;",
        "rose": "background: #fff1f2; color: #e11d48; border: 1px solid #fecdd3;",
        "slate": "background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1;",
    }
    style = tones_css.get(tone, tones_css["indigo"])
    return f"<span style='{style} padding: 4px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; display: inline-block;'>{text}</span>"

def render_section_header(title, subtitle=""):
    """Renders a section header with Outfit typography."""
    st.markdown(f"""
        <div style='margin-bottom: 1.25rem;'>
            <h2 style='color: #0f172a; font-family: Outfit, sans-serif; font-weight: 800; font-size: 1.6rem; margin: 0;'>{title}</h2>
            {f"<p style='color: #64748b; font-size: 0.92rem; margin-top: 0.2rem;'>{subtitle}</p>" if subtitle else ""}
        </div>
    """, unsafe_allow_html=True)
