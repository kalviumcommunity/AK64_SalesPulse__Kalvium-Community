"""
Win/Loss Analysis View for SalesPulse AI Streamlit Frontend.
Provides historical win rate trends, loss reason breakdowns, and rep performance matrices.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from Frontend.utils.api import get_win_loss_summary
from Frontend.utils.components import render_stat_card, render_section_header

def render_win_loss_view():
    render_section_header("Win / Loss Analysis", "Historical conversion insights, win rate trends, and loss root-cause attribution.")

    date_range = st.selectbox("Period Selection", ["Last 30 Days", "Quarter to Date", "Last 6 Months", "Year to Date"], index=2, key="winloss_period")

    wl_data = get_win_loss_summary(date_range)

    m1, m2, m3 = st.columns(3)
    with m1:
        render_stat_card("Total Revenue Won", wl_data["total_won_value"], "+14% vs Q1 baseline", "🏆", "emerald")
    with m2:
        render_stat_card("Overall Win Rate", wl_data["overall_win_rate"], "+3.2% performance gain", "📈", "indigo")
    with m3:
        render_stat_card("Lost Revenue", wl_data["lost_revenue"], "-8% reduced deal loss", "📉", "rose")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
            <div style='background: white; padding: 1.25rem 1.4rem 0.5rem 1.4rem; border: 1px solid #e2e8f0; border-radius: 16px; margin-bottom: 0.5rem; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0; font-family: Outfit, sans-serif;'>Monthly Win / Loss Performance Trend</h3>
                <p style='font-size: 0.82rem; color: #64748b; margin: 3px 0 0 0;'>Deals won vs lost alongside overall win rate percentage.</p>
            </div>
        """, unsafe_allow_html=True)

        df_trend = wl_data["win_loss_trend"]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_trend["Month"], y=df_trend["Won"], name="Deals Won", marker_color="#10b981"))
        fig.add_trace(go.Bar(x=df_trend["Month"], y=df_trend["Lost"], name="Deals Lost", marker_color="#f43f5e"))
        fig.add_trace(go.Scatter(
            x=df_trend["Month"], y=df_trend["Win Rate (%)"],
            name="Win Rate (%)", yaxis="y2",
            mode="lines+markers", line=dict(color="#6366f1", width=3.5, shape='spline')
        ))

        fig.update_layout(
            barmode="group",
            height=340,
            margin=dict(l=10, r=10, t=15, b=20),
            yaxis=dict(title="Number of Deals"),
            yaxis2=dict(title="Win Rate (%)", overlaying="y", side="right", range=[0, 100]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            template="plotly_white",
            font=dict(family="Inter")
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""
            <div style='background: white; padding: 1.25rem 1.4rem 0.5rem 1.4rem; border: 1px solid #e2e8f0; border-radius: 16px; margin-bottom: 0.5rem; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0; font-family: Outfit, sans-serif;'>Primary Loss Reasons</h3>
                <p style='font-size: 0.82rem; color: #64748b; margin: 3px 0 0 0;'>Root cause loss distribution.</p>
            </div>
        """, unsafe_allow_html=True)

        df_reasons = wl_data["loss_reasons"]
        fig_pie = px.pie(
            df_reasons,
            values="Deals Lost",
            names="Reason",
            color_discrete_sequence=["#f43f5e", "#f97316", "#f59e0b", "#64748b"],
            hole=0.45
        )
        fig_pie.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=15, b=20),
            legend=dict(orientation="h", y=-0.15)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div style='background: white; padding: 1.25rem; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
            <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0 0 0.85rem 0; font-family: Outfit, sans-serif;'>Representative Conversion Matrix</h3>
    """, unsafe_allow_html=True)
    df_reps = wl_data["rep_win_rates"]
    st.dataframe(df_reps, hide_index=True, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
