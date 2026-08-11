"""
SQL Window Functions & Ranking Systems / Dashboard Architecture
---------------------------------------------------------------
Assignment 2.41 - Kalvium SalesPulse Hierarchical Dashboard Pipeline

Implements five tasks:
1. Task 1: Level 1 - Status (KPI summary cards design & metric justification)
2. Task 2: Level 2 - Trends (Revenue trend, active vs churned dual-line trend, AOV trend)
3. Task 3: Level 3 - Segments (Revenue by segment horizontal bar chart)
4. Task 4: Level 4 - Progressive Disclosure (Filter data, tabular explorer & CSV export)
5. Task 5: Document Design Decisions (dashboard_design.md & docs/DASHBOARD_DESIGN.md)
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from sqlalchemy import create_engine, text, inspect

# Ensure UTF-8 stdout on Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DB_PATH = 'analytics_dashboard.db'


# ---------------------------------------------------------------------------
# Database & View Creation
# ---------------------------------------------------------------------------

def setup_database_and_views(db_path=DB_PATH):
    """
    Create SQLite database with views matching dashboard design requirements:
      - vw_monthly_kpi_summary
      - agg_daily_revenue
      - agg_monthly_customer_trends
      - vw_customer_segment_revenue
    """
    print("\n" + "="*65)
    print("DATABASE & VIEWS SETUP")
    print("="*65)
    engine = create_engine(f'sqlite:///{db_path}', echo=False)

    np.random.seed(42)
    months = pd.date_range('2024-01-01', periods=12, freq='ME')
    revenue = [4.2, 4.5, 4.8, 4.6, 5.0, 5.1, 4.9, 4.7, 5.2, 5.4, 5.5, 5.2]
    active_cust = [2100, 2150, 2220, 2280, 2350, 2400, 2420, 2450, 2480, 2510, 2530, 2500]
    churned_cust = [120, 115, 130, 110, 105, 98, 102, 112, 95, 90, 88, 92]
    aov = [132, 135, 138, 136, 140, 142, 141, 139, 143, 146, 148, 145]

    monthly_df = pd.DataFrame({
        'month': months.strftime('%Y-%m'),
        'revenue_millions': revenue,
        'active_customers': active_cust,
        'churned_customers': churned_cust,
        'avg_order_value': aov
    })
    monthly_df.to_sql('agg_monthly_customer_trends', engine, if_exists='replace', index=False)

    segments = ['Enterprise', 'Mid-Market', 'SMB', 'Starter']
    segment_revenue = [2.1, 1.5, 1.0, 0.6]
    segment_df = pd.DataFrame({
        'segment': segments,
        'revenue_millions': segment_revenue,
        'customer_count': [40, 120, 350, 600]
    })
    segment_df.to_sql('vw_customer_segment_revenue', engine, if_exists='replace', index=False)

    with engine.connect() as conn:
        conn.execute(text("""
        CREATE VIEW IF NOT EXISTS vw_monthly_kpi_summary AS
        SELECT 
            '2024-12' AS period,
            5.2 AS current_revenue_m,
            12.5 AS revenue_growth_pct,
            2500 AS active_customers,
            5.2 AS customer_growth_pct,
            145 AS avg_order_value,
            3.1 AS aov_growth_pct,
            4.8 AS churn_rate_pct,
            -1.2 AS churn_rate_change,
            72 AS nps_score,
            4 AS nps_change
        """))

    inspector = inspect(engine)
    print(f"  Tables & Views created: {inspector.get_table_names() + inspector.get_view_names()}")
    return engine


# ---------------------------------------------------------------------------
# Task 1: Level 1 - Status (KPI Cards Justification)
# ---------------------------------------------------------------------------

def task_1_status_kpis(engine):
    """
    Task 1: Level 1 KPI Summary Cards
    Document and display 5 core metrics with justification.
    """
    print("\n" + "="*65)
    print("TASK 1: LEVEL 1 STATUS - KPI SUMMARY CARDS")
    print("="*65)

    kpi_df = pd.read_sql("SELECT * FROM vw_monthly_kpi_summary", engine)
    print("  Level 1 KPI Summary Card Data:")
    print(kpi_df.to_string(index=False))

    kpis = [
        {"metric": "Revenue", "value": "$5.2M", "delta": "+12.5%", "trend": "↑", "question": "What is our overall financial growth?"},
        {"metric": "Active Customers", "value": "2,500", "delta": "+5.2%", "trend": "↑", "question": "Is our active customer base expanding?"},
        {"metric": "Avg Order Value", "value": "$145", "delta": "+3.1%", "trend": "↑", "question": "Are customers purchasing higher-value packages?"},
        {"metric": "Churn Rate", "value": "4.8%", "delta": "-1.2%", "trend": "↓", "question": "Are we successfully retaining existing revenue?"},
        {"metric": "NPS Score", "value": "72", "delta": "+4 pts", "trend": "↑", "question": "What is overall user satisfaction and sentiment?"}
    ]

    print("\n  KPI Justifications & Business Questions:")
    for k in kpis:
        print(f"  • {k['metric']:18} | Val: {k['value']:6} | Delta: {k['delta']:7} | Trend: {k['trend']} | Question: {k['question']}")

    return kpi_df, kpis


# ---------------------------------------------------------------------------
# Task 2: Level 2 - Trends (Charts)
# ---------------------------------------------------------------------------

def task_2_build_trend_section(engine):
    """
    Task 2: Level 2 Trends
    Generate line charts for Revenue trend, Customer metrics trend, and AOV trend.
    Save outputs to output/revenue_trend.png and output/customer_metrics_trend.png.
    """
    print("\n" + "="*65)
    print("TASK 2: LEVEL 2 TRENDS - TIME SERIES CHARTS")
    print("="*65)

    os.makedirs('output', exist_ok=True)
    df = pd.read_sql("SELECT * FROM agg_monthly_customer_trends", engine)
    months = pd.to_datetime(df['month'])

    # Chart 1: Revenue Trend
    fig1, ax1 = plt.subplots(figsize=(10, 4.5))
    ax1.plot(months, df['revenue_millions'], marker='o', linewidth=2.2, color='#1f77b4', label='Monthly Revenue')
    ax1.axhline(y=5.0, color='#2ca02c', linestyle='--', linewidth=1.5, label='Target: $5.0M')
    ax1.set_title('Monthly Revenue Trend (2024)', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Month', fontsize=11)
    ax1.set_ylabel('Revenue ($M)', fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    plt.tight_layout()
    chart1_path = 'output/revenue_trend.png'
    plt.savefig(chart1_path, dpi=200)
    plt.close()
    print(f"  Saved Chart 1: {os.path.abspath(chart1_path)}")

    # Chart 2: Customer Metrics (Dual Line Chart)
    fig2, ax2 = plt.subplots(figsize=(10, 4.5))
    ax2.plot(months, df['active_customers'], marker='s', linewidth=2, color='#1f77b4', label='Active Customers')
    ax2_twin = ax2.twinx()
    ax2_twin.plot(months, df['churned_customers'], marker='^', linewidth=2, color='#d62728', label='Churned Customers')
    ax2.set_title('Active vs. Churned Customers Trend (2024)', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Month', fontsize=11)
    ax2.set_ylabel('Active Customers', color='#1f77b4', fontsize=11)
    ax2_twin.set_ylabel('Churned Customers', color='#d62728', fontsize=11)
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    chart2_path = 'output/customer_metrics_trend.png'
    plt.savefig(chart2_path, dpi=200)
    plt.close()
    print(f"  Saved Chart 2: {os.path.abspath(chart2_path)}")

    # Chart 3: Domain Trend (Average Order Value Trend)
    fig3, ax3 = plt.subplots(figsize=(10, 4.5))
    ax3.plot(months, df['avg_order_value'], marker='d', linewidth=2, color='#ff7f0e', label='Avg Order Value ($)')
    ax3.axhline(y=140.0, color='#6366f1', linestyle=':', linewidth=1.5, label='Benchmark: $140')
    ax3.set_title('Average Order Value (AOV) Trend (2024)', fontsize=13, fontweight='bold')
    ax3.set_xlabel('Month', fontsize=11)
    ax3.set_ylabel('AOV ($)', fontsize=11)
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=10)
    plt.tight_layout()
    chart3_path = 'output/domain_trend.png'
    plt.savefig(chart3_path, dpi=200)
    plt.close()
    print(f"  Saved Chart 3: {os.path.abspath(chart3_path)}")

    return df


# ---------------------------------------------------------------------------
# Task 3: Level 3 - Segments (Revenue by Segment Bar Chart)
# ---------------------------------------------------------------------------

def task_3_build_segment_section(engine):
    """
    Task 3: Level 3 Segments
    Horizontal bar chart for Revenue by Customer Segment with value labels.
    Save output to output/revenue_by_segment.png.
    """
    print("\n" + "="*65)
    print("TASK 3: LEVEL 3 SEGMENTS - REVENUE BY SEGMENT")
    print("="*65)

    os.makedirs('output', exist_ok=True)
    segment_df = pd.read_sql("SELECT * FROM vw_customer_segment_revenue", engine)

    segments = segment_df['segment'].tolist()
    segment_revenue = segment_df['revenue_millions'].tolist()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.barh(segments, segment_revenue, color=colors, edgecolor='black', alpha=0.85)
    ax.set_xlabel('Revenue ($M)', fontsize=11, fontweight='bold')
    ax.set_title('Revenue by Customer Segment (2024)', fontsize=13, fontweight='bold')
    ax.invert_yaxis()

    for bar, val in zip(bars, segment_revenue):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                f'${val}M', va='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    segment_chart_path = 'output/revenue_by_segment.png'
    plt.savefig(segment_chart_path, dpi=200)
    plt.close()
    print(f"  Saved Segment Chart: {os.path.abspath(segment_chart_path)}")
    print(segment_df.to_string(index=False))

    return segment_df


# ---------------------------------------------------------------------------
# Task 4: Level 4 - Progressive Disclosure & Data Explorer
# ---------------------------------------------------------------------------

def task_4_progressive_disclosure():
    """
    Task 4: Level 4 Progressive Disclosure
    Generates structured sample detail dataset and validates filtering & export capability.
    """
    print("\n" + "="*65)
    print("TASK 4: LEVEL 4 PROGRESSIVE DISCLOSURE (DATA EXPLORER)")
    print("="*65)

    np.random.seed(42)
    n_records = 400
    segments = ['Enterprise', 'Mid-Market', 'SMB', 'Starter']

    detail_df = pd.DataFrame({
        'customer_id': [f"CUST-{1000 + i}" for i in range(n_records)],
        'segment': np.random.choice(segments, size=n_records, p=[0.15, 0.30, 0.35, 0.20]),
        'revenue': np.round(np.random.uniform(500, 50000, size=n_records), 2),
        'last_activity': pd.date_range('2024-01-01', '2024-12-31', periods=n_records).strftime('%Y-%m-%d'),
        'churn_risk': np.random.choice(['Low', 'Medium', 'High'], size=n_records, p=[0.70, 0.20, 0.10])
    })

    os.makedirs('output', exist_ok=True)
    detail_df.to_csv('output/detail_customer_records.csv', index=False)
    print(f"  Saved full detail dataset ({len(detail_df)} records) to output/detail_customer_records.csv")

    # Filter demonstration
    ent_filtered = detail_df[detail_df['segment'] == 'Enterprise']
    ent_filtered.to_csv('output/filtered_enterprise_data.csv', index=False)
    print(f"  Validated Filter: Enterprise segment filtered to {len(ent_filtered)} records.")
    print("  Sample Enterprise Detail Records:")
    print(ent_filtered.head(5).to_string(index=False))

    return detail_df, ent_filtered


# ---------------------------------------------------------------------------
# Task 5: Document Design Decisions
# ---------------------------------------------------------------------------

def task_5_document_design_decisions():
    """
    Task 5: Ensure dashboard_design.md documentation is present and formatted.
    """
    print("\n" + "="*65)
    print("TASK 5: DOCUMENT DASHBOARD DESIGN DECISIONS")
    print("="*65)

    doc_path1 = 'dashboard_design.md'
    doc_path2 = 'docs/DASHBOARD_DESIGN.md'

    assert os.path.exists(doc_path1), f"Missing {doc_path1}"
    assert os.path.exists(doc_path2), f"Missing {doc_path2}"

    print(f"  [PASS] Confirmed design document at: {os.path.abspath(doc_path1)}")
    print(f"  [PASS] Confirmed design document at: {os.path.abspath(doc_path2)}")


# ---------------------------------------------------------------------------
# Visual Dashboard Summary Plot Generator
# ---------------------------------------------------------------------------

def generate_full_dashboard_summary_plot(trend_df, segment_df):
    """Generate a 4-panel complete layout overview representing Level 1 to 4."""
    os.makedirs('output', exist_ok=True)
    sns.set_theme(style='whitegrid')

    fig = plt.figure(figsize=(16, 11))
    fig.suptitle('SalesPulse Hierarchical Dashboard Overview (2.41)', fontsize=15, fontweight='bold', y=0.98)
    gs = gridspec.GridSpec(3, 2, figure=fig, height_ratios=[0.6, 1.2, 1.0], hspace=0.45, wspace=0.3)

    # Panel 1 (Level 1 Status): KPI Mock Cards
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axis('off')
    kpi_items = [
        ("Revenue", "$5.2M", "+12.5%"),
        ("Active Cust.", "2,500", "+5.2%"),
        ("AOV", "$145", "+3.1%"),
        ("Churn Rate", "4.8%", "-1.2%"),
        ("NPS Score", "72", "+4 pts")
    ]
    for i, (title, val, delta) in enumerate(kpi_items):
        x_pos = 0.05 + i * 0.19
        ax1.text(x_pos, 0.65, title, fontsize=10, fontweight='bold', color='#4b5563', transform=ax1.transAxes)
        ax1.text(x_pos, 0.25, val, fontsize=16, fontweight='bold', color='#111827', transform=ax1.transAxes)
        ax1.text(x_pos + 0.10, 0.28, delta, fontsize=10, fontweight='bold',
                 color='#16a34a' if '-' not in delta or 'Churn' in title else '#dc2626', transform=ax1.transAxes)

    # Panel 2 (Level 2 Trends): Revenue Trend
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(trend_df['month'], trend_df['revenue_millions'], marker='o', color='#1f77b4', linewidth=2)
    ax2.axhline(y=5.0, color='#2ca02c', linestyle='--', label='Target: $5M')
    ax2.set_title('Level 2 — Revenue Trend ($M)', fontweight='bold', fontsize=11)
    ax2.tick_params(axis='x', rotation=45)
    ax2.legend(fontsize=8)

    # Panel 3 (Level 2 Trends): Active vs Churned
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(trend_df['month'], trend_df['active_customers'], marker='s', color='#1f77b4', label='Active')
    ax3_t = ax3.twinx()
    ax3_t.plot(trend_df['month'], trend_df['churned_customers'], marker='^', color='#d62728', label='Churned')
    ax3.set_title('Level 2 — Customer Dynamics', fontweight='bold', fontsize=11)
    ax3.tick_params(axis='x', rotation=45)

    # Panel 4 (Level 3 Segments): Revenue by Segment
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.barh(segment_df['segment'], segment_df['revenue_millions'], color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax4.invert_yaxis()
    ax4.set_title('Level 3 — Revenue by Segment', fontweight='bold', fontsize=11)

    # Panel 5 (Level 4 Detail): Architecture summary
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.axis('off')
    ax5.text(0.05, 0.85, "Level 4 — Progressive Disclosure & Explorer", fontsize=11, fontweight='bold', color='#111827')
    ax5.text(0.05, 0.65, "• Dynamic Sidebar Filters: Segment & Churn Risk", fontsize=10, color='#374151')
    ax5.text(0.05, 0.45, "• Tabular Explorer: Searchable granular records", fontsize=10, color='#374151')
    ax5.text(0.05, 0.25, "• CSV Export: Instant download for offline analysis", fontsize=10, color='#374151')

    summary_plot_path = 'output/dashboard_layout_summary.png'
    plt.savefig(summary_plot_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[PLOT] Saved layout summary plot: {os.path.abspath(summary_plot_path)}")


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def main():
    print("="*65)
    print("SALESPULSE DASHBOARD ARCHITECTURE & HIERARCHY (2.41)")
    print("="*65)

    engine = setup_database_and_views()
    kpi_df, kpis = task_1_status_kpis(engine)
    trend_df = task_2_build_trend_section(engine)
    segment_df = task_3_build_segment_section(engine)
    detail_df, ent_filtered = task_4_progressive_disclosure()
    task_5_document_design_decisions()

    generate_full_dashboard_summary_plot(trend_df, segment_df)

    print("\n" + "="*65)
    print("DASHBOARD PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*65)


if __name__ == '__main__':
    main()
