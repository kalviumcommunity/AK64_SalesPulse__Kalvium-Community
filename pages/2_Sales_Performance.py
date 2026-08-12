"""
SalesPulse — Sales Performance
View 2: KPI summary left + revenue trend chart right → segment breakdown table.
"""

import streamlit as st
import plotly.graph_objects as go
from components.styles import inject_custom_css
from components.sidebar import render_sidebar
from components.header import render_top_bar
from components.ui_components import metric_card, data_table
from database_manager import fetch_sales_performance

st.set_page_config(page_title="Sales Performance | SalesPulse AI", layout="wide", page_icon="⚡")

inject_custom_css()
render_sidebar("Sales Performance")
render_top_bar("Sales Performance", "Monthly revenue trajectory, quota attainment & segment breakdown")

start_date, end_date = st.session_state.get("date_range", (None, None))
segment = st.session_state.get("selected_segment", "All Segments")
metrics, df_trend, df_table = fetch_sales_performance(start_date, end_date, segment)

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1: metric_card("Total Revenue YTD",   metrics["total_revenue"],    metrics["yoy_growth"], "positive", "blue")
with k2: metric_card("Quota Attainment",    metrics["quota_attainment"], "+2.1 pts",            "positive", "green")
with k3: metric_card("Avg Deal Size (AOV)", metrics["avg_deal_size"],    "+4.5%",               "positive", "amber")
with k4: metric_card("YoY Growth Rate",     metrics["yoy_growth"],       "+3.4 pts",            "positive", "purple")

# ── Top Section ───────────────────────────────────────────────────────────────
col_left, col_right = st.columns([0.38, 0.62], gap="medium")

with col_left:
    st.markdown('<div class="sp-card">', unsafe_allow_html=True)
    st.markdown('<div class="sp-card-title">📈 Performance Summary</div>', unsafe_allow_html=True)

    items = [
        ("Revenue vs Target", metrics["total_revenue"], "$2.4M target", "blue"),
        ("Quota Attainment",  metrics["quota_attainment"], "Company avg: 87%", "green"),
        ("Avg Deal Size",     metrics["avg_deal_size"],    "vs $18K last year", "amber"),
        ("YoY Growth",        metrics["yoy_growth"],       "Industry avg: 12%", "purple"),
    ]
    for label, val, note, _ in items:
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:10px 0;border-bottom:1px solid #F1F5F9;">
            <div>
                <div style="font-size:13px;font-weight:600;color:#1E293B;">{label}</div>
                <div style="font-size:11px;color:#94A3B8;margin-top:2px;">{note}</div>
            </div>
            <div style="font-size:16px;font-weight:800;color:#2563EB;">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="sp-card">', unsafe_allow_html=True)
    st.markdown('<div class="sp-card-title">📊 Monthly Revenue Trajectory vs Target</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_trend["Month"], y=df_trend["Revenue"],
        mode="lines+markers", name="Actual Revenue",
        line=dict(color="#2563EB", width=2.5),
        marker=dict(size=5, color="#2563EB"),
        fill="tozeroy", fillcolor="rgba(37,99,235,0.07)"
    ))
    fig.add_trace(go.Scatter(
        x=df_trend["Month"], y=df_trend["Target"],
        mode="lines", name="Target",
        line=dict(color="#94A3B8", width=1.5, dash="dot")
    ))
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=260,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#94A3B8")),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=11, color="#94A3B8"), zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=11, color="#64748B")),
        font=dict(family="Inter, sans-serif")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Bottom: Segment Table ─────────────────────────────────────────────────────
st.markdown('<div class="sp-card">', unsafe_allow_html=True)
st.markdown('<div class="sp-card-title">🏢 Segment & Product Performance Breakdown</div>', unsafe_allow_html=True)

df_disp = df_table.copy()
df_disp["status_tag"] = df_disp["status"].apply(
    lambda s: "success" if s in ["Strong Growth", "High Margin"]
              else ("info" if s == "On Target" else "danger")
)
data_table(
    df_disp[["segment", "deals_closed", "revenue", "aov", "win_rate", "growth", "status"]],
    tag_column="status", tag_type_column="status_tag"
)
st.markdown('</div>', unsafe_allow_html=True)
