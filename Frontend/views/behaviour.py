"""
Behaviour Analytics View for SalesPulse AI Streamlit Frontend.
Provides core behavioural analysis: response time latency, follow-up cadence, and email tone classification.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from Frontend.utils.api import get_behaviour_metrics
from Frontend.utils.components import render_stat_card, render_section_header

def render_behaviour_view():
    render_section_header("Behaviour Analytics", "Surface behavioural activity patterns: response latency, follow-up cadence, and email communication tone.")

    beh_data = get_behaviour_metrics()

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_stat_card("Team Avg Response", beh_data["team_avg_response_time"], "−0.6h faster vs last week", "⚡", "indigo")
    with m2:
        render_stat_card("Top Performer Goal", beh_data["top_performer_benchmark"], "Target benchmark: < 2.0h", "🎯", "emerald")
    with m3:
        render_stat_card("Follow-Up Cadence", beh_data["avg_follow_up_cadence"], "+0.4 touchpoints / week", "🔄", "cyan")
    with m4:
        render_stat_card("Tone Quality Index", beh_data["overall_tone_score"], "+5.2% positive sentiment", "💬", "amber")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
            <div style='background: white; padding: 1.25rem 1.4rem 0.5rem 1.4rem; border: 1px solid #e2e8f0; border-radius: 16px; margin-bottom: 0.5rem; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0; font-family: Outfit, sans-serif;'>Email Tone Classification (NLP)</h3>
                <p style='font-size: 0.82rem; color: #64748b; margin: 3px 0 0 0;'>Breakdown of communication sentiment across all deal interactions.</p>
            </div>
        """, unsafe_allow_html=True)

        df_tone = beh_data["tone_distribution"]
        fig_tone = px.bar(
            df_tone,
            x="Count",
            y="Tone",
            orientation='h',
            color="Tone",
            color_discrete_map={
                "Positive / Empathetic": "#10b981",
                "Neutral / Transactional": "#3b82f6",
                "Passive / Hesitant": "#f97316",
                "Assertive / Urgent": "#a855f7"
            },
            text_auto=True
        )
        fig_tone.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=15, b=20),
            showlegend=False,
            template="plotly_white",
            font=dict(family="Inter")
        )
        st.plotly_chart(fig_tone, use_container_width=True)

    with col2:
        st.markdown("""
            <div style='background: white; padding: 1.25rem 1.4rem 0.5rem 1.4rem; border: 1px solid #e2e8f0; border-radius: 16px; margin-bottom: 0.5rem; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0; font-family: Outfit, sans-serif;'>Response Time vs Close Rate Benchmark</h3>
                <p style='font-size: 0.82rem; color: #64748b; margin: 3px 0 0 0;'>Correlation between response latency and deal win rate.</p>
            </div>
        """, unsafe_allow_html=True)
        df_bm = beh_data["response_time_benchmarks"]
        st.dataframe(df_bm, hide_index=True, use_container_width=True)
        st.info("💡 Insight: Representatives who respond within 2 hours achieve a 74% close rate compared to 41% for reps averaging over 5 hours.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div style='background: white; padding: 1.25rem; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
            <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0 0 0.85rem 0; font-family: Outfit, sans-serif;'>Sales Representative Behaviour Scorecard</h3>
    """, unsafe_allow_html=True)

    df_scorecard = beh_data["rep_scorecards"]
    st.dataframe(
        df_scorecard,
        column_config={
            "Behaviour Score": st.column_config.ProgressColumn(
                "Composite Score (0-100)",
                help="Weighted score calculated from response time, follow-up cadence, and tone score",
                format="%d",
                min_value=0,
                max_value=100
            ),
            "Avg Response Time (hrs)": st.column_config.NumberColumn(
                "Avg Response Time (h)",
                format="%.1f hrs"
            ),
            "Positive Tone (%)": st.column_config.NumberColumn(
                "Positive Tone %",
                format="%d%%"
            ),
        },
        hide_index=True,
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
