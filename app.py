"""
SalesPulse Analytics Dashboard
--------------------------------
Assignment 2.56 - Alert Monitoring & Metric Threshold Detection

Operational Streamlit dashboard displaying business KPIs and reactive alerts:
  Task 1: Monitor 3 metrics (Churn Rate, Avg Order Value, Data Quality Null %) against thresholds
  Task 2: Visual alerts displayed using st.error (critical) and st.warning (warning)
  Task 3: Thresholds stored in alert_config.py configuration module
  Task 4: Complete alert messages including metric name, current value, threshold, and risk action
  Task 5: Alerts dynamically update on filter changes
"""

import os
import sys
import io
import streamlit as st
import pandas as pd
import numpy as np

# Add frontend directory to path if needed for imports
sys.path.append(os.path.dirname(__file__))

# Import Alert Configuration Module (Task 1 & Task 3)
try:
    from alert_config import ALERT_THRESHOLDS, check_alerts
except ImportError:
    from frontend.alert_config import ALERT_THRESHOLDS, check_alerts

# -----------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="SalesPulse Analytics Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------
# Cached Data Loading
# -----------------------------------------------------------------------
@st.cache_data
def load_uploaded_data(file_bytes, file_name):
    """Load uploaded file bytes into a DataFrame. Cached by content."""
    buffer = io.BytesIO(file_bytes)
    if file_name.endswith(".csv"):
        return pd.read_csv(buffer)
    elif file_name.endswith(".json"):
        return pd.read_json(buffer)
    else:
        raise ValueError(f"Unsupported file format: {file_name}")

@st.cache_data
def load_sample_data():
    """Generate baseline SalesPulse dataset. Cached in memory."""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=180, freq="D")
    customer_ids = np.random.randint(1001, 1500, size=180)
    df = pd.DataFrame({
        "customer_id": customer_ids,
        "date": dates,
        "revenue": np.round(np.random.uniform(500, 5000, size=180), 2),
        "orders": np.random.randint(1, 15, size=180),
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


# Initialize dataset source (Sample or Uploaded)
if "custom_df" in st.session_state and st.session_state["custom_df"] is not None:
    df = st.session_state["custom_df"]
else:
    df = load_sample_data()

# Ensure date column is datetime
if "date" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["date"]):
    try:
        df["date"] = pd.to_datetime(df["date"])
    except Exception:
        pass

if "customer_id" not in df.columns:
    df["customer_id"] = np.arange(1000, 1000 + len(df))

# -----------------------------------------------------------------------
# Sidebar Navigation & Threshold Config Viewer
# -----------------------------------------------------------------------
st.sidebar.title("SalesPulse")
st.sidebar.markdown("*Analytics Dashboard*")
st.sidebar.divider()

st.sidebar.subheader("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Trends", "Data Explorer", "Segment Workflow", "Data Upload"],
    label_visibility="collapsed"
)

st.sidebar.divider()

# Sidebar Threshold Settings Info (Task 3 Verification)
with st.sidebar.expander("⚙️ Alert Threshold Config"):
    st.caption("Configured in `alert_config.py`:")
    for key, cfg in ALERT_THRESHOLDS.items():
        st.write(f"• **{cfg['metric']}**: {cfg['direction']} `{cfg['threshold']}` ({cfg['severity']})")

st.sidebar.divider()

# -----------------------------------------------------------------------
# Sidebar Filters (Reactive Filter Chain)
# -----------------------------------------------------------------------
st.sidebar.header("Filters")

if "date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["date"]):
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
else:
    date_range = None

if "segment" in df.columns:
    all_segments = sorted(df["segment"].dropna().unique().tolist())
    selected_segments = st.sidebar.multiselect(
        "Segments",
        options=all_segments,
        default=all_segments,
    )
else:
    all_segments = []
    selected_segments = []

rev_col = "revenue" if "revenue" in df.columns else df.select_dtypes(include="number").columns[0]
rev_min_global = float(df[rev_col].min())
rev_max_global = float(df[rev_col].max())

rev_range = st.sidebar.slider(
    "Revenue Range ($)",
    min_value=int(rev_min_global),
    max_value=int(rev_max_global),
    value=(int(rev_min_global), int(rev_max_global)),
    step=100 if rev_max_global - rev_min_global < 10000 else 1000,
)

granularity = st.sidebar.radio(
    "Chart Granularity",
    ["Daily", "Weekly", "Monthly"],
    index=0,
)

st.sidebar.divider()

if st.sidebar.button("Reset Filters"):
    st.rerun()

# -----------------------------------------------------------------------
# Reactive DataFrame Filter Chain
# -----------------------------------------------------------------------
filtered_df = df.copy()

