"""
SalesPulse Executive & Operational Dashboard
--------------------------------------------
Assignment 2.41 - Streamlit Hierarchical Dashboard Application

Implements 4-Level Information Hierarchy:
- Level 1: Status (5 KPI Summary Cards)
- Level 2: Trends (Line charts for Revenue, Active vs Churned, and AOV)
- Level 3: Segments (Horizontal bar chart of Revenue by Customer Segment)
- Level 4: Detail & Progressive Disclosure (Sidebar filters, data explorer table, CSV export)
"""

import datetime
import os
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Streamlit Page Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SalesPulse Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("SalesPulse Executive & Operational Dashboard")
st.caption("Hierarchical Information Design: Status → Trends → Segments → Detail")

# ---------------------------------------------------------------------------
# Data Generation / Provider
# ---------------------------------------------------------------------------
@st.cache_data
def load_dashboard_data():
    np.random.seed(42)
    months = pd.date_range('2024-01-01', periods=12, freq='ME')
    revenue = [4.2, 4.5, 4.8, 4.6, 5.0, 5.1, 4.9, 4.7, 5.2, 5.4, 5.5, 5.2]
    active_customers = [2100, 2150, 2220, 2280, 2350, 2400, 2420, 2450, 2480, 2510, 2530, 2500]
    churned_customers = [120, 115, 130, 110, 105, 98, 102, 112, 95, 90, 88, 92]
    aov = [132, 135, 138, 136, 140, 142, 141, 139, 143, 146, 148, 145]

    trend_df = pd.DataFrame({
        'month': months,
        'revenue_millions': revenue,
        'active_customers': active_customers,
        'churned_customers': churned_customers,
        'avg_order_value': aov
    })

    segments = ['Enterprise', 'Mid-Market', 'SMB', 'Starter']
    segment_revenue = [2.1, 1.5, 1.0, 0.6]
    segment_df = pd.DataFrame({
        'segment': segments,
        'revenue_millions': segment_revenue
    })

    # Detail records (400 sample customer rows)
    n_cust = 400
    detail_df = pd.DataFrame({
        'customer_id': [f"CUST-{1000 + i}" for i in range(n_cust)],
        'segment': np.random.choice(segments, size=n_cust, p=[0.15, 0.30, 0.35, 0.20]),
        'revenue': np.round(np.random.uniform(500, 50000, size=n_cust), 2),
        'last_activity': pd.date_range('2024-01-01', '2024-12-31', periods=n_cust).strftime('%Y-%m-%d'),
        'churn_risk': np.random.choice(['Low', 'Medium', 'High'], size=n_cust, p=[0.70, 0.20, 0.10])
    })

    return trend_df, segment_df, detail_df

trend_df, segment_df, detail_df = load_dashboard_data()

# ---------------------------------------------------------------------------
# Level 1: Status — KPI Summary Cards (5 cards max)
# ---------------------------------------------------------------------------
st.subheader("Level 1: Executive Status Overview")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label="Revenue", value="$5.2M", delta="+12.5% YoY")
with col2:
    st.metric(label="Active Customers", value="2,500", delta="+5.2% YoY")
with col3:
    st.metric(label="Avg Order Value", value="$145", delta="+3.1% YoY")
with col4:
    st.metric(label="Churn Rate", value="4.8%", delta="-1.2% YoY", delta_color="inverse")
with col5:
    st.metric(label="NPS Score", value="72", delta="+4 YoY")

st.divider()

# ---------------------------------------------------------------------------
# Level 2: Trends — Performance Over Time (Middle Row)
# ---------------------------------------------------------------------------
st.subheader("Level 2: Business Trends & Performance Patterns")

t_col1, t_col2 = st.columns(2)

with t_col1:
    fig1, ax1 = plt.subplots(figsize=(7, 3.8))
    ax1.plot(trend_df['month'], trend_df['revenue_millions'], marker='o', linewidth=2.2, color='#1f77b4', label='Monthly Revenue')
    ax1.axhline(y=5.0, color='#2ca02c', linestyle='--', linewidth=1.5, label='Target: $5.0M')
    ax1.set_title('Monthly Revenue Trend (2024)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Month', fontsize=10)
    ax1.set_ylabel('Revenue ($M)', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=9)
    plt.tight_layout()
    st.pyplot(fig1)

with t_col2:
    fig2, ax2 = plt.subplots(figsize=(7, 3.8))
    ax2.plot(trend_df['month'], trend_df['active_customers'], marker='s', linewidth=2, color='#1f77b4', label='Active Customers')
    ax2_twin = ax2.twinx()
    ax2_twin.plot(trend_df['month'], trend_df['churned_customers'], marker='^', linewidth=2, color='#d62728', label='Churned Customers')
    ax2.set_title('Active vs. Churned Customers Trend', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Month', fontsize=10)
    ax2.set_ylabel('Active Customers', color='#1f77b4', fontsize=10)
    ax2_twin.set_ylabel('Churned Customers', color='#d62728', fontsize=10)
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig2)

st.divider()

# ---------------------------------------------------------------------------
# Level 3: Segments — Segment Breakdown
# ---------------------------------------------------------------------------
st.subheader("Level 3: Revenue by Customer Segment")
s_col1, s_col2 = st.columns([1.5, 1])

with s_col1:
    fig3, ax3 = plt.subplots(figsize=(8, 3.5))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    bars = ax3.barh(segment_df['segment'], segment_df['revenue_millions'], color=colors, edgecolor='black', alpha=0.85)
    ax3.invert_yaxis()
    ax3.set_xlabel('Revenue ($M)', fontsize=10)
    ax3.set_title('Revenue Share by Segment (2024)', fontsize=12, fontweight='bold')
    for bar in bars:
        ax3.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, f'${bar.get_width()}M', va='center', fontweight='bold', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig3)

with s_col2:
    st.markdown("""
    **Segment Performance Takeaways:**
    - **Enterprise** generates **$2.1M (40.4%)** of total revenue despite smaller logo count.
    - **Mid-Market** accounts for **$1.5M (28.8%)** with steady retention.
    - **SMB** ($1.0M) and **Starter** ($0.6M) represent expansion opportunities.
    """)

st.divider()

# ---------------------------------------------------------------------------
# Level 4: Detail — Progressive Disclosure & Data Explorer
# ---------------------------------------------------------------------------
st.subheader("Level 4: Detailed Data Explorer (Progressive Disclosure)")

st.sidebar.header("Filter Explorer Controls")
selected_segment = st.sidebar.selectbox("Customer Segment", ["All", "Enterprise", "Mid-Market", "SMB", "Starter"])
selected_risk = st.sidebar.multiselect("Churn Risk Level", ["Low", "Medium", "High"], default=["Low", "Medium", "High"])

filtered_df = detail_df.copy()
if selected_segment != "All":
    filtered_df = filtered_df[filtered_df['segment'] == selected_segment]

if selected_risk:
    filtered_df = filtered_df[filtered_df['churn_risk'].isin(selected_risk)]

st.write(f"Showing **{len(filtered_df):,}** customer records matching active filters.")
st.dataframe(filtered_df, use_container_width=True)

csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data CSV",
    data=csv_data,
    file_name=f"salespulse_filtered_data_{selected_segment.lower()}.csv",
    mime="text/csv"
)
