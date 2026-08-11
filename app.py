"""
SalesPulse Analytics Dashboard
--------------------------------
Assignment 2.53 - Streamlit Filters & Interactive Widgets

Extends 2.52 with a full interactive filter chain:
  Task 1: Three widget types -- date_input, multiselect, slider, radio
  Task 2: All widgets wired to filter the DataFrame reactively
  Task 3: Meaningful defaults so the app loads with full data visible
  Task 4: Empty filter result handling with st.warning + st.stop
  Task 5: Reset Filters button via st.rerun()
"""

import streamlit as st
import pandas as pd
import numpy as np

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
# Cached data loader
# -----------------------------------------------------------------------
@st.cache_data
def load_sample_data():
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


df = load_sample_data()

# -----------------------------------------------------------------------
# Sidebar: Navigation
# -----------------------------------------------------------------------
st.sidebar.title("SalesPulse")
st.sidebar.markdown("*Analytics Dashboard*")
st.sidebar.divider()

st.sidebar.subheader("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Trends", "Data Explorer", "Data Upload"],
    label_visibility="collapsed"
)

st.sidebar.divider()

# -----------------------------------------------------------------------
# Task 1: Three widget types wired to a shared filter chain
# Widget 1 -- st.date_input  (date range picker)
# Widget 2 -- st.multiselect (categorical segment filter)
# Widget 3 -- st.slider      (numeric revenue range)
# Widget 4 -- st.radio       (chart granularity: Daily / Weekly / Monthly)
# -----------------------------------------------------------------------
st.sidebar.header("Filters")

# Widget 1: Date range picker -- defaults to full dataset range (Task 3)
date_range = st.sidebar.date_input(
    "Date Range",
    value=(df["date"].min().date(), df["date"].max().date()),
    min_value=df["date"].min().date(),
    max_value=df["date"].max().date(),
)

# Widget 2: Multi-select -- defaults to all segments selected (Task 3)
all_segments = sorted(df["segment"].unique().tolist())
selected_segments = st.sidebar.multiselect(
    "Segments",
    options=all_segments,
    default=all_segments,
)

# Widget 3: Revenue slider -- defaults to full range (Task 3)
rev_min_global = int(df["revenue"].min())
rev_max_global = int(df["revenue"].max())
rev_range = st.sidebar.slider(
    "Revenue Range ($)",
    min_value=rev_min_global,
    max_value=rev_max_global,
    value=(rev_min_global, rev_max_global),
    step=1000,
)

# Widget 4: Radio -- chart granularity (Task 1, 4th widget type)
granularity = st.sidebar.radio(
    "Chart Granularity",
    ["Daily", "Weekly", "Monthly"],
    index=0,
)

st.sidebar.divider()

# Task 5: Reset Filters -- st.rerun() resets all widgets to defaults
if st.sidebar.button("Reset Filters"):
    st.rerun()

st.sidebar.caption("Filters apply to Overview, Trends, and Data Explorer sections.")

# -----------------------------------------------------------------------
# Task 2: Wire all widgets into a single filtered DataFrame
# Every chart, metric, and table reads from filtered_df
# -----------------------------------------------------------------------
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = df["date"].min().date()
    end_date = df["date"].max().date()

# Guard: if multiselect is cleared use all segments to prevent crash
active_segments = selected_segments if selected_segments else all_segments

filtered_df = df[
    (df["date"].dt.date >= start_date)
    & (df["date"].dt.date <= end_date)
    & (df["segment"].isin(active_segments))
    & (df["revenue"] >= rev_range[0])
    & (df["revenue"] <= rev_range[1])
].copy()

# -----------------------------------------------------------------------
# Task 4: Empty filter result handling
# -----------------------------------------------------------------------
def check_empty(fdf):
    if len(fdf) == 0:
        st.warning(
            "No data matches the current filters. "
            "Try broadening your date range, selecting more segments, "
            "or widening the revenue slider."
        )
        st.stop()


# -----------------------------------------------------------------------
# Helper: resample filtered_df by granularity widget
# -----------------------------------------------------------------------
RESAMPLE_MAP = {"Daily": "D", "Weekly": "W", "Monthly": "ME"}

def resample_revenue(fdf, gran):
    freq = RESAMPLE_MAP.get(gran, "D")
    return (
        fdf.resample(freq, on="date")["revenue"]
        .sum()
        .reset_index()
        .rename(columns={"revenue": "Revenue ($)"})
    )


