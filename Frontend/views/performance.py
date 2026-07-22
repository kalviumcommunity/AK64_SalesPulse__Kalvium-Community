"""
Sales Performance View for SalesPulse AI Streamlit Frontend.
Displays high-level KPIs, revenue trend charts, activity breakdowns, and top performers.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from Frontend.utils.api import get_performance_summary
from Frontend.utils.components import render_stat_card, render_badge, render_section_header

def render_performance_view():
    render_section_header("Sales Performance", "Individual contribution overview and sales velocity metrics.")

    header_col1, header_col2 = st.columns([3, 1])
    with header_col2:
        date_range = st.selectbox("Date Range Filter", ["Last 7 Days", "Last 30 Days", "Quarter to Date", "Year to Date"], index=1)

    perf_data = get_performance_summary(date_range)

    # Metric Row using Rich StatCards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        render_stat_card("Today's Achievement", perf_data["today_achievement"], perf_data["today_comparison"], "📈", "indigo")
    with kpi2:
        render_stat_card("Win Rate (MTD)", perf_data["win_rate_mtd"], perf_data["win_rate_helper"], "🏆", "emerald")
    with kpi3:
        render_stat_card("Avg Cycle Time", perf_data["avg_cycle_time"], perf_data["cycle_time_helper"], "⏱️", "cyan")
    with kpi4:
        render_stat_card("Active Reps", perf_data["active_reps"], "2 reps on leave", "👥", "amber")

    # Chart Section
    chart_col1, chart_col2 = st.columns([2, 1])

    with chart_col1:
        st.markdown("""
            <div style='background: white; padding: 1.25rem 1.4rem 0.5rem 1.4rem; border: 1px solid #e2e8f0; border-radius: 16px; margin-bottom: 0.5rem; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0; font-family: Outfit, sans-serif;'>Revenue Trend vs Target</h3>
                <p style='font-size: 0.82rem; color: #64748b; margin: 3px 0 0 0;'>Monthly closed sales performance compared against target quota.</p>
            </div>
        """, unsafe_allow_html=True)

        df_rev = perf_data["revenue_trend"]
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Scatter(
            x=df_rev["Month"], y=df_rev["Sales ($)"],
            mode='lines+markers',
            name='Closed Sales ($)',
            line=dict(color='#6366f1', width=3.5, shape='spline'),
            marker=dict(size=8, color='#4f46e5', line=dict(width=2, color='#ffffff')),
            fill='tozeroy',
            fillcolor='rgba(99, 102, 241, 0.12)'
        ))
        fig_rev.add_trace(go.Scatter(
            x=df_rev["Month"], y=df_rev["Target ($)"],
            mode='lines',
            name='Monthly Target ($)',
            line=dict(color='#94a3b8', width=2, dash='dash')
        ))
        fig_rev.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=15, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            template="plotly_white",
            font=dict(family="Inter")
        )
        st.plotly_chart(fig_rev, use_container_width=True)

    with chart_col2:
        st.markdown("""
            <div style='background: white; padding: 1.25rem 1.4rem 0.5rem 1.4rem; border: 1px solid #e2e8f0; border-radius: 16px; margin-bottom: 0.5rem; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0; font-family: Outfit, sans-serif;'>Touchpoints by Channel</h3>
                <p style='font-size: 0.82rem; color: #64748b; margin: 3px 0 0 0;'>Distribution of sales engagement activities.</p>
            </div>
        """, unsafe_allow_html=True)

        df_channel = perf_data["channel_data"]
        fig_chan = px.bar(
            df_channel,
            x="Touchpoints",
            y="Channel",
            orientation='h',
            color_discrete_sequence=['#4f46e5'],
            text_auto=True
        )
        fig_chan.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=15, b=20),
            template="plotly_white",
            font=dict(family="Inter")
        )
        st.plotly_chart(fig_chan, use_container_width=True)

    # Bottom Row: Performance Insights & Leaderboard
    bottom_col1, bottom_col2 = st.columns([1, 2])

    with bottom_col1:
        st.markdown("""
            <div style='background: white; padding: 1.25rem; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0 0 0.85rem 0; font-family: Outfit, sans-serif;'>Performance Insights</h3>
        """, unsafe_allow_html=True)

        for item in perf_data["insights"]:
            tone_key = "emerald" if item["type"] == "success" else ("indigo" if item["type"] == "info" else "amber")
            badge_html = render_badge(item['tag'], tone_key)
            st.markdown(f"""
                <div style='border: 1px solid #e2e8f0; padding: 0.85rem; border-radius: 12px; margin-bottom: 0.85rem; background: #fafafa;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <strong style='color: #0f172a; font-size: 0.92rem; font-family: Outfit, sans-serif;'>{item['label']}</strong>
                        {badge_html}
                    </div>
                    <p style='color: #475569; font-size: 0.82rem; margin-top: 0.4rem; margin-bottom: 0;'>{item['note']}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with bottom_col2:
        st.markdown("""
            <div style='background: white; padding: 1.25rem; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0 0 0.85rem 0; font-family: Outfit, sans-serif;'>Top Performers</h3>
        """, unsafe_allow_html=True)
        df_top = perf_data["top_performers"]
        st.dataframe(
            df_top,
            column_config={
                "Quota Attainment": st.column_config.ProgressColumn(
                    "Quota Attainment",
                    help="Target completion percentage",
                    format="%s",
                    min_value=0,
                    max_value=150,
                ),
            },
            hide_index=True,
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
