"""
SQL Business Metrics Query Design
-----------------------------------
Assignment 2.38 - Kalvium SalesPulse Business Metrics Pipeline

Implements five tasks:
1. Active Users Metric         - queries/monthly_active_users.sql (MAU by month + segment)
2. Revenue by Segment          - queries/revenue_by_segment.sql (JOIN + 4+ metrics/segment/month)
3. Funnel Conversion           - queries/conversion_funnel.sql (CASE WHEN conversion %)
4. Call Queries from Python    - load_query() helper + pd.read_sql execution
5. Validate Query Results      - null checks, value range asserts, logical consistency
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text, inspect

# Ensure UTF-8 stdout on Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Dataset Generation
# ---------------------------------------------------------------------------

def generate_customers(n=300, seed=42):
    """Generate synthetic customers table with customer_id, type, region."""
    np.random.seed(seed)
    ids = list(range(1001, 1001 + n))
    n_ent = int(n * 0.05)
    n_smb = int(n * 0.40)
    n_startup = n - n_ent - n_smb
    types = ['Enterprise'] * n_ent + ['SMB'] * n_smb + ['Startup'] * n_startup
    regions = np.random.choice(['US', 'EU', 'APAC', 'LATAM'], size=n, p=[0.45, 0.30, 0.15, 0.10])
    signup_dates = pd.date_range(end='2025-01-01', periods=n, freq='D').strftime('%Y-%m-%d').tolist()
    return pd.DataFrame({
        'customer_id': ids,
        'customer_type': types,
        'region': regions,
        'signup_date': signup_dates
    })


def generate_transactions(customers_df, n_tx=1200, seed=42):
    """
    Generate synthetic transactions table.
    Columns: transaction_id, order_id, customer_id, transaction_date, amount
    Dates spread across last 13 months to ensure 12-month window has data.
    """
    np.random.seed(seed)
    base_date = datetime.utcnow()

    # Enterprise: higher-value transactions; SMB: mid; Startup: low
    type_amounts = {'Enterprise': (5000, 50000), 'SMB': (500, 8000), 'Startup': (100, 1500)}
    rows = []
    for i in range(n_tx):
        cust = customers_df.sample(1, weights=None).iloc[0]
        lo, hi = type_amounts[cust['customer_type']]
        amount = round(np.random.uniform(lo, hi), 2)
        days_ago = int(np.random.exponential(scale=120))
        days_ago = min(days_ago, 395)
        tx_date = (base_date - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        rows.append({
            'transaction_id': 5000 + i,
            'order_id': 9000 + i,
            'customer_id': int(cust['customer_id']),
            'transaction_date': tx_date,
            'amount': amount
        })
    return pd.DataFrame(rows)


def generate_users(n=400, seed=42):
    """
    Generate synthetic users table for funnel metric.
    Columns: user_id, created_at, email_verified_at, first_purchase_at
    Spread created_at over past 120 days for 90-day query to return results.
    """
    np.random.seed(seed)
    base_date = datetime.utcnow()
    rows = []
    for i in range(n):
        days_ago = int(np.random.uniform(1, 120))
        created_at = (base_date - timedelta(days=days_ago)).strftime('%Y-%m-%d')

        # 75% verify email
        email_verified_at = None
        if np.random.rand() < 0.75:
            v_days = int(np.random.uniform(0, 3))
            email_verified_at = (base_date - timedelta(days=days_ago - v_days)).strftime('%Y-%m-%d')

        # 30% of all users make first purchase (conversion)
        first_purchase_at = None
        if np.random.rand() < 0.30:
            p_days = int(np.random.uniform(1, 14))
            first_purchase_at = (base_date - timedelta(days=days_ago - p_days)).strftime('%Y-%m-%d')

        rows.append({
            'user_id': 3000 + i,
            'created_at': created_at,
            'email_verified_at': email_verified_at,
            'first_purchase_at': first_purchase_at
        })
    return pd.DataFrame(rows)


def setup_database(db_path='analytics_metrics.db'):
    """Create engine, generate data, load all three source tables."""
    print("\n" + "="*65)
    print("DATABASE SETUP: Loading source tables")
    print("="*65)
    engine = create_engine(f'sqlite:///{db_path}', echo=False)

    customers_df = generate_customers(n=300)
    transactions_df = generate_transactions(customers_df, n_tx=1200)
    users_df = generate_users(n=400)

    customers_df.to_sql('customers', engine, if_exists='replace', index=False)
    transactions_df.to_sql('transactions', engine, if_exists='replace', index=False)
    users_df.to_sql('users', engine, if_exists='replace', index=False)

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"  Tables loaded: {tables}")
    print(f"  customers : {len(customers_df):>4} rows")
    print(f"  transactions: {len(transactions_df):>4} rows")
    print(f"  users       : {len(users_df):>4} rows")
    return engine, customers_df, transactions_df, users_df


# ---------------------------------------------------------------------------
# Task 4: load_query helper (central pattern used by all tasks)
# ---------------------------------------------------------------------------

def load_query(query_name, queries_dir='queries'):
    """
    Load SQL query from .sql file.

    Parameters:
        query_name (str): Filename without .sql extension (e.g. 'monthly_active_users')
        queries_dir (str): Directory containing .sql files (default: 'queries/')

    Returns:
        str: Raw SQL query string ready for pd.read_sql()
    """
    sql_path = os.path.join(queries_dir, f'{query_name}.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------------------
# Task 1: Active Users Metric
# ---------------------------------------------------------------------------

def task_1_active_users_metric(engine):
    """
    Task 1: Monthly Active Users (MAU)
    - Load and execute queries/monthly_active_users.sql via load_query()
    - Prints MAU per month with Enterprise / SMB / Startup segment breakdown
    """
    print("\n" + "="*65)
    print("TASK 1: ACTIVE USERS METRIC (monthly_active_users.sql)")
    print("="*65)

    query = load_query('monthly_active_users')
    mau_df = pd.read_sql(query, engine)

    print(f"  Query returned {len(mau_df)} month rows.")
    print(mau_df.to_string(index=False))
    return mau_df


# ---------------------------------------------------------------------------
# Task 2: Revenue by Segment
# ---------------------------------------------------------------------------

def task_2_revenue_by_segment(engine):
    """
    Task 2: Revenue by Segment
    - Load and execute queries/revenue_by_segment.sql via load_query()
    - Prints 7-column metric table: segment, month, orders, revenue, avg_order,
      unique_customers, revenue_per_customer
    """
    print("\n" + "="*65)
    print("TASK 2: REVENUE BY SEGMENT (revenue_by_segment.sql)")
    print("="*65)

    query = load_query('revenue_by_segment')
    revenue_df = pd.read_sql(query, engine)

    print(f"  Query returned {len(revenue_df)} segment-month rows.")
    print(revenue_df.to_string(index=False))
    return revenue_df


# ---------------------------------------------------------------------------
# Task 3: Funnel Conversion
# ---------------------------------------------------------------------------

def task_3_funnel_conversion(engine):
    """
    Task 3: Daily Funnel Conversion Metric
    - Load and execute queries/conversion_funnel.sql via load_query()
    - Computes: signups -> email_verified -> first_purchase -> conversion_pct
    """
    print("\n" + "="*65)
    print("TASK 3: FUNNEL CONVERSION (conversion_funnel.sql)")
    print("="*65)

    query = load_query('conversion_funnel')
    funnel_df = pd.read_sql(query, engine)

    print(f"  Query returned {len(funnel_df)} day rows.")
    print(funnel_df.head(15).to_string(index=False))
    if len(funnel_df) > 15:
        print(f"  ... ({len(funnel_df) - 15} more rows)")
    return funnel_df


# ---------------------------------------------------------------------------
# Task 4: Call Queries from Python
# ---------------------------------------------------------------------------

def task_4_call_queries_from_python(engine):
    """
    Task 4: Demonstrate the load_query() → pd.read_sql() pattern for all 3 queries.
    All teams share the same .sql files -> consistent metric numbers.
    """
    print("\n" + "="*65)
    print("TASK 4: CALL QUERIES FROM PYTHON (load_query pattern)")
    print("="*65)

    # Monthly Active Users
    mau_query = load_query('monthly_active_users')
    mau = pd.read_sql(mau_query, engine)
    print("Monthly Active Users:")
    print(mau.to_string(index=False))

    # Revenue by Segment
    revenue_query = load_query('revenue_by_segment')
    revenue = pd.read_sql(revenue_query, engine)
    print("\nRevenue by Segment:")
    print(revenue.to_string(index=False))

    # Conversion Funnel
    funnel_query = load_query('conversion_funnel')
    funnel = pd.read_sql(funnel_query, engine)
    print("\nConversion Funnel:")
    print(funnel.head(10).to_string(index=False))

    print("\n[INFO] All teams use the same .sql files -> one number, one truth.")
    return mau, revenue, funnel


# ---------------------------------------------------------------------------
# Task 5: Validate Query Results
# ---------------------------------------------------------------------------

def validate_metrics(mau_df, revenue_df, funnel_df):
    """
    Task 5: Validate metric computation integrity.

    Checks:
    - No null values in MAU or Revenue DataFrames
    - All revenue values > 0
    - Conversion percentage 0-100 range
    - Logical consistency: order_count > 0 and monthly_revenue > 0 per row

    Parameters:
        mau_df (pd.DataFrame): Monthly Active Users result
        revenue_df (pd.DataFrame): Revenue by Segment result
        funnel_df (pd.DataFrame): Conversion Funnel result

    Returns:
        bool: True if all validations pass, raises AssertionError on failure
    """
    print("\n" + "="*65)
    print("TASK 5: VALIDATE QUERY RESULTS")
    print("="*65)

    # --- Null checks ---
    mau_nulls = mau_df.isnull().sum().sum()
    revenue_nulls = revenue_df.isnull().sum().sum()
    assert mau_nulls == 0, f"MAU has {mau_nulls} null values"
    print(f"  [PASS] MAU nulls:       {mau_nulls}")

    assert revenue_nulls == 0, f"Revenue has {revenue_nulls} null values"
    print(f"  [PASS] Revenue nulls:   {revenue_nulls}")

    # --- Value range checks ---
    assert (revenue_df['monthly_revenue'] > 0).all(), "Some monthly_revenue values are <= 0"
    print(f"  [PASS] All revenue > 0  (min: ${revenue_df['monthly_revenue'].min():,.2f})")

    assert (funnel_df['conversion_pct'] >= 0).all() and (funnel_df['conversion_pct'] <= 100).all(), \
        "conversion_pct out of [0, 100] range"
    print(f"  [PASS] conversion_pct in [0, 100] range")

    # --- Logical consistency ---
    for idx, row in revenue_df.iterrows():
        assert row['order_count'] > 0, f"Row {idx}: order_count is 0"
        assert row['monthly_revenue'] > 0, f"Row {idx}: monthly_revenue is 0"
    print(f"  [PASS] Logical consistency: all {len(revenue_df)} revenue rows have order_count > 0")

    # --- Active users sanity ---
    assert (mau_df['active_users'] > 0).all(), "Some months have 0 active users"
    print(f"  [PASS] Active users > 0 in all months (max: {mau_df['active_users'].max()})")

    # --- Funnel funnel ordering check ---
    assert (funnel_df['signups'] >= funnel_df['first_purchase']).all(), \
        "first_purchase count exceeds signups — funnel logic error"
    print(f"  [PASS] Funnel ordering: signups >= first_purchase for all days")

    print("\n  [RESULT] All metrics validated successfully.")
    return True


# ---------------------------------------------------------------------------
# Visualizations
# ---------------------------------------------------------------------------

def generate_visualizations(mau_df, revenue_df, funnel_df):
    """Generate a 3-panel metrics dashboard plot."""
    os.makedirs('output', exist_ok=True)
    sns.set_theme(style='darkgrid')

    fig = plt.figure(figsize=(18, 12))
    fig.suptitle('SalesPulse SQL Business Metrics Dashboard (2.38)', fontsize=16, fontweight='bold', y=1.01)
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    # ---- Panel 1: MAU trend ----
    ax1 = fig.add_subplot(gs[0, 0])
    if not mau_df.empty:
        mau_plot = mau_df.sort_values('month')
        ax1.plot(mau_plot['month'], mau_plot['active_users'], marker='o', color='#3b82f6', linewidth=2.2, label='Total MAU')
        ax1.fill_between(range(len(mau_plot)), mau_plot['active_users'].values, alpha=0.15, color='#3b82f6')
        ax1.set_xticks(range(len(mau_plot)))
        ax1.set_xticklabels(mau_plot['month'].tolist(), rotation=45, ha='right', fontsize=7)
        ax1.set_title('Monthly Active Users (MAU)', fontweight='bold')
        ax1.set_ylabel('Unique Active Customers')
        ax1.set_xlabel('Month')
    else:
        ax1.text(0.5, 0.5, 'No data', ha='center')

    # ---- Panel 2: MAU segment stacked bar ----
    ax2 = fig.add_subplot(gs[0, 1])
    if not mau_df.empty:
        mau_plot = mau_df.sort_values('month')
        months = mau_plot['month'].tolist()
        x = range(len(months))
        ax2.bar(x, mau_plot['enterprise_users'], label='Enterprise', color='#f59e0b')
        ax2.bar(x, mau_plot['smb_users'], bottom=mau_plot['enterprise_users'], label='SMB', color='#10b981')
        ax2.bar(x, mau_plot['startup_users'],
                bottom=(mau_plot['enterprise_users'] + mau_plot['smb_users']), label='Startup', color='#6366f1')
        ax2.set_xticks(list(x))
        ax2.set_xticklabels(months, rotation=45, ha='right', fontsize=7)
        ax2.set_title('MAU Segment Breakdown', fontweight='bold')
        ax2.set_ylabel('Active Customers')
        ax2.legend(fontsize=8)

    # ---- Panel 3: Revenue per segment (aggregate bar) ----
    ax3 = fig.add_subplot(gs[1, 0])
    if not revenue_df.empty:
        seg_rev = revenue_df.groupby('customer_type')['monthly_revenue'].sum().reset_index()
        bars = ax3.bar(seg_rev['customer_type'], seg_rev['monthly_revenue'],
                       color=['#f59e0b', '#10b981', '#6366f1'], edgecolor='black', alpha=0.85)
        ax3.set_title('Total Revenue by Segment (12 months)', fontweight='bold')
        ax3.set_ylabel('Total Revenue ($)')
        ax3.set_xlabel('Segment')
        for bar in bars:
            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + bar.get_height() * 0.01,
                     f'${bar.get_height():,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # ---- Panel 4: Daily conversion funnel scatter ----
    ax4 = fig.add_subplot(gs[1, 1])
    if not funnel_df.empty:
        funnel_plot = funnel_df.sort_values('signup_date').tail(30)
        ax4.scatter(range(len(funnel_plot)), funnel_plot['conversion_pct'],
                    c=funnel_plot['conversion_pct'], cmap='RdYlGn', s=60, zorder=3)
        ax4.axhline(funnel_plot['conversion_pct'].mean(), color='#3b82f6',
                    linestyle='--', linewidth=1.5, label=f"Avg {funnel_plot['conversion_pct'].mean():.1f}%")
        ax4.set_title('Daily Conversion Rate (last 30 days)', fontweight='bold')
        ax4.set_ylabel('Conversion % (signup → purchase)')
        ax4.set_xlabel('Day (recent 30)')
        ax4.legend(fontsize=9)

    plt.tight_layout()
    plot_path = 'output/sql_business_metrics_dashboard.png'
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n[PLOT] Saved metrics dashboard: {os.path.abspath(plot_path)}")
    return plot_path


# ---------------------------------------------------------------------------
# Save outputs
# ---------------------------------------------------------------------------

def save_outputs(mau_df, revenue_df, funnel_df):
    """Save all metric DataFrames to CSV in output/"""
    os.makedirs('output', exist_ok=True)
    mau_df.to_csv('output/mau_metric.csv', index=False)
    revenue_df.to_csv('output/revenue_by_segment_metric.csv', index=False)
    funnel_df.to_csv('output/conversion_funnel_metric.csv', index=False)
    print("[OUTPUT] Saved: output/mau_metric.csv")
    print("[OUTPUT] Saved: output/revenue_by_segment_metric.csv")
    print("[OUTPUT] Saved: output/conversion_funnel_metric.csv")


# ---------------------------------------------------------------------------
# Documentation
# ---------------------------------------------------------------------------

def generate_documentation():
    """Write technical documentation markdown to docs/"""
    os.makedirs('docs', exist_ok=True)
    doc_path = 'docs/SQL_BUSINESS_METRICS_QUERY_DESIGN.md'
    content = """# SalesPulse SQL Business Metrics Query Design