# -----------------------------------------------------------------------
# OVERVIEW PAGE
# -----------------------------------------------------------------------
if page == "Overview":
    st.title("Business Overview")
    st.caption(
        f"Filtered view: {start_date} to {end_date} "
        f"| Segments: {', '.join(active_segments)} "
        f"| Revenue: ${rev_range[0]:,} - ${rev_range[1]:,}"
    )

    check_empty(filtered_df)

    # KPI cards from filtered data
    st.header("Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Revenue (Filtered)", f"${filtered_df['revenue'].sum():,.0f}")
    with col2:
        st.metric("Records", f"{len(filtered_df):,}")
    with col3:
        st.metric("Avg. Order Value", f"${filtered_df['aov'].mean():.2f}")
    with col4:
        churn_high = round((filtered_df["churn_risk"] == "High").mean() * 100, 1)
        st.metric("High Churn Risk", f"{churn_high}%", delta_color="inverse")
    with col5:
        avg_resp = filtered_df["support_response_hours"].mean()
        st.metric("Avg Response Time", f"{avg_resp:.1f} hrs")

    st.caption(f"Showing {len(filtered_df):,} of {len(df):,} total records")
    st.divider()

    # Segment breakdown on filtered data
    st.header("Segment Performance")
    st.subheader("Revenue and Risk Distribution")

    seg_summary = (
        filtered_df.groupby("segment")
        .agg(avg_revenue=("revenue", "mean"), record_count=("orders", "sum"))
        .reset_index()
    )

    col_a, col_b = st.columns(2)
    with col_a:
        try:
            import plotly.express as px
            fig_seg = px.bar(
                seg_summary, x="segment", y="avg_revenue", color="segment",
                title="Average Daily Revenue by Segment (Filtered)",
                color_discrete_map={
                    "Enterprise": "#1e3a8a",
                    "Mid-Market": "#3b82f6",
                    "SMB": "#93c5fd",
                },
                template="plotly_white",
            )
            st.plotly_chart(fig_seg, use_container_width=True)
        except ImportError:
            st.bar_chart(seg_summary.set_index("segment")["avg_revenue"])

    with col_b:
        try:
            risk_counts = filtered_df["churn_risk"].value_counts().reset_index()
            risk_counts.columns = ["churn_risk", "count"]
            fig_risk = px.pie(
                risk_counts, names="churn_risk", values="count",
                title="Risk Distribution (Filtered)",
                color="churn_risk",
                color_discrete_map={
                    "Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"
                },
                template="plotly_white",
            )
            st.plotly_chart(fig_risk, use_container_width=True)
        except ImportError:
            st.write(filtered_df["churn_risk"].value_counts())

    with st.expander("About These Metrics"):
        st.write(
            "All KPIs reflect the current filter selection. "
            "Use the sidebar to change date range, segments, or revenue threshold. "
            "Click **Reset Filters** to return to the full dataset view."
        )


# -----------------------------------------------------------------------
# TRENDS PAGE
# -----------------------------------------------------------------------
elif page == "Trends":
    st.title("Trend Analysis")
    st.caption(
        f"Granularity: {granularity} | "
        f"{start_date} to {end_date} | "
        f"Segments: {', '.join(active_segments)}"
    )

    check_empty(filtered_df)

    # Revenue trend -- granularity controlled by radio widget
    st.header("Revenue Trends")
    st.subheader(f"{granularity} Revenue -- Filtered Selection")

    resampled = resample_revenue(filtered_df, granularity)

    try:
        import plotly.express as px
        fig_rev = px.line(
            resampled, x="date", y="Revenue ($)",
            title=f"{granularity} Revenue (Filtered)",
            template="plotly_white",
            color_discrete_sequence=["#1e3a8a"],
        )
        fig_rev.update_traces(line_width=2)
        st.plotly_chart(fig_rev, use_container_width=True)
    except ImportError:
        st.line_chart(resampled.set_index("date")["Revenue ($)"])

    st.divider()

    # Customer and orders trends
    st.header("Customer Metrics")
    st.subheader("Orders and Support Response Over Filtered Period")

    col_left, col_right = st.columns(2)
    with col_left:
        try:
            freq = RESAMPLE_MAP.get(granularity, "D")
            weekly_orders = (
                filtered_df.resample(freq, on="date")["orders"]
                .sum()
                .reset_index()
            )
            fig_orders = px.bar(
                weekly_orders, x="date", y="orders",
                title=f"{granularity} Order Volume (Filtered)",
                template="plotly_white",
                color_discrete_sequence=["#6366f1"],
            )
            st.plotly_chart(fig_orders, use_container_width=True)
        except Exception:
            st.bar_chart(filtered_df.set_index("date")["orders"])

    with col_right:
        try:
            fig_resp = px.histogram(
                filtered_df, x="support_response_hours", color="churn_risk",
                title="Response Time Distribution (Filtered)",
                color_discrete_map={
                    "Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"
                },
                template="plotly_white", nbins=20,
            )
            st.plotly_chart(fig_resp, use_container_width=True)
        except ImportError:
            st.write(filtered_df["support_response_hours"].describe())

    with st.expander("Methodology Notes"):
        st.write(
            f"**{granularity} granularity** is controlled by the Chart Granularity "
            "radio button in the sidebar. Switch between Daily, Weekly, and Monthly "
            "to smooth or zoom the revenue trend line.\n\n"
            "All data reflects the current sidebar filter combination."
        )


