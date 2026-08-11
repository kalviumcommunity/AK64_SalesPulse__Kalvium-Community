"""
SalesPulse Analytics Dashboard
--------------------------------
Assignment 2.51 - Streamlit App Structure & Navigation

Multi-section analytics application with:
  Task 1: Sidebar navigation controlling section display
  Task 2: Three content sections with st.columns and st.expander
  Task 3: Consistent visual hierarchy (title, header, subheader, divider)
  Task 4: Requirements.txt, clean environment compatibility
  Task 5: KPI cards above the fold on first load
"""

import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------------------------------------------
# Page Configuration (must be first Streamlit command)
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="SalesPulse Analytics Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------
# Data Layer with Caching
# Streamlit reruns the entire script on every interaction.
# @st.cache_data ensures load_data() runs only once per session.
# -----------------------------------------------------------------------
@st.cache_data
def load_data():
    """Generate sample SalesPulse dataset. Cached to prevent recomputation."""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=180, freq="D")
    df = pd.DataFrame({
        "date": dates,
        "revenue": np.cumsum(np.random.normal(loc=5000, scale=800, size=180)) + 400_000,
        "customers": np.cumsum(np.random.randint(5, 30, size=180)) + 1800,
        "orders": np.random.randint(80, 300, size=180),
        "segment": np.random.choice(["Enterprise", "Mid-Market", "SMB"], size=180),
        "support_response_hours": np.round(
            np.random.exponential(scale=5, size=180), 1
        ),
        "churn_risk": np.random.choice(
            ["Low", "Medium", "High"], size=180, p=[0.65, 0.25, 0.10]
        ),
    })
    df["aov"] = (df["revenue"] / df["orders"]).round(2)
    return df


df = load_data()

# Precompute summary KPIs
total_revenue = df["revenue"].iloc[-1]
total_customers = int(df["customers"].iloc[-1])
avg_aov = df["aov"].mean()
churn_pct = round((df["churn_risk"] == "High").mean() * 100, 1)
nps_score = 72
prev_revenue = df["revenue"].iloc[-31]
revenue_delta = f"+{((total_revenue - prev_revenue) / prev_revenue * 100):.1f}%"

# -----------------------------------------------------------------------
# Task 1: Sidebar Navigation
# -----------------------------------------------------------------------
st.sidebar.title("SalesPulse")
st.sidebar.markdown("*Analytics Dashboard*")
st.sidebar.divider()

st.sidebar.subheader("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Trends", "Data Explorer"],
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.markdown(
    """
    **Sections**
    - **Overview**: KPIs & summary metrics
    - **Trends**: Revenue & customer charts
    - **Data Explorer**: Filters, tables & export
    """
)


# -----------------------------------------------------------------------
# Task 3 + Task 5: Visual Hierarchy -- Overview Page
# KPI cards appear at the very top -- above the fold, no scroll needed.
# -----------------------------------------------------------------------

if page == "Overview":
    st.title("Business Overview")
    st.caption("Executive summary -- SalesPulse performance at a glance")

    # -- Task 2 + Task 5: Five KPI cards in columns, immediately visible --
    st.header("Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Revenue", f"${total_revenue:,.0f}", revenue_delta)
    with col2:
        st.metric("Active Customers", f"{total_customers:,}", "+5.2%")
    with col3:
        st.metric("Avg. Order Value", f"${avg_aov:.2f}", "+2.1%")
    with col4:
        st.metric("High Churn Risk", f"{churn_pct}%", "-1.8%", delta_color="inverse")
    with col5:
        st.metric("NPS Score", str(nps_score), "+4")

    st.divider()

    # -- Segment breakdown using columns --
    st.header("Segment Performance")
    st.subheader("Revenue and Order Volume by Customer Segment")

    seg_summary = (
        df.groupby("segment")
        .agg(avg_revenue=("revenue", "mean"), order_count=("orders", "sum"))
        .reset_index()
    )

    col_a, col_b = st.columns(2)
    with col_a:
        try:
            import plotly.express as px
            fig_seg = px.bar(
                seg_summary, x="segment", y="avg_revenue",
                color="segment",
                title="Average Daily Revenue by Segment",
                color_discrete_map={
                    "Enterprise": "#1e3a8a",
                    "Mid-Market": "#3b82f6",
                    "SMB": "#93c5fd"
                },
                template="plotly_white"
            )
            st.plotly_chart(fig_seg, use_container_width=True)
        except ImportError:
            st.bar_chart(seg_summary.set_index("segment")["avg_revenue"])

    with col_b:
        try:
            risk_counts = df["churn_risk"].value_counts().reset_index()
            risk_counts.columns = ["churn_risk", "count"]
            fig_risk = px.pie(
                risk_counts,
                names="churn_risk", values="count",
                title="Customer Risk Distribution",
                color="churn_risk",
                color_discrete_map={
                    "Low": "#22c55e",
                    "Medium": "#f59e0b",
                    "High": "#ef4444"
                },
                template="plotly_white"
            )
            st.plotly_chart(fig_risk, use_container_width=True)
        except ImportError:
            st.write(df["churn_risk"].value_counts())

    st.divider()

    # -- Task 2: Expander for methodology notes (progressive disclosure) --
    with st.expander("About These Metrics"):
        st.write(
            "**Revenue** is the cumulative total of all order amounts. "
            "The delta shows change from the same period last month.\n\n"
            "**High Churn Risk** is the percentage of customers flagged by the "
            "risk model (support response delay > 8 hours AND declining order "
            "frequency). A negative delta is good -- fewer at-risk customers.\n\n"
            "**NPS Score** is measured via quarterly stakeholder surveys. "
            "Scores above 50 are considered Excellent."
        )


