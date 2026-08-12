"""
SalesPulse Page Top Bar
------------------------
Renders the page title strip + date/segment filter controls.
No user/login/session-user logic.
"""

import streamlit as st
from datetime import date


def render_top_bar(page_title: str, subtitle: str = "Real-time AI-powered sales intelligence"):
    col_title, col_controls = st.columns([0.5, 0.5])

    with col_title:
        st.markdown(f"""
        <div style="padding: 4px 0 0 0;">
            <h1 class="sp-page-title">{page_title}</h1>
            <div class="sp-page-sub">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_controls:
        fc1, fc2 = st.columns([0.5, 0.5])

        with fc1:
            if "date_range" not in st.session_state:
                st.session_state["date_range"] = (date(2024, 1, 1), date(2024, 12, 31))
            selected_dates = st.date_input(
                "Date Range",
                value=st.session_state["date_range"],
                key="header_date_picker",
                label_visibility="collapsed"
            )
            if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
                st.session_state["date_range"] = selected_dates

        with fc2:
            if "selected_segment" not in st.session_state:
                st.session_state["selected_segment"] = "All Segments"
            segments = ["All Segments", "Enterprise", "Mid-Market", "SMB Core", "Custom Services"]
            sel = st.selectbox(
                "Segment",
                options=segments,
                index=segments.index(st.session_state["selected_segment"])
                      if st.session_state["selected_segment"] in segments else 0,
                key="header_segment_select",
                label_visibility="collapsed"
            )
            st.session_state["selected_segment"] = sel

    st.markdown('<hr class="sp-hr">', unsafe_allow_html=True)