if date_range and len(date_range) == 2 and "date" in filtered_df.columns:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["date"].dt.date >= start_date) &
        (filtered_df["date"].dt.date <= end_date)
    ]

if selected_segments and "segment" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["segment"].isin(selected_segments)]

filtered_df = filtered_df[
    (filtered_df[rev_col] >= rev_range[0]) &
    (filtered_df[rev_col] <= rev_range[1])
]

# Guard function for empty filtered dataset
def check_empty(fdf):
    if len(fdf) == 0:
        st.warning("No data matches current filters. Broaden your selection.")
        st.stop()


RESAMPLE_MAP = {"Daily": "D", "Weekly": "W", "Monthly": "ME"}

def resample_revenue(fdf, gran):
    freq = RESAMPLE_MAP.get(gran, "D")
    if "date" in fdf.columns:
        return (
            fdf.resample(freq, on="date")[rev_col]
            .sum()
            .reset_index()
            .rename(columns={rev_col: "Revenue ($)"})
        )
    return pd.DataFrame()


# -----------------------------------------------------------------------
# OVERVIEW PAGE WITH ALERT SYSTEM INTEGRATION
# -----------------------------------------------------------------------
if page == "Overview":
    st.title("Real-Time Business Overview & Alert Monitoring")
    st.caption("Live operational dashboard with metric threshold detection (Assignment 2.56)")

    check_empty(filtered_df)

    # -------------------------------------------------------------------
    # Compute Current Metrics for Threshold Evaluation (Task 1 & Task 5)
    # -------------------------------------------------------------------
    total_revenue = filtered_df[rev_col].sum()
    avg_order = filtered_df[rev_col].mean()
    row_count = len(filtered_df)
    unique_customers = filtered_df["customer_id"].nunique()

    # Metric 1: Churn Rate (%)
    if "churn_risk" in filtered_df.columns:
        churn_rate_val = float((filtered_df["churn_risk"] == "High").mean() * 100)
    else:
        churn_rate_val = 0.0

    # Metric 2: Avg Order Value ($)
    avg_order_val = float(avg_order) if not pd.isna(avg_order) else 0.0

    # Metric 3: Data Quality Null Percentage (%)
    total_cells = filtered_df.shape[0] * filtered_df.shape[1]
    null_count = filtered_df.isnull().sum().sum()
    null_pct_val = (null_count / total_cells * 100) if total_cells > 0 else 0.0
    data_quality_pct = 100.0 - null_pct_val

    # Dict of current metrics for threshold evaluation
    current_metrics = {
        "churn_rate": churn_rate_val,
        "avg_order_value": avg_order_val,
        "null_percentage": null_pct_val
    }

    # -------------------------------------------------------------------
    # Check Alerts & Render Visual Banner Alerts (Task 2, Task 4, Task 5)
    # -------------------------------------------------------------------
    active_alerts = check_alerts(current_metrics, ALERT_THRESHOLDS)

    if active_alerts:
        st.header("🚨 Active Operational Alerts")
        for alert in active_alerts:
            # Task 4: Complete message string: metric, value, threshold, action
            alert_text = (
                f"**ALERT:** {alert['metric']} is **{alert['value']:.1f}** "
                f"(Threshold: `{alert['threshold']}`). {alert['message']}"
            )
            if alert["severity"] == "critical":
                st.error(alert_text)
            else:
                st.warning(alert_text)
        st.divider()

    # -------------------------------------------------------------------
    # Five Reactive KPI Cards
    # -------------------------------------------------------------------
    st.header("Key Performance Indicators")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Revenue", f"${total_revenue:,.0f}")
    with col2:
        st.metric("Avg Order", f"${avg_order:,.0f}")
    with col3:
        st.metric("Records", f"{row_count:,}")
    with col4:
        st.metric("Customers", f"{unique_customers:,}")
    with col5:
        st.metric("Data Quality", f"{data_quality_pct:.1f}%")

    st.divider()

    # -------------------------------------------------------------------
    # Visualizations
    # -------------------------------------------------------------------
    st.header("Interactive Analytics Visualizations")

    st.subheader("Revenue Over Time (Line Trend)")
    if "date" in filtered_df.columns:
        trend_df = resample_revenue(filtered_df, granularity)
        st.line_chart(trend_df.set_index("date"))

    st.divider()

    col_chart_a, col_chart_b = st.columns(2)

    with col_chart_a:
        st.subheader("Revenue by Segment (Bar Chart)")
        if "segment" in filtered_df.columns:
            seg_df = filtered_df.groupby("segment")[rev_col].sum().reset_index()
            st.bar_chart(seg_df.set_index("segment"))

    with col_chart_b:
        st.subheader("Order Value Distribution (Plotly Histogram)")
        try:
            import plotly.express as px
            fig_hist = px.histogram(
                filtered_df, x=rev_col, nbins=30,
                title="Revenue / Order Value Distribution",
                template="plotly_white",
                color_discrete_sequence=["#1e3a8a"]
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        except ImportError:
            st.write(filtered_df[rev_col].describe())

    st.divider()

    with st.expander("ℹ️ About Metric Threshold Monitoring"):
        st.write(
            "Threshold alerts are defined in `alert_config.py` and checked on every rerun.\n\n"
            "• **Churn Rate Threshold**: > 7.0% (Critical Error)\n"
            "• **Avg Order Value Threshold**: < $2500.0 (Warning)\n"
            "• **Null Data Quality Threshold**: > 5.0% (Warning)\n\n"
            "When filters change the metrics (e.g. filtering to Enterprise vs SMB), alerts recalculate dynamically."
        )

# -----------------------------------------------------------------------
# TRENDS PAGE
# -----------------------------------------------------------------------
elif page == "Trends":
    st.title("Trend Analysis")
    st.caption(f"Granularity: {granularity} | Filtered Selection")

    check_empty(filtered_df)

    st.header("Revenue Trends")
    if "date" in filtered_df.columns:
        resampled = resample_revenue(filtered_df, granularity)
        try:
            import plotly.express as px
            fig_rev = px.line(
                resampled, x="date", y="Revenue ($)",
                title=f"{granularity} Revenue Growth",
                template="plotly_white",
                color_discrete_sequence=["#1e3a8a"],
            )
            fig_rev.update_traces(line_width=2)
            st.plotly_chart(fig_rev, use_container_width=True)
        except ImportError:
            st.line_chart(resampled.set_index("date")["Revenue ($)"])

    st.divider()

    st.header("Volume & Risk Distribution")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if "orders" in filtered_df.columns and "date" in filtered_df.columns:
            freq = RESAMPLE_MAP.get(granularity, "D")
            weekly_orders = filtered_df.resample(freq, on="date")["orders"].sum().reset_index()
            st.bar_chart(weekly_orders.set_index("date"))
        else:
            st.bar_chart(filtered_df[rev_col].head(20))

    with col_t2:
        if "churn_risk" in filtered_df.columns:
            try:
                import plotly.express as px
                fig_risk = px.pie(
                    filtered_df["churn_risk"].value_counts().reset_index(),
                    names="churn_risk", values="count",
                    title="Risk Tier Distribution",
                    template="plotly_white",
                    color_discrete_map={"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"}
                )
                st.plotly_chart(fig_risk, use_container_width=True)
            except ImportError:
                st.write(filtered_df["churn_risk"].value_counts())

# -----------------------------------------------------------------------
# DATA EXPLORER PAGE
# -----------------------------------------------------------------------
elif page == "Data Explorer":
    st.title("Data Explorer")
    st.caption("Inspect and export filtered dataset")

    check_empty(filtered_df)

    st.header("Filtered Data Summary")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Records", f"{len(filtered_df):,}")
    with m2:
        st.metric("Total Revenue", f"${filtered_df[rev_col].sum():,.0f}")
    with m3:
        st.metric("Avg Order", f"${filtered_df[rev_col].mean():,.0f}")
    with m4:
        st.metric("Customers", f"{filtered_df['customer_id'].nunique():,}")

    st.divider()

    st.header("Filtered Records")
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

    st.divider()
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered CSV",
        data=csv_bytes,
        file_name="salespulse_filtered_data.csv",
        mime="text/csv",
    )

