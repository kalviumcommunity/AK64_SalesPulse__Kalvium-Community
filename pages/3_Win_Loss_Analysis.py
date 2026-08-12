"""
SalesPulse — Win/Loss Analysis
View 3: KPI row → donut chart left + reason cards right → deal log table bottom.
"""

import streamlit as st
import plotly.graph_objects as go
from components.styles import inject_custom_css
from components.sidebar import render_sidebar
from components.header import render_top_bar
from components.ui_components import metric_card, data_table, reason_card
from database_manager import fetch_win_loss_data

st.set_page_config(page_title="Win/Loss Analysis | SalesPulse AI", layout="wide", page_icon="⚡")

inject_custom_css()
render_sidebar("Win/Loss Analysis")
render_top_bar("Win/Loss Analysis", "Deal outcome distribution, competitive win rates & driver ranking")

start_date, end_date = st.session_state.get("date_range", (None, None))
segment = st.session_state.get("selected_segment", "All Segments")
chart_data, win_drivers, deals_table = fetch_win_loss_data(start_date, end_date, segment)

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1: metric_card("Overall Win Rate",        "51.3%",      "+4.1 pts",  "positive", "green")
with k2: metric_card("Competitive Win Rate",    "67.6%",      "+6.2 pts",  "positive", "blue")
with k3: metric_card("Avg Sales Cycle (Won)",   "31.2 Days",  "-4.0 days", "positive", "amber")
with k4: metric_card("No-Decision Loss Rate",   "16.2%",      "-2.5 pts",  "positive", "purple")

# ── Chart Left + Reason Cards Right ──────────────────────────────────────────
col_left, col_right = st.columns([0.44, 0.56], gap="medium")

with col_left:
    st.markdown('<div class="sp-card">', unsafe_allow_html=True)
    st.markdown('<div class="sp-card-title">🥧 Deal Outcome Distribution</div>', unsafe_allow_html=True)

    fig = go.Figure(go.Pie(
        labels=chart_data["Category"],
        values=chart_data["Count"],
        hole=0.52,
        marker=dict(
            colors=["#10B981", "#EF4444", "#F59E0B", "#94A3B8"],
            line=dict(color="#FFFFFF", width=2)
        ),
        textinfo="label+percent",
        textfont=dict(size=11, color="#1E293B"),
        hovertemplate="%{label}: %{value} deals<br>%{percent}<extra></extra>"
    ))
    # Center annotation
    total = chart_data["Count"].sum()
    fig.update_layout(
        margin=dict(l=10, r=10, t=20, b=20),
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5,
                    font=dict(size=11, color="#64748B")),
        annotations=[dict(text=f"<b>{total}</b><br><span style='font-size:10px'>Deals</span>",
                          x=0.5, y=0.5, font=dict(size=14, color="#1E293B"), showarrow=False)]
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="sp-card">', unsafe_allow_html=True)
    st.markdown('<div class="sp-card-title">🏆 Key Win & Loss Drivers</div>', unsafe_allow_html=True)

    for item in win_drivers:
        ctype = "win" if item.get("tag_type") in ["success", "info"] else (
                "loss" if item.get("tag_type") == "danger" else "neutral")
        impact = item.get("impact", "+12%").replace("+", "").replace("-", "").replace("%", "")
        try:
            pct = float(impact)
        except ValueError:
            pct = 0
        reason_card(item["rank"], item["driver"], int(pct), ctype)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Bottom: Deal Log Table ────────────────────────────────────────────────────
st.markdown('<div class="sp-card">', unsafe_allow_html=True)
st.markdown('<div class="sp-card-title">🔍 Deal Win/Loss Retrospective Log</div>', unsafe_allow_html=True)

data_table(
    deals_table[["deal", "value", "outcome", "competitor", "primary_reason", "cycle_days", "tag"]],
    tag_column="tag", tag_type_column="tag_type"
)
st.markdown('</div>', unsafe_allow_html=True)
