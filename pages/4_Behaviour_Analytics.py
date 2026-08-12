"""
SalesPulse — Behaviour Analytics
View 4: KPI row → rep benchmark table → NLP activity telemetry log.
"""

import streamlit as st
import plotly.graph_objects as go
from components.styles import inject_custom_css
from components.sidebar import render_sidebar
from components.header import render_top_bar
from components.ui_components import metric_card, data_table
from database_manager import fetch_behaviour_data
from behaviour_analytics import compute_rep_behaviour_metrics

st.set_page_config(page_title="Behaviour Analytics | SalesPulse AI", layout="wide", page_icon="⚡")

inject_custom_css()
render_sidebar("Behaviour Analytics")
render_top_bar("Behaviour Analytics", "Rep response time, follow-up cadence, NLP email sentiment & performance scores")

df_rep = compute_rep_behaviour_metrics()
_, event_log = fetch_behaviour_data()

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1: metric_card("Avg Rep Response Time",     "3.4 Hours",  "-1.2 hrs",  "positive", "blue")
with k2: metric_card("Avg Follow-up Cadence",     "3.8 Days",   "-0.6 days", "positive", "green")
with k3: metric_card("Avg NLP Sentiment Score",   "+0.62",      "+0.15 pts", "positive", "amber")
with k4: metric_card("Top Rep Performance Score", "89.4 / 100", "+4.2 pts",  "positive", "purple")

# ── Rep Benchmark Chart ────────────────────────────────────────────────────────
col_chart, col_gauge = st.columns([0.65, 0.35], gap="medium")

with col_chart:
    with st.container(border=True):
        st.markdown('<div class="sp-card-title">📊 Rep Response Time vs Follow-Up Cadence</div>', unsafe_allow_html=True)

        if not df_rep.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Avg Response Time (hrs)",
                x=df_rep["name"],
                y=df_rep["avg_response_time"],
                marker_color="#3B82F6",
                marker_line_width=0,
            ))
            fig.add_trace(go.Bar(
                name="Follow-up Cadence (days)",
                x=df_rep["name"],
                y=df_rep["followup_frequency"],
                marker_color="#10B981",
                marker_line_width=0,
            ))
            fig.update_layout(
                barmode="group",
                margin=dict(l=10, r=10, t=10, b=10),
                height=240,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#94A3B8")),
                yaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=11, color="#94A3B8"), zeroline=False),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                            font=dict(size=11, color="#64748B")),
                font=dict(family="Inter, sans-serif"),
                bargap=0.3, bargroupgap=0.08
            )
            st.plotly_chart(fig, use_container_width=True)

with col_gauge:
    with st.container(border=True):
        st.markdown('<div class="sp-card-title">🎯 Team Avg Performance Score</div>', unsafe_allow_html=True)

        avg_score = df_rep["performance_score"].mean() if not df_rep.empty else 72.0
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_score,
            number=dict(suffix=" / 100", font=dict(size=22, color="#0F172A")),
            gauge=dict(
                axis=dict(range=[0, 100], tickwidth=1, tickcolor="#E2E8F0",
                          tickfont=dict(size=10, color="#94A3B8")),
                bar=dict(color="#2563EB", thickness=0.6),
                bgcolor="white",
                steps=[
                    dict(range=[0, 60],  color="#FEE2E2"),
                    dict(range=[60, 80], color="#FEF3C7"),
                    dict(range=[80, 100],color="#DCFCE7"),
                ],
                threshold=dict(line=dict(color="#2563EB", width=2), thickness=0.8, value=80)
            )
        ))
        fig2.update_layout(
            margin=dict(l=20, r=20, t=20, b=10),
            height=240,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig2, use_container_width=True)

# ── Rep Behaviour Table ───────────────────────────────────────────────────────
with st.container(border=True):
    st.markdown('<div class="sp-card-title">👥 Sales Rep Behavioural Analytics Summary</div>', unsafe_allow_html=True)

    df_disp = df_rep.copy()
    df_disp["status"] = df_disp["performance_score"].apply(
        lambda s: "Top Performer" if s >= 80 else ("Solid" if s >= 60 else "Needs Coaching"))
    df_disp["status_tag"] = df_disp["performance_score"].apply(
        lambda s: "success" if s >= 80 else ("info" if s >= 60 else "warning"))
    data_table(
        df_disp[["name", "win_rate", "avg_response_time_label", "followup_frequency_label",
                 "avg_closing_days", "performance_score", "status"]].rename(columns={
                     "avg_response_time_label": "avg_response_time",
                     "followup_frequency_label": "followup_frequency"
                 }),
        tag_column="status", tag_type_column="status_tag"
    )

# ── Activity Telemetry Log ────────────────────────────────────────────────────
with st.container(border=True):
    st.markdown('<div class="sp-card-title">⚡ Real-Time Customer Event & NLP Communication Telemetry</div>', unsafe_allow_html=True)

    data_table(
        event_log[["account", "user_email", "event", "timestamp", "usage_tier", "health_score", "status"]],
        tag_column="status", tag_type_column="tag_type"
    )