# -----------------------------------------------------------------------
# SEGMENT WORKFLOW PAGE
# -----------------------------------------------------------------------
elif page == "Segment Workflow":
    st.title("Guided Segment Analysis Workflow")
    st.caption("Multi-step analytical workflow powered by Streamlit session state")

    if "selected_segment" not in st.session_state:
        st.session_state["selected_segment"] = "All"
    if "workflow_step" not in st.session_state:
        st.session_state["workflow_step"] = 1
    if "analysis_result" not in st.session_state:
        st.session_state["analysis_result"] = None

    st.sidebar.divider()
    st.sidebar.subheader("Workflow State")
    st.sidebar.info(f"Current Step: {st.session_state['workflow_step']} of 3")
    st.sidebar.write(f"Active Segment: **{st.session_state['selected_segment']}**")

    if st.sidebar.button("Reset Workflow"):
        for key in ["selected_segment", "workflow_step", "analysis_result"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    progress_val = min(st.session_state["workflow_step"] / 3.0, 1.0)
    st.progress(progress_val, text=f"Workflow Progress: Step {st.session_state['workflow_step']} / 3")
    st.divider()

    st.header("Step 1: Select Target Segment")
    segment_options = ["All", "Enterprise", "Mid-Market", "SMB"]
    current_index = segment_options.index(st.session_state["selected_segment"])

    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        chosen_seg = st.selectbox(
            "Choose customer segment to analyze",
            options=segment_options,
            index=current_index,
        )
    with col_s2:
        st.write("")
        st.write("")
        if st.button("Confirm Segment", type="primary"):
            st.session_state["selected_segment"] = chosen_seg
            st.session_state["workflow_step"] = max(st.session_state["workflow_step"], 2)
            st.rerun()

    st.divider()

    if st.session_state["workflow_step"] >= 2:
        st.header("Step 2: Segment Metrics Computation")
        active_seg = st.session_state["selected_segment"]
        st.success(f"Confirmed Target Segment: **{active_seg}**")

        if active_seg == "All" or "segment" not in filtered_df.columns:
            w_df = filtered_df
        else:
            w_df = filtered_df[filtered_df["segment"] == active_seg]

        check_empty(w_df)

        st.session_state["analysis_result"] = {
            "segment": active_seg,
            "record_count": len(w_df),
            "total_revenue": w_df[rev_col].sum(),
            "avg_order": w_df[rev_col].mean(),
            "customers": w_df["customer_id"].nunique()
        }

        res = st.session_state["analysis_result"]

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("Segment Revenue", f"${res['total_revenue']:,.0f}")
        with m_col2:
            st.metric("Total Records", f"{res['record_count']:,}")
        with m_col3:
            st.metric("Avg Order", f"${res['avg_order']:,.0f}")
        with m_col4:
            st.metric("Unique Customers", f"{res['customers']:,}")

        if st.button("Proceed to Detailed Breakdown"):
            st.session_state["workflow_step"] = 3
            st.rerun()

        st.divider()

    if st.session_state["workflow_step"] >= 3:
        st.header("Step 3: Detailed Breakdown & Export")
        res = st.session_state["analysis_result"]

        active_seg = st.session_state["selected_segment"]
        if active_seg == "All" or "segment" not in filtered_df.columns:
            w_df = filtered_df
        else:
            w_df = filtered_df[filtered_df["segment"] == active_seg]

        st.dataframe(w_df.head(20), use_container_width=True)

        with st.expander("Export Segment Analysis Data"):
            csv_data = w_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label=f"Download {res['segment']} Segment CSV",
                data=csv_data,
                file_name=f"salespulse_{res['segment'].lower()}_analysis.csv",
                mime="text/csv"
            )