## Overview
This document describes the SQL-first metric architecture for SalesPulse analytics.
Metrics are defined once in `.sql` files under `queries/` and loaded via `load_query()` in Python.
All teams execute the same files — achieving one truth for every KPI.

## Query Files

| File | Metric | Tables Used | Key Technique |
|---|---|---|---|
| `queries/monthly_active_users.sql` | Monthly Active Users by segment | `transactions`, `customers` | `CASE WHEN` conditional aggregation |
| `queries/revenue_by_segment.sql` | Revenue per customer segment per month | `transactions`, `customers` | `JOIN` + `GROUP BY` + 4+ aggregates |
| `queries/conversion_funnel.sql` | Daily signup → purchase conversion % | `users` | `CASE WHEN` conditional counting + `ROUND` |

## Python Usage Pattern

```python
def load_query(query_name, queries_dir='queries'):
    with open(f'{queries_dir}/{query_name}.sql', 'r') as f:
        return f.read()

mau = pd.read_sql(load_query('monthly_active_users'), engine)
revenue = pd.read_sql(load_query('revenue_by_segment'), engine)
funnel = pd.read_sql(load_query('conversion_funnel'), engine)
```

## SQLite Compatibility Notes
- `strftime('%Y-%m', date_col)` replaces PostgreSQL `DATE_TRUNC('month', ...)::DATE`
- `date('now', '-12 months')` replaces PostgreSQL `NOW() - INTERVAL '12 months'`
- `CASE WHEN ... END` replaces PostgreSQL `FILTER (WHERE ...)` for maximum portability

