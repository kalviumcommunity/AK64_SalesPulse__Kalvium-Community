"""
SalesPulse Analytics Dashboard
--------------------------------
Assignment 2.52 - Dataset Upload & Dynamic Preview System

Extends the multi-section app (2.51) with a full file upload pipeline:
  Task 1: st.file_uploader accepts CSV and JSON, handles None state
  Task 2: Automatic preview -- rows, columns, null%, first 10 rows, column summary
  Task 3: Descriptive statistics via df.describe()
  Task 4: Graceful error handling with st.error / st.stop (no tracebacks)
  Task 5: Downstream usability -- uploaded DataFrame drives filters and charts
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
# Cached sample data loader (2.51 baseline dataset)
# @st.cache_data prevents recomputation on every Streamlit rerun
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


df_sample = load_sample_data()

# Precompute KPIs for Overview section
total_revenue = df_sample["revenue"].iloc[-1]
total_customers = int(df_sample["customers"].iloc[-1])
avg_aov = df_sample["aov"].mean()
churn_pct = round((df_sample["churn_risk"] == "High").mean() * 100, 1)
nps_score = 72
prev_revenue = df_sample["revenue"].iloc[-31]
revenue_delta = f"+{((total_revenue - prev_revenue) / prev_revenue * 100):.1f}%"

# -----------------------------------------------------------------------
# Sidebar Navigation
# -----------------------------------------------------------------------
st.sidebar.title("SalesPulse")
st.sidebar.markdown("*Analytics Dashboard*")
st.sidebar.divider()

st.sidebar.subheader("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Trends", "Data Upload", "Data Explorer"],
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.markdown(
    """
    **Sections**
    - **Overview**: KPIs & summary metrics
    - **Trends**: Revenue & customer charts
    - **Data Upload**: Upload your own CSV or JSON
    - **Data Explorer**: Filters, tables & export
    """
)


# -----------------------------------------------------------------------
# OVERVIEW PAGE
# -----------------------------------------------------------------------
if page == "Overview":
    st.title("Business Overview")
    st.caption("Executive summary -- SalesPulse performance at a glance")

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

    st.header("Segment Performance")
    st.subheader("Revenue and Risk Distribution by Segment")

    seg_summary = (
        df_sample.groupby("segment")
        .agg(avg_revenue=("revenue", "mean"), order_count=("orders", "sum"))
        .reset_index()
    )

    col_a, col_b = st.columns(2)
    with col_a:
        try:
            import plotly.express as px
            fig_seg = px.bar(
                seg_summary, x="segment", y="avg_revenue", color="segment",
                title="Average Daily Revenue by Segment",
                color_discrete_map={
                    "Enterprise": "#1e3a8a", "Mid-Market": "#3b82f6", "SMB": "#93c5fd"
                },
                template="plotly_white"
            )
            st.plotly_chart(fig_seg, use_container_width=True)
        except ImportError:
            st.bar_chart(seg_summary.set_index("segment")["avg_revenue"])

    with col_b:
        try:
            risk_counts = df_sample["churn_risk"].value_counts().reset_index()
            risk_counts.columns = ["churn_risk", "count"]
            fig_risk = px.pie(
                risk_counts, names="churn_risk", values="count",
                title="Customer Risk Distribution",
                color="churn_risk",
                color_discrete_map={"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"},
                template="plotly_white"
            )
            st.plotly_chart(fig_risk, use_container_width=True)
        except ImportError:
            st.write(df_sample["churn_risk"].value_counts())

    st.divider()

    with st.expander("About These Metrics"):
        st.write(
            "**Revenue** is the cumulative total of all order amounts. "
            "The delta shows change from the same period last month.\n\n"
            "**High Churn Risk** is the percentage of customers flagged by the "
            "risk model (support response delay > 8 hours AND declining order "
            "frequency). A negative delta is good.\n\n"
            "**NPS Score** is measured via quarterly stakeholder surveys. "
            "Scores above 50 are considered Excellent."
        )


# -----------------------------------------------------------------------
# TRENDS PAGE
# -----------------------------------------------------------------------
elif page == "Trends":
    st.title("Trend Analysis")
    st.caption("Time-series performance over the past 6 months")

    st.header("Revenue Trends")
    st.subheader("Daily Revenue -- Last 180 Days")

    try:
        import plotly.express as px
        fig_rev = px.line(
            df_sample, x="date", y="revenue",
            title="Cumulative Revenue Growth",
            labels={"revenue": "Revenue ($)", "date": "Date"},
            template="plotly_white",
            color_discrete_sequence=["#1e3a8a"]
        )
        fig_rev.update_traces(line_width=2)
        st.plotly_chart(fig_rev, use_container_width=True)
    except ImportError:
        st.line_chart(df_sample.set_index("date")["revenue"])

    st.divider()

    st.header("Customer Metrics")
    st.subheader("Active Customers and Order Volume Over Time")

    col_left, col_right = st.columns(2)
    with col_left:
        try:
            fig_cust = px.area(
                df_sample, x="date", y="customers",
                title="Cumulative Active Customers",
                labels={"customers": "Customers", "date": "Date"},
                template="plotly_white",
                color_discrete_sequence=["#3b82f6"]
            )
            st.plotly_chart(fig_cust, use_container_width=True)
        except ImportError:
            st.line_chart(df_sample.set_index("date")["customers"])

    with col_right:
        try:
            weekly_orders = df_sample.resample("W", on="date")["orders"].sum().reset_index()
            fig_orders = px.bar(
                weekly_orders, x="date", y="orders",
                title="Weekly Order Volume",
                labels={"orders": "Orders", "date": "Week"},
                template="plotly_white",
                color_discrete_sequence=["#6366f1"]
            )
            st.plotly_chart(fig_orders, use_container_width=True)
        except ImportError:
            st.bar_chart(df_sample.set_index("date")["orders"])

    st.divider()

    with st.expander("Methodology Notes"):
        st.write(
            "**Revenue** is plotted as a cumulative daily sum to show growth "
            "trajectory over the full 6-month period.\n\n"
            "**Weekly Order Volume** is aggregated using a 7-day rolling window. "
            "Data source: analytics_views.db -- vw_product_performance view."
        )


# -----------------------------------------------------------------------
# DATA UPLOAD PAGE  (Assignment 2.52 -- all 5 tasks)
# -----------------------------------------------------------------------
elif page == "Data Upload":
    st.title("Dataset Upload & Preview")
    st.caption("Upload your own CSV or JSON file for instant analysis")

    # -------------------------------------------------------------------
    # Task 1: st.file_uploader accepting CSV and JSON, None state handled
    # -------------------------------------------------------------------
    uploaded_file = st.file_uploader(
        "Upload your dataset",
        type=["csv", "json"],
        help="Supported formats: CSV (.csv) and JSON (.json)"
    )

    if uploaded_file is not None:

        # ---------------------------------------------------------------
        # Task 4: Error handling -- wrap everything in try/except.
        # Show st.error / st.warning + st.stop instead of Python traceback.
        # ---------------------------------------------------------------
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".json"):
                df = pd.read_json(uploaded_file)
            else:
                st.error(
                    "Unsupported file type: '" + uploaded_file.name +
                    "'. Please upload a .csv or .json file."
                )
                st.stop()

            if len(df) == 0:
                st.warning("The uploaded file is empty. Please check your data and try again.")
                st.stop()

        except Exception as e:
            st.error(
                "Could not read '" + uploaded_file.name +
                "'. Please check the file format and try again."
            )
            st.stop()

        # Success banner
        st.success(
            "File loaded: " + uploaded_file.name +
            " (" + str(len(df)) + " rows, " + str(len(df.columns)) + " columns)"
        )

        st.divider()

        # ---------------------------------------------------------------
        # Task 2: Automatic preview -- shape metrics, first 10 rows, column summary
        # ---------------------------------------------------------------
        st.header("Dataset Preview")

        total_nulls = df.isnull().sum().sum()
        total_cells = df.shape[0] * df.shape[1]
        null_pct = (total_nulls / total_cells * 100) if total_cells > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", f"{len(df):,}")
        with col2:
            st.metric("Columns", str(len(df.columns)))
        with col3:
            st.metric("Null %", f"{null_pct:.1f}%")

        st.divider()

        st.subheader("First 10 Rows")
        st.dataframe(df.head(10), use_container_width=True)

        st.subheader("Column Summary")
        summary = pd.DataFrame({
            "Column": df.columns,
            "Type": df.dtypes.astype(str).values,
            "Non-Null": df.notnull().sum().values,
            "Null Count": df.isnull().sum().values,
            "Null %": (df.isnull().sum() / len(df) * 100).round(1).values,
        })
        st.dataframe(summary, use_container_width=True)

        st.divider()

        # ---------------------------------------------------------------
        # Task 3: Descriptive statistics for numeric columns
        # ---------------------------------------------------------------
        st.header("Descriptive Statistics")
        st.subheader("Numeric Column Summary (count, mean, std, min, quartiles, max)")

        numeric_df = df.select_dtypes(include="number")
        if not numeric_df.empty:
            st.dataframe(numeric_df.describe(), use_container_width=True)
        else:
            st.info("No numeric columns found in this dataset.")

        # Categorical column top value counts
        cat_cols = df.select_dtypes(exclude="number").columns.tolist()
        if cat_cols:
            st.subheader("Categorical Column Value Counts")
            cat_col_sel = st.selectbox(
                "Select a categorical column to inspect",
                cat_cols,
                key="cat_col_inspect"
            )
            val_counts = df[cat_col_sel].value_counts().head(10).reset_index()
            val_counts.columns = [cat_col_sel, "Count"]
            st.dataframe(val_counts, use_container_width=True)

        st.divider()

        # ---------------------------------------------------------------
        # Task 5: Downstream usability -- uploaded data drives filters & chart
        # ---------------------------------------------------------------
        st.header("Quick Exploration")
        st.subheader("Visualise Your Uploaded Data")

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            col_vis, col_filter = st.columns([2, 1])

            with col_filter:
                selected_col = st.selectbox(
                    "Select a numeric column to visualise",
                    numeric_cols,
                    key="vis_col"
                )
                n_bins = st.slider("Number of bins", min_value=5, max_value=50, value=20)

            with col_vis:
                try:
                    import plotly.express as px
                    fig_hist = px.histogram(
                        df, x=selected_col, nbins=n_bins,
                        title=f"Distribution of {selected_col}",
                        template="plotly_white",
                        color_discrete_sequence=["#3b82f6"]
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                except ImportError:
                    st.bar_chart(df[selected_col].value_counts().head(20))

            st.divider()

            # Optional correlation heatmap for multi-numeric datasets
            if len(numeric_cols) >= 2:
                with st.expander("View Correlation Matrix"):
                    corr = df[numeric_cols].corr().round(2)
                    try:
                        fig_corr = px.imshow(
                            corr, text_auto=True,
                            color_continuous_scale="Blues",
                            title="Numeric Column Correlations",
                            template="plotly_white"
                        )
                        st.plotly_chart(fig_corr, use_container_width=True)
                    except Exception:
                        st.dataframe(corr, use_container_width=True)

        else:
            st.info("No numeric columns available for visualisation.")

        st.divider()

        # Download filtered data back out
        with st.expander("Download Processed Data"):
            csv_out = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download as CSV",
                data=csv_out,
                file_name="processed_" + uploaded_file.name.replace(".json", ".csv"),
                mime="text/csv"
            )

    else:
        # Task 1: Handle None state -- show informative placeholder
        st.info("Upload a CSV or JSON file to begin. Your data will be previewed instantly.")

        st.subheader("What you will see after upload")
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.markdown("**Dataset Shape**\nRow count, column count, and null percentage at a glance.")
        with col_p2:
            st.markdown("**Column Summary**\nData types, non-null counts, and null percentages per column.")
        with col_p3:
            st.markdown("**Descriptive Statistics**\nMean, std, min, max, and quartiles for all numeric columns.")


# -----------------------------------------------------------------------
# DATA EXPLORER PAGE
# -----------------------------------------------------------------------
elif page == "Data Explorer":
    st.title("Data Explorer")
    st.caption("Filter, inspect, and export the underlying sample dataset")

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
            value=(df_sample["date"].min().date(), df_sample["date"].max().date())
        )

    filtered = df_sample[
        df_sample["segment"].isin(segments) &
        df_sample["churn_risk"].isin(risk_tiers)
    ]
    if len(date_range) == 2:
        filtered = filtered[
            (filtered["date"].dt.date >= date_range[0]) &
            (filtered["date"].dt.date <= date_range[1])
        ]

    st.divider()

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
                        "Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"
                    },
                    template="plotly_white", nbins=20
                )
                st.plotly_chart(fig_resp, use_container_width=True)
            except ImportError:
                st.write(filtered["support_response_hours"].describe())
