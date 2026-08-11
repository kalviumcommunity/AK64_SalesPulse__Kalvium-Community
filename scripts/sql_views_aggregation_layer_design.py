"""
SQL Views & Aggregation Layer Design
--------------------------------------
Assignment 2.43 - Kalvium SalesPulse Clean Data Layer Pipeline

Implements five tasks:
1. Task 1: Create two SQL Views (vw_active_customers, vw_product_performance)
2. Task 2: Create & populate one pre-aggregated table (agg_daily_metrics) with updated_at
3. Task 3: Query views & aggregated tables from Python (simulating dashboard queries)
4. Task 4: Define & apply naming conventions (data_layer_conventions.md)
5. Task 5: View definitions committed as .sql files in database/views/ and database/aggregations/
"""

import os
import sys
import time
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

DB_PATH = 'analytics_views.db'
VIEWS_DIR = 'database/views'
AGGREGATIONS_DIR = 'database/aggregations'


# ---------------------------------------------------------------------------
# Dataset Generation
# ---------------------------------------------------------------------------

def generate_dataset(seed=42):
    """
    Generate 4 relational tables for the clean data layer:
      - customers (1,000 rows) with deleted_at field for soft-delete simulation
      - orders (5,000 rows)
      - products (50 rows) with category
      - order_items (8,000 rows)
    """
    np.random.seed(seed)
    base = datetime.utcnow()
    
    # Customers
    cust_ids = list(range(1001, 2001))
    customers_df = pd.DataFrame({
        'customer_id': cust_ids,
        'customer_name': [f"Customer-{cid}" for cid in cust_ids],
        'segment': np.random.choice(['Enterprise', 'Mid-Market', 'SMB', 'Starter'], size=1000),
        'deleted_at': [None if np.random.rand() > 0.05 else '2024-01-01' for _ in cust_ids]  # 5% soft-deleted
    })

    # Products
    prod_ids = list(range(101, 151))
    products_df = pd.DataFrame({
        'product_id': prod_ids,
        'product_name': [f"SalesPulse-Module-{pid}" for pid in prod_ids],
        'category': np.random.choice(['Analytics', 'CRM', 'Billing', 'AI-Engine'], size=50)
    })

    # Orders
    order_ids = list(range(5001, 10001))
    order_dates = [
        (base - timedelta(days=int(np.random.exponential(scale=60)))).strftime('%Y-%m-%d')
        for _ in order_ids
    ]
    product_per_order = np.random.choice(prod_ids, size=5000)
    orders_df = pd.DataFrame({
        'order_id': order_ids,
        'customer_id': np.random.choice(cust_ids, size=5000),
        'product_id': product_per_order,
        'order_date': order_dates,
        'order_amount': np.round(np.random.uniform(50, 5000, size=5000), 2)
    })

    # Order Items (multiple line items per order)
    item_rows = []
    item_id = 1
    for oid in order_ids[:2000]:  # Use 2000 orders for order_items table
        n_items = np.random.choice([1, 2, 3], p=[0.5, 0.35, 0.15])
        chosen_pids = np.random.choice(prod_ids, size=n_items, replace=False)
        for pid in chosen_pids:
            item_rows.append({
                'item_id': item_id,
                'order_id': oid,
                'product_id': pid,
                'quantity': int(np.random.randint(1, 10)),
                'unit_price': round(np.random.uniform(10, 500), 2)
            })
            item_id += 1
    order_items_df = pd.DataFrame(item_rows)

    return customers_df, products_df, orders_df, order_items_df


def setup_database(db_path=DB_PATH):
    """Create SQLite engine and load all relational tables."""
    print("\n" + "="*65)
    print("DATABASE SETUP: Loading Relational Tables")
    print("="*65)
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    c_df, p_df, o_df, oi_df = generate_dataset()
    c_df.to_sql('customers', engine, if_exists='replace', index=False)
    p_df.to_sql('products', engine, if_exists='replace', index=False)
    o_df.to_sql('orders', engine, if_exists='replace', index=False)
    oi_df.to_sql('order_items', engine, if_exists='replace', index=False)
    print(f"  customers   : {len(c_df):>5} rows (5% soft-deleted with deleted_at)")
    print(f"  products    : {len(p_df):>5} rows (4 categories)")
    print(f"  orders      : {len(o_df):>5} rows")
    print(f"  order_items : {len(oi_df):>5} rows")
    return engine, c_df, p_df, o_df, oi_df


