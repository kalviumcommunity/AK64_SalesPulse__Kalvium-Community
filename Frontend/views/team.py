"""
Team Performance View for SalesPulse AI Streamlit Frontend.
Manager-facing dashboard with quota attainment progress, leaderboards, and coaching queue.
"""

import streamlit as st
import plotly.express as px
from Frontend.utils.api import get_team_performance
from Frontend.utils.components import render_stat_card, render_section_header

def render_team_view():
    render_section_header("Team Performance", "Manager view for team quota tracking, leaderboard rankings, and flagged coaching queue.")

    team_data = get_team_performance()

    m1, m2, m3 = st.columns(3)
    with m1:
        render_stat_card("Active Team", team_data["team_name"], "Enterprise B2B Segment", "👥", "indigo")
    with m2:
        render_stat_card("Team Quota Attainment", team_data["overall_attainment"], "+$32k vs quota plan", "🎯", "emerald")
    with m3:
        render_stat_card("Revenue Closed", team_data["total_achieved"], f"Target Plan: {team_data['total_quota']}", "💰", "cyan")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
            <div style='background: white; padding: 1.25rem 1.4rem 0.5rem 1.4rem; border: 1px solid #e2e8f0; border-radius: 16px; margin-bottom: 0.5rem; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0; font-family: Outfit, sans-serif;'>Team Quota Attainment Leaderboard</h3>
                <p style='font-size: 0.82rem; color: #64748b; margin: 3px 0 0 0;'>Quota attainment percentage per account executive.</p>
            </div>
        """, unsafe_allow_html=True)

        df_quota = team_data["quota_df"]
        fig_bar = px.bar(
            df_quota,
            x="Attainment (%)",
            y="Rep",
            orientation='h',
            color="Attainment (%)",
            color_continuous_scale=["#f43f5e", "#f59e0b", "#10b981"],
            text_auto='.1f'
        )
        fig_bar.add_vline(x=100, line_dash="dash", line_color="#64748b", annotation_text="100% Quota Target")
        fig_bar.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=15, b=20),
            coloraxis_showscale=False,
            template="plotly_white",
            font=dict(family="Inter")
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown("""
            <div style='background: white; padding: 1.25rem; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0 0 0.25rem 0; font-family: Outfit, sans-serif;'>🚨 Manager Coaching Queue</h3>
                <p style='font-size: 0.82rem; color: #64748b; margin-bottom: 0.85rem;'>AI-flagged reps needing immediate coaching attention.</p>
        """, unsafe_allow_html=True)

        for item in team_data["coaching_queue"]:
            badge_color = "linear-gradient(135deg, #ef4444, #dc2626)" if item["severity"] == "High" else "linear-gradient(135deg, #f97316, #ea580c)"
            st.markdown(f"""
                <div style='background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 0.95rem; margin-bottom: 0.85rem;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <strong style='color: #0f172a; font-family: Outfit, sans-serif; font-size: 0.95rem;'>{item['rep']}</strong>
                        <span style='background: {badge_color}; color: white; padding: 3px 10px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700;'>{item['severity']} Priority</span>
                    </div>
                    <p style='color: #475569; font-size: 0.83rem; margin-top: 0.45rem; margin-bottom: 0.45rem;'>⚠️ {item['issue']}</p>
                    <div style='font-size: 0.82rem; color: #4f46e5; font-weight: 700;'>👉 Suggested Action: {item['action']}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
