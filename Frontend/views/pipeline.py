"""
Pipeline Analytics View for SalesPulse AI Streamlit Frontend.
Provides deal stage distribution funnel, deal risk status, and ML closing probabilities.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from Frontend.utils.api import get_pipeline_data
from Frontend.utils.components import render_stat_card, render_section_header

def render_pipeline_view():
    render_section_header("Pipeline Analytics", "Deal-level visibility into open pipeline stages and ML closing probabilities.")

    # Filter Bar
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        stage_filter = st.selectbox("Filter by Deal Stage", ["All", "Lead Qualification", "Discovery Call", "Proposal / Demo", "Negotiation", "Contract Sent"])
    with f_col2:
        rep_filter = st.selectbox("Filter by Sales Rep", ["All", "Sarah Jenkins", "Michael Chen", "Aditya Kulkarni", "David Miller", "Emma Watson"])
    with f_col3:
        st.write("")

    pipeline_data = get_pipeline_data(stage_filter, rep_filter)

    # Summary Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        render_stat_card("Total Active Pipeline", pipeline_data["total_pipeline_value"], "+$140k vs last month", "💼", "indigo")
    with m2:
        render_stat_card("Open Deals Count", str(pipeline_data["open_deals_count"]), "+5 new deals this week", "📊", "cyan")
    with m3:
        render_stat_card("Average Deal Size", pipeline_data["avg_deal_size"], "+$1,200 avg expansion", "💰", "emerald")

    st.markdown("<br>", unsafe_allow_html=True)

    # Stage Distribution Funnel Card
    st.markdown("""
        <div style='background: white; padding: 1.25rem 1.4rem 0.5rem 1.4rem; border: 1px solid #e2e8f0; border-radius: 16px; margin-bottom: 0.5rem; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
            <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0; font-family: Outfit, sans-serif;'>Pipeline Stage Funnel Distribution</h3>
            <p style='font-size: 0.82rem; color: #64748b; margin: 3px 0 0 0;'>Total deal volume and pipeline value per sales cycle stage.</p>
        </div>
    """, unsafe_allow_html=True)

    df_stages = pipeline_data["stages"]
    fig_funnel = go.Figure(go.Funnel(
        y=df_stages["Stage"],
        x=df_stages["Total Value ($)"],
        textinfo="value+percent initial",
        marker=dict(color=["#6366f1", "#3b82f6", "#06b6d4", "#10b981", "#ec4899"])
    ))
    fig_funnel.update_layout(
        height=330,
        margin=dict(l=10, r=10, t=15, b=20),
        template="plotly_white",
        font=dict(family="Inter")
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Deals Table Card
    st.markdown("""
        <div style='background: white; padding: 1.25rem; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
            <h3 style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0 0 0.25rem 0; font-family: Outfit, sans-serif;'>Active Deals & ML Closing Probabilities</h3>
            <p style='font-size: 0.82rem; color: #64748b; margin-bottom: 1rem;'>Real-time AI probability scores calculated from activity logs and sentiment signals.</p>
    """, unsafe_allow_html=True)

    df_deals = pipeline_data["deals"]

    if df_deals.empty:
        st.info("No active deals match the selected stage and representative filters.")
    else:
        st.dataframe(
            df_deals,
            column_config={
                "Closing Probability": st.column_config.TextColumn(
                    "ML Closing Prob.",
                    help="ML model predicted probability of successful closure"
                ),
                "Value": st.column_config.TextColumn("Deal Value"),
                "Status": st.column_config.TextColumn("Health Status"),
            },
            hide_index=True,
            use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