# -----------------------------------------------------------------------
# DATA UPLOAD PAGE
# -----------------------------------------------------------------------
elif page == "Data Upload":
    st.title("Dataset Upload & Live Dashboard Wiring")
    st.caption("Upload custom CSV/JSON files -- automatically updates dashboard metrics")

    uploaded_file = st.file_uploader(
        "Upload your dataset",
        type=["csv", "json"],
        help="Supported formats: CSV (.csv) and JSON (.json)",
    )

    if uploaded_file is not None:
        try:
            file_bytes = uploaded_file.getvalue()
            udf = load_uploaded_data(file_bytes, uploaded_file.name)

            if len(udf) == 0:
                st.warning("The uploaded file is empty. Please check your data.")
                st.stop()

            st.session_state["custom_df"] = udf

        except Exception as e:
            st.error(f"Could not read '{uploaded_file.name}': {e}")
            st.stop()

        st.success(
            f"File loaded and wired to dashboard: {uploaded_file.name} "
            f"({len(udf):,} rows, {len(udf.columns)} columns)"
        )
        st.divider()

        st.header("Dataset Preview")
        total_nulls = udf.isnull().sum().sum()
        null_pct = total_nulls / (udf.shape[0] * udf.shape[1]) * 100 if udf.shape[0] * udf.shape[1] > 0 else 0
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", f"{len(udf):,}")
        with col2:
            st.metric("Columns", str(len(udf.columns)))
        with col3:
            st.metric("Null %", f"{null_pct:.1f}%")

        st.divider()
        st.subheader("First 10 Rows")
        st.dataframe(udf.head(10), use_container_width=True)

        st.subheader("Descriptive Statistics")
        num_udf = udf.select_dtypes(include="number")
        if not num_udf.empty:
            st.dataframe(num_udf.describe(), use_container_width=True)

        if st.button("Use This Dataset Across Dashboard"):
            st.rerun()

    else:
        st.info("Upload a CSV or JSON file. The dashboard will automatically adapt to your data.")
        if "custom_df" in st.session_state:
            if st.button("Reset to Default Sample Dataset"):
                st.session_state["custom_df"] = None
                st.rerun()