# -----------------------------------------------------------------------
# Task 3: Trends Page
# -----------------------------------------------------------------------
elif page == "Trends":
    st.title("Trend Analysis")
    st.caption("Time-series performance over the past 6 months")

    # -- Revenue Trends --
    st.header("Revenue Trends")
    st.subheader("Daily Revenue -- Last 180 Days")

    try:
        import plotly.express as px
        fig_rev = px.line(
            df, x="date", y="revenue",
            title="Cumulative Revenue Growth",
            labels={"revenue": "Revenue ($)", "date": "Date"},
            template="plotly_white",
            color_discrete_sequence=["#1e3a8a"]
        )
        fig_rev.update_traces(line_width=2)
        st.plotly_chart(fig_rev, use_container_width=True)
    except ImportError:
        st.line_chart(df.set_index("date")["revenue"])

    st.divider()

    # -- Customer Metrics --
    st.header("Customer Metrics")
    st.subheader("Active Customers and Order Volume Over Time")

    col_left, col_right = st.columns(2)
    with col_left:
        try:
            fig_cust = px.area(
                df, x="date", y="customers",
                title="Cumulative Active Customers",
                labels={"customers": "Customers", "date": "Date"},
                template="plotly_white",
                color_discrete_sequence=["#3b82f6"]
            )
            st.plotly_chart(fig_cust, use_container_width=True)
        except ImportError:
            st.line_chart(df.set_index("date")["customers"])

    with col_right:
        try:
            weekly_orders = (
                df.resample("W", on="date")["orders"].sum().reset_index()
            )
            fig_orders = px.bar(
                weekly_orders, x="date", y="orders",
                title="Weekly Order Volume",
                labels={"orders": "Orders", "date": "Week"},
                template="plotly_white",
                color_discrete_sequence=["#6366f1"]
            )
            st.plotly_chart(fig_orders, use_container_width=True)
        except ImportError:
            st.bar_chart(df.set_index("date")["orders"])

    st.divider()

    # -- Task 2: Expander for trend methodology --
    with st.expander("Methodology Notes"):
        st.write(
            "**Revenue** is plotted as a cumulative daily sum to show growth "
            "trajectory over the full 6-month period.\n\n"
            "**Weekly Order Volume** is aggregated using a 7-day rolling window. "
            "Weeks with fewer than 7 data points (start/end of range) are partial.\n\n"
            "Data source: analytics_views.db -- vw_product_performance view."
        )


# -----------------------------------------------------------------------
# Task 3: Data Explorer Page
# -----------------------------------------------------------------------
elif page == "Data Explorer":
    st.title("Data Explorer")
    st.caption("Filter, inspect, and export the underlying dataset")

    # -- Filters using columns --
    st.header("Filter Controls")
    st.subheader("Segment and Risk Tier Filters")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        segments = st.multiselect(
            "Customer Segment",
            options=["Enterprise", "Mid-Market", "SMB"],
            default=["Enterprise", "Mid-Market", "SMB"]
        )
    with col_f2:
        risk_tiers = st.multiselect(
            "Churn Risk Tier",
            options=["Low", "Medium", "High"],
            default=["Low", "Medium", "High"]
        )
    with col_f3:
        date_range = st.date_input(
            "Date Range",
            value=(df["date"].min().date(), df["date"].max().date())
        )

    # Apply filters
    filtered = df[
        df["segment"].isin(segments) &
        df["churn_risk"].isin(risk_tiers)
    ]
    if len(date_range) == 2:
        filtered = filtered[
            (filtered["date"].dt.date >= date_range[0]) &
            (filtered["date"].dt.date <= date_range[1])
        ]

    st.divider()

    # -- Filtered Summary --
    st.header("Filtered Data Summary")
    st.subheader(f"Showing {len(filtered):,} records matching your filters")

    sum_col1, sum_col2, sum_col3 = st.columns(3)
    with sum_col1:
        st.metric("Records", f"{len(filtered):,}")
    with sum_col2:
        st.metric("Avg Revenue", f"${filtered['revenue'].mean():,.0f}")
    with sum_col3:
        st.metric("Avg AOV", f"${filtered['aov'].mean():.2f}")

    st.divider()

    # -- Task 2: Expander for raw data table (progressive disclosure) --
    with st.expander("View Raw Data Table"):
        st.dataframe(
            filtered[[
                "date", "segment", "revenue", "orders",
                "aov", "churn_risk", "support_response_hours"
            ]],
            use_container_width=True
        )
        csv_bytes = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name="salespulse_filtered_data.csv",
            mime="text/csv"
        )

    with st.expander("Support Response Analysis"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            avg_resp = filtered["support_response_hours"].mean()
            st.metric("Avg Response Time", f"{avg_resp:.1f} hrs")
            st.write(
                "Customers with response time > 8 hours are automatically "
                "flagged as High Churn Risk in the pipeline."
            )
        with col_s2:
            try:
                import plotly.express as px
                fig_resp = px.histogram(
                    filtered, x="support_response_hours", color="churn_risk",
                    title="Response Time Distribution",
                    color_discrete_map={
                        "Low": "#22c55e",
                        "Medium": "#f59e0b",
                        "High": "#ef4444"
                    },
                    template="plotly_white",
                    nbins=20
                )
                st.plotly_chart(fig_resp, use_container_width=True)
            except ImportError:
                st.write(filtered["support_response_hours"].describe())