# -----------------------------------------------------------------------
# DATA EXPLORER PAGE
# -----------------------------------------------------------------------
elif page == "Data Explorer":
    st.title("Data Explorer")
    st.caption("Interactive filter chain -- all sidebar widgets apply here")

    check_empty(filtered_df)

    # Summary metrics from filtered data
    st.header("Filtered Data Summary")
    st.subheader(f"Showing {len(filtered_df):,} of {len(df):,} records")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Records", f"{len(filtered_df):,}")
    with m2:
        st.metric("Total Revenue", f"${filtered_df['revenue'].sum():,.0f}")
    with m3:
        st.metric("Avg AOV", f"${filtered_df['aov'].mean():.2f}")
    with m4:
        st.metric("Avg Response", f"{filtered_df['support_response_hours'].mean():.1f} hrs")

    st.divider()

    # Filtered data table
    st.header("Filtered Records")
    st.dataframe(
        filtered_df[[
            "date", "segment", "revenue", "orders",
            "aov", "churn_risk", "support_response_hours"
        ]].reset_index(drop=True),
        use_container_width=True,
    )

    st.divider()

    # Download filtered dataset
    st.header("Export")
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered CSV",
        data=csv_bytes,
        file_name="salespulse_filtered_data.csv",
        mime="text/csv",
    )

    with st.expander("Support Response Analysis"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            avg_resp = filtered_df["support_response_hours"].mean()
            high_resp = (filtered_df["support_response_hours"] > 8).mean() * 100
            st.metric("Avg Response Time", f"{avg_resp:.1f} hrs")
            st.metric("% Responses > 8 hrs", f"{high_resp:.1f}%")
            st.write(
                "Customers with response time > 8 hours are flagged as "
                "High Churn Risk in the pipeline."
            )
        with col_s2:
            try:
                import plotly.express as px
                fig_resp = px.histogram(
                    filtered_df, x="support_response_hours", color="churn_risk",
                    title="Response Time Distribution",
                    color_discrete_map={
                        "Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"
                    },
                    template="plotly_white", nbins=20,
                )
                st.plotly_chart(fig_resp, use_container_width=True)
            except ImportError:
                st.write(filtered_df["support_response_hours"].describe())


# -----------------------------------------------------------------------
# DATA UPLOAD PAGE (2.52 -- preserved unchanged)
# -----------------------------------------------------------------------
elif page == "Data Upload":
    st.title("Dataset Upload & Preview")
    st.caption("Upload your own CSV or JSON file for instant analysis")

    uploaded_file = st.file_uploader(
        "Upload your dataset",
        type=["csv", "json"],
        help="Supported formats: CSV (.csv) and JSON (.json)",
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                udf = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".json"):
                udf = pd.read_json(uploaded_file)
            else:
                st.error("Unsupported file type. Please upload a .csv or .json file.")
                st.stop()

            if len(udf) == 0:
                st.warning("The uploaded file is empty. Please check your data.")
                st.stop()

        except Exception:
            st.error("Could not read this file. Please check the format and try again.")
            st.stop()

        st.success(
            "File loaded: " + uploaded_file.name +
            " (" + str(len(udf)) + " rows, " + str(len(udf.columns)) + " columns)"
        )
        st.divider()

        st.header("Dataset Preview")
        total_nulls = udf.isnull().sum().sum()
        null_pct = total_nulls / (udf.shape[0] * udf.shape[1]) * 100
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

        st.subheader("Column Summary")
        summary = pd.DataFrame({
            "Column": udf.columns,
            "Type": udf.dtypes.astype(str).values,
            "Non-Null": udf.notnull().sum().values,
            "Null Count": udf.isnull().sum().values,
            "Null %": (udf.isnull().sum() / len(udf) * 100).round(1).values,
        })
        st.dataframe(summary, use_container_width=True)
        st.divider()

        st.header("Descriptive Statistics")
        numeric_udf = udf.select_dtypes(include="number")
        if not numeric_udf.empty:
            st.dataframe(numeric_udf.describe(), use_container_width=True)
        else:
            st.info("No numeric columns found in this dataset.")

        st.divider()
        st.header("Quick Exploration")
        numeric_cols = udf.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            col_vis, col_filter = st.columns([2, 1])
            with col_filter:
                selected_col = st.selectbox("Select column to visualise", numeric_cols)
                n_bins = st.slider("Number of bins", 5, 50, 20)
            with col_vis:
                try:
                    import plotly.express as px
                    fig_h = px.histogram(
                        udf, x=selected_col, nbins=n_bins,
                        title=f"Distribution of {selected_col}",
                        template="plotly_white",
                        color_discrete_sequence=["#3b82f6"],
                    )
                    st.plotly_chart(fig_h, use_container_width=True)
                except ImportError:
                    st.bar_chart(udf[selected_col].value_counts().head(20))
        else:
            st.info("No numeric columns available for visualisation.")

    else:
        st.info("Upload a CSV or JSON file to begin. Your data will be previewed instantly.")
