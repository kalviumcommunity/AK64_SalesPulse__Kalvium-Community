"""
SalesPulse — Pipeline Analytics
View 1: KPI row → funnel chart left + active deals table right → AI recommendations feed.
"""

import streamlit as st
import plotly.graph_objects as go
from components.styles import inject_custom_css
from components.header import render_top_bar
from components.ui_components import metric_card, status_tag, data_table, insight_feed_row
from database_manager import fetch_pipeline_data
from deal_predictor import get_all_active_deal_predictions

st.set_page_config(page_title="Pipeline Analytics | SalesPulse AI", layout="wide")
inject_custom_css()
render_top_bar("Pipeline Analytics", "Live funnel tracking with ML-powered closing probability scores")

start_date, end_date = st.session_state.get("date_range", (None, None))
segment = st.session_state.get("selected_segment", "All Segments")
df_stages, _, insights = fetch_pipeline_data(start_date, end_date, segment)
df_preds = get_all_active_deal_predictions()

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1: metric_card("Total Pipeline Value",    "$1,407,000", "+12.4% vs last period", "positive", "blue")
with k2: metric_card("Active Deals in Funnel",  "371 Deals",  "+8 new deals",          "positive", "green")
with k3: metric_card("ML Avg Win Probability",  "68.4%",      "+4.2 pts",              "positive", "purple")
with k4: metric_card("Stage Conversion Rate",   "64.8%",      "+3.2 pts",              "positive", "amber")

# ── Main: Funnel Left + Deals Table Right ────────────────────────────────────
col_left, col_right = st.columns([0.44, 0.56], gap="medium")

with col_left:
    st.markdown('<div class="sp-card">', unsafe_allow_html=True)
    st.markdown('<div class="sp-card-title">📊 Pipeline Stage Breakdown</div>', unsafe_allow_html=True)

    fig = go.Figure(go.Funnel(
        y=df_stages["stage"],
        x=df_stages["value"],
        textinfo="value+percent initial",
        textfont=dict(size=12, color="#1E293B"),
        marker=dict(
            color=["#1D4ED8", "#2563EB", "#3B82F6", "#60A5FA", "#10B981"],
            line=dict(width=0)
        ),
        connector=dict(line=dict(color="#E2E8F0", width=1))
    ))
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=310,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#64748B", size=12),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="sp-card">', unsafe_allow_html=True)
    st.markdown('<div class="sp-card-title">🎯 Active Deals & ML Closing Probabilities</div>', unsafe_allow_html=True)

    disp = df_preds[["deal_id", "account", "owner", "stage", "value", "closing_probability", "tag"]].copy()
    data_table(disp, tag_column="tag", tag_type_column="tag_type")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Bottom: AI Recommendations ────────────────────────────────────────────────
st.markdown('<div class="sp-card">', unsafe_allow_html=True)
st.markdown('<div class="sp-card-title">💡 AI Pipeline Recommendations & Risk Flags</div>', unsafe_allow_html=True)

for item in insights:
    dot = "red" if item.get("tag_type") == "danger" else (
          "amber" if item.get("tag_type") == "warning" else "green")
    insight_feed_row(
        title=item["title"],
        description=item["desc"],
        category=item.get("category"),
        tag=item["tag"],
        tag_type=item["tag_type"],
        dot_color=dot
    )

st.markdown('</div>', unsafe_allow_html=True)