## Validation Checks
1. Zero null values in MAU and Revenue DataFrames
2. All `monthly_revenue` values > 0
3. `conversion_pct` in [0, 100] range
4. `order_count > 0` for every revenue row
5. `signups >= first_purchase` (funnel ordering logic)
"""
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OUTPUT] Saved documentation: {os.path.abspath(doc_path)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("="*65)
    print("SALESPULSE SQL BUSINESS METRICS QUERY DESIGN (2.38)")
    print("="*65)

    # Setup DB and load source tables
    engine, customers_df, transactions_df, users_df = setup_database(db_path='analytics_metrics.db')

    # Task 1: Active Users
    mau_df = task_1_active_users_metric(engine)

    # Task 2: Revenue by Segment
    revenue_df = task_2_revenue_by_segment(engine)

    # Task 3: Funnel Conversion
    funnel_df = task_3_funnel_conversion(engine)

    # Task 4: Call Queries from Python
    mau, revenue, funnel = task_4_call_queries_from_python(engine)

    # Task 5: Validate
    validate_metrics(mau_df, revenue_df, funnel_df)

    # Outputs
    save_outputs(mau_df, revenue_df, funnel_df)
    generate_visualizations(mau_df, revenue_df, funnel_df)
    generate_documentation()

    print("\n" + "="*65)
    print("SQL BUSINESS METRICS PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*65)


if __name__ == '__main__':
    main()