def load_sql_file(filepath):
    """Load SQL content from file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------------------
# Task 1: Create Two SQL Views
# ---------------------------------------------------------------------------

def task_1_create_views(engine):
    """
    Task 1: Create two SQL views in the database from .sql files:
      - vw_active_customers: 30-day rolling active customer metrics
      - vw_product_performance: 90-day product revenue & buyer analytics
    """
    print("\n" + "="*65)
    print("TASK 1: CREATE TWO SQL VIEWS")
    print("="*65)

    with engine.connect() as conn:
        # Drop and recreate views
        conn.execute(text("DROP VIEW IF EXISTS vw_active_customers"))
        conn.execute(text("DROP VIEW IF EXISTS vw_product_performance"))

        vw1_sql = load_sql_file(os.path.join(VIEWS_DIR, 'vw_active_customers.sql'))
        conn.execute(text(vw1_sql))

        vw2_sql = load_sql_file(os.path.join(VIEWS_DIR, 'vw_product_performance.sql'))
        conn.execute(text(vw2_sql))

    # Verify views exist
    inspector = inspect(engine)
    views = inspector.get_view_names()
    print(f"  Registered Views: {views}")

    # Query and validate vw_active_customers
    vw1_df = pd.read_sql("SELECT * FROM vw_active_customers LIMIT 10", engine)
    print(f"\n  [VIEW 1] vw_active_customers — {len(pd.read_sql('SELECT * FROM vw_active_customers', engine))} rows")
    print(f"  Columns: {vw1_df.columns.tolist()}")
    print(vw1_df.head(5).to_string(index=False))

    # Query and validate vw_product_performance
    vw2_df = pd.read_sql("SELECT * FROM vw_product_performance LIMIT 10", engine)
    print(f"\n  [VIEW 2] vw_product_performance — {len(pd.read_sql('SELECT * FROM vw_product_performance', engine))} rows")
    print(f"  Columns: {vw2_df.columns.tolist()}")
    print(vw2_df.head(5).to_string(index=False))

    return vw1_df, vw2_df


# ---------------------------------------------------------------------------
# Task 2: Create & Populate Pre-Aggregated Table
# ---------------------------------------------------------------------------

def task_2_create_aggregated_table(engine):
    """
    Task 2: Create agg_daily_metrics table from .sql file.
    Drop existing, recreate, populate, verify updated_at, and benchmark query speed.
    """
    print("\n" + "="*65)
    print("TASK 2: CREATE PRE-AGGREGATED TABLE (agg_daily_metrics)")
    print("="*65)

    import sqlite3
    # Extract db file path from engine URL
    db_file = str(engine.url).replace('sqlite:///', '')

    conn_raw = sqlite3.connect(db_file)
    cursor = conn_raw.cursor()

    # Full refresh strategy: drop and recreate
    cursor.execute("DROP TABLE IF EXISTS agg_daily_metrics")

    # Load and execute agg SQL file via raw sqlite3 (handles DDL + DML reliably)
    agg_sql = load_sql_file(os.path.join(AGGREGATIONS_DIR, 'agg_daily_metrics.sql'))
    # Split on semicolons; strip comment-only lines
    for raw_stmt in agg_sql.split(';'):
        lines = [ln for ln in raw_stmt.splitlines() if not ln.strip().startswith('--')]
        clean = '\n'.join(lines).strip()
        if clean:
            cursor.execute(clean)

    conn_raw.commit()
    conn_raw.close()

    agg_df = pd.read_sql(
        "SELECT * FROM agg_daily_metrics ORDER BY aggregation_date DESC LIMIT 10",
        engine
    )
    total_rows = pd.read_sql("SELECT COUNT(*) FROM agg_daily_metrics", engine).iloc[0, 0]

    print(f"  Aggregated {total_rows} date x product_line rows into agg_daily_metrics")
    print(f"  Sample rows (most recent dates):")
    print(agg_df.to_string(index=False))

    # Validate updated_at is populated
    null_updated = pd.read_sql("SELECT COUNT(*) FROM agg_daily_metrics WHERE updated_at IS NULL", engine).iloc[0, 0]
    assert null_updated == 0, "ERROR: updated_at has NULL values!"
    print(f"\n  [PASS] updated_at populated for all {total_rows} rows (0 nulls)")

    # Benchmark query speed against pre-aggregated table
    t0 = time.time()
    result = pd.read_sql(
        "SELECT product_line, SUM(total_revenue) AS gross_revenue FROM agg_daily_metrics GROUP BY product_line",
        engine
    )
    elapsed_ms = (time.time() - t0) * 1000.0
    print(f"\n  [BENCHMARK] Pre-aggregated summary query: {elapsed_ms:.2f} ms")
    print(result.to_string(index=False))

    return agg_df, total_rows


# ---------------------------------------------------------------------------
# Task 3: Query Views & Aggregated Tables from Python
# ---------------------------------------------------------------------------

def task_3_query_clean_data_layer(engine):
    """
    Task 3: Demonstrate dashboard-style queries against vw_active_customers,
    vw_product_performance, and agg_daily_metrics — simulating a Streamlit dashboard.
    """
    print("\n" + "="*65)
    print("TASK 3: QUERY CLEAN DATA LAYER FROM PYTHON (DASHBOARD SIMULATION)")
    print("="*65)

    # Query 1: Top 20 active customers by 30-day revenue (direct filter on view column)
    top_active_df = pd.read_sql("""
        SELECT customer_id, customer_name, segment, revenue_30d, order_count_30d, days_since_order
        FROM vw_active_customers
        WHERE days_since_order <= 30
        ORDER BY revenue_30d DESC
        LIMIT 20
    """, engine)
    print(f"  [vw_active_customers] Top 20 Active Customers (≤30 days since last order):")
    print(top_active_df.to_string(index=False))

    # Query 2: Product performance view for Product Management Dashboard
    product_df = pd.read_sql("""
        SELECT product_name, category, total_revenue, total_orders, unique_buyers
        FROM vw_product_performance
        ORDER BY total_revenue DESC
        LIMIT 10
    """, engine)
    print(f"\n  [vw_product_performance] Top 10 Products by Revenue:")
    print(product_df.to_string(index=False))

    # Query 3: Recent 30 days from pre-aggregated table
    agg_recent_df = pd.read_sql("""
        SELECT aggregation_date, product_line, total_revenue, order_count, avg_order_value
        FROM agg_daily_metrics
        WHERE aggregation_date >= date('now', '-30 days')
        ORDER BY aggregation_date DESC
        LIMIT 10
    """, engine)
    print(f"\n  [agg_daily_metrics] Last 30 Days Revenue (sample rows):")
    print(agg_recent_df.to_string(index=False))

    # Query 4: Segment breakdown from view (executive-level filtering)
    segment_df = pd.read_sql("""
        SELECT 
            segment,
            COUNT(*) AS customer_count,
            ROUND(SUM(revenue_30d), 2) AS total_segment_revenue,
            ROUND(AVG(revenue_30d), 2) AS avg_customer_revenue
        FROM vw_active_customers
        GROUP BY segment
        ORDER BY total_segment_revenue DESC
    """, engine)
    print(f"\n  [vw_active_customers] Revenue by Segment (Executive View):")
    print(segment_df.to_string(index=False))

    return top_active_df, product_df, agg_recent_df, segment_df


# ---------------------------------------------------------------------------
# Visualizations
# ---------------------------------------------------------------------------

def generate_visualizations(segment_df, product_df, agg_df, total_rows):
    """Generate 4-panel dashboard demonstrating clean data layer output."""
    os.makedirs('output', exist_ok=True)
    sns.set_theme(style='darkgrid')

    fig = plt.figure(figsize=(16, 11))
    fig.suptitle('SalesPulse Clean Data Layer — Views & Aggregation Dashboard (2.43)',
                 fontsize=15, fontweight='bold', y=0.98)
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.35)

    # Panel 1: Segment Revenue from vw_active_customers
    ax1 = fig.add_subplot(gs[0, 0])
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    bars1 = ax1.barh(segment_df['segment'], segment_df['total_segment_revenue'],
                     color=colors[:len(segment_df)], edgecolor='black', alpha=0.85)
    ax1.invert_yaxis()
    ax1.set_title('vw_active_customers — Revenue by Segment', fontweight='bold', fontsize=11)
    ax1.set_xlabel('Total Revenue (30d, $)')
    for bar in bars1:
        ax1.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height()/2,
                 f'${bar.get_width():,.0f}', va='center', fontsize=8)

    # Panel 2: Top Products from vw_product_performance
    ax2 = fig.add_subplot(gs[0, 1])
    top8 = product_df.head(8)
    bars2 = ax2.barh(top8['product_name'], top8['total_revenue'],
                     color='#6366f1', edgecolor='black', alpha=0.85)
    ax2.invert_yaxis()
    ax2.set_title('vw_product_performance — Top Products by Revenue', fontweight='bold', fontsize=11)
    ax2.set_xlabel('Total Revenue (90d, $)')

    # Panel 3: agg_daily_metrics revenue trend by product line
    ax3 = fig.add_subplot(gs[1, 0])
    if not agg_df.empty:
        agg_df['aggregation_date'] = pd.to_datetime(agg_df['aggregation_date'])
        for pl, grp in agg_df.groupby('product_line'):
            ax3.plot(grp['aggregation_date'], grp['total_revenue'], marker='o', markersize=3, label=pl)
    ax3.set_title('agg_daily_metrics — Daily Revenue by Product Line', fontweight='bold', fontsize=11)
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Revenue ($)')
    ax3.tick_params(axis='x', rotation=30)
    ax3.legend(fontsize=8)

    # Panel 4: Data Layer Architecture (text summary)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    ax4.text(0.05, 0.92, 'Clean Data Layer Architecture', fontsize=12, fontweight='bold', color='#111827')
    ax4.text(0.05, 0.78, '  vw_  Prefix: SQL Views (stored logic, fresh on query)', fontsize=10)
    ax4.text(0.05, 0.65, '  vw_active_customers    — 30d rolling activity', fontsize=9, color='#1f77b4')
    ax4.text(0.05, 0.53, '  vw_product_performance — 90d revenue & buyers', fontsize=9, color='#1f77b4')
    ax4.text(0.05, 0.40, '  agg_  Prefix: Pre-Aggregated Tables (fast reads)', fontsize=10)
    ax4.text(0.05, 0.28, '  agg_daily_metrics      — daily pre-computed sums', fontsize=9, color='#16a34a')
    ax4.text(0.05, 0.15, f'  Total aggregated rows: {total_rows:,}', fontsize=9, color='#374151')
    ax4.text(0.05, 0.03, '  All definitions version-controlled as .sql files', fontsize=9, color='#374151')

    plt.tight_layout()
    plot_path = 'output/data_layer_dashboard.png'
    plt.savefig(plot_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"\n[PLOT] Saved dashboard: {os.path.abspath(plot_path)}")


# ---------------------------------------------------------------------------
# Task 5: Validate .sql files committed in database/ folder structure
# ---------------------------------------------------------------------------

def task_5_validate_sql_files():
    """
    Task 5: Assert all view and aggregation .sql files exist in the correct directory structure.
    """
    print("\n" + "="*65)
    print("TASK 5: VALIDATE .SQL FILES IN database/ FOLDER STRUCTURE")
    print("="*65)

    expected_files = [
        os.path.join(VIEWS_DIR, 'vw_active_customers.sql'),
        os.path.join(VIEWS_DIR, 'vw_product_performance.sql'),
        os.path.join(AGGREGATIONS_DIR, 'agg_daily_metrics.sql')
    ]

    for f in expected_files:
        assert os.path.exists(f), f"Missing .sql file: {f}"
        size_kb = os.path.getsize(f) / 1024.0
        print(f"  [PASS] {f}  ({size_kb:.1f} KB)")

    print("\n  [PASS] All view & aggregation .sql files present and version-controlled.")


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def main():
    print("="*65)
    print("SALESPULSE SQL VIEWS & AGGREGATION LAYER DESIGN (2.43)")
    print("="*65)

    engine, c_df, p_df, o_df, oi_df = setup_database()

    vw1_df, vw2_df = task_1_create_views(engine)
    agg_df, total_rows = task_2_create_aggregated_table(engine)
    top_active_df, product_df, agg_recent_df, segment_df = task_3_query_clean_data_layer(engine)

    print("\n" + "="*65)
    print("TASK 4: NAMING CONVENTIONS (see data_layer_conventions.md)")
    print("="*65)
    assert os.path.exists('data_layer_conventions.md'), "Missing data_layer_conventions.md!"
    print("  [PASS] data_layer_conventions.md exists")
    print("  Convention: vw_ prefix for views | agg_ prefix for pre-aggregated tables")
    print("  Pattern: vw_[entity]_[metric] | agg_[grain]_[subject]")
    print("  Objects created following convention:")
    print("    - vw_active_customers      (vw_[entity]_[metric])")
    print("    - vw_product_performance   (vw_[entity]_[metric])")
    print("    - agg_daily_metrics        (agg_[grain]_[subject])")

    task_5_validate_sql_files()

    full_agg_df = pd.read_sql("SELECT * FROM agg_daily_metrics", engine)
    generate_visualizations(segment_df, product_df, full_agg_df, total_rows)

    print("\n" + "="*65)
    print("SQL VIEWS & AGGREGATION LAYER PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*65)


if __name__ == '__main__':
    main()
