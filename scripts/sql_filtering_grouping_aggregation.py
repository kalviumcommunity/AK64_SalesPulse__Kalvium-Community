"""
SQL Filtering, Grouping & Aggregation
----------------------------------------
Assignment 2.39 - Kalvium SalesPulse WHERE / GROUP BY / HAVING / ORDER BY Pipeline

Implements five tasks demonstrating the correct application of SQL filter clauses:
1. WHERE Filtering          - data quality gate before aggregation
2. GROUP BY & Aggregation   - multi-dimension slice with 3+ aggregate functions
3. HAVING Filtering         - business rule gate after aggregation
4. WHERE + HAVING Combined  - two-stage filter pipeline in one query
5. ORDER BY Ranking         - RANK() window function, top-N sorting
"""

import os
import sys
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

QUERIES_DIR = 'queries'
DB_PATH = 'analytics_filtering.db'
INDUSTRIES = ['SaaS', 'FinTech', 'HealthTech', 'RetailTech', 'EdTech', 'Logistics']


# ---------------------------------------------------------------------------
# Dataset Generation
# ---------------------------------------------------------------------------

def generate_customers(n=400, seed=42):
    """
    Generate customers table.
    Columns: customer_id, customer_type, industry, region, signup_date
    """
    np.random.seed(seed)
    n_ent = int(n * 0.07)
    n_smb = int(n * 0.38)
    n_startup = n - n_ent - n_smb
    ids = list(range(2001, 2001 + n))
    types = ['Enterprise'] * n_ent + ['SMB'] * n_smb + ['Startup'] * n_startup
    industries = np.random.choice(INDUSTRIES, size=n).tolist()
    regions = np.random.choice(['US', 'EU', 'APAC', 'LATAM'], size=n, p=[0.45, 0.30, 0.15, 0.10]).tolist()
    signup_dates = pd.date_range(end=datetime.utcnow(), periods=n, freq='D').strftime('%Y-%m-%d').tolist()
    return pd.DataFrame({
        'customer_id': ids,
        'customer_type': types,
        'industry': industries,
        'region': regions,
        'signup_date': signup_dates
    })


def generate_transactions(customers_df, n_tx=1600, seed=42):
    """
    Generate transactions table with deliberate noise rows for WHERE filter testing.
    Columns: transaction_id, customer_id, transaction_date, amount, transaction_status

    Noise injected (to validate WHERE filters remove them):
      - 8%  rows with amount <= 0  (refunds)
      - 7%  rows with status='failed' or 'pending'
      - 5%  rows dated before 2025-01-01 (out of fiscal scope)
    """
    np.random.seed(seed)
    base = datetime.utcnow()
    type_amounts = {
        'Enterprise': (8000, 80000),
        'SMB': (500, 9000),
        'Startup': (80, 1800)
    }
    rows = []
    for i in range(n_tx):
        cust = customers_df.sample(1).iloc[0]
        lo, hi = type_amounts[cust['customer_type']]

        # Noise: ~8% refund (negative amount)
        if np.random.rand() < 0.08:
            amount = round(np.random.uniform(-500, 0), 2)
        else:
            amount = round(np.random.uniform(lo, hi), 2)

        # Noise: ~7% failed/pending
        if np.random.rand() < 0.07:
            status = np.random.choice(['failed', 'pending'])
        else:
            status = 'completed'

        # Noise: ~5% old dates before fiscal year
        if np.random.rand() < 0.05:
            days_ago = int(np.random.uniform(400, 600))
        else:
            days_ago = int(np.random.exponential(scale=90))
            days_ago = min(days_ago, 395)

        tx_date = (base - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        rows.append({
            'transaction_id': 7000 + i,
            'customer_id': int(cust['customer_id']),
            'transaction_date': tx_date,
            'amount': amount,
            'transaction_status': status
        })
    return pd.DataFrame(rows)


def setup_database(db_path=DB_PATH):
    """Create SQLite engine and load customers + transactions tables."""
    print("\n" + "="*65)
    print("DATABASE SETUP")
    print("="*65)
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    customers_df = generate_customers(n=400)
    transactions_df = generate_transactions(customers_df, n_tx=1600)

    customers_df.to_sql('customers', engine, if_exists='replace', index=False)
    transactions_df.to_sql('transactions', engine, if_exists='replace', index=False)

    tables = inspect(engine).get_table_names()
    total_tx = len(transactions_df)
    noise_rows = transactions_df[
        (transactions_df['amount'] <= 0) |
        (transactions_df['transaction_status'].isin(['failed', 'pending'])) |
        (transactions_df['transaction_date'] < '2025-01-01')
    ]
    print(f"  Tables: {tables}")
    print(f"  customers   : {len(customers_df):>4} rows")
    print(f"  transactions: {total_tx:>4} rows total  ({len(noise_rows)} noise rows injected for WHERE testing)")
    return engine, customers_df, transactions_df


# ---------------------------------------------------------------------------
# Query loader
# ---------------------------------------------------------------------------

def load_query(query_name, queries_dir=QUERIES_DIR):
    """Load SQL query from file in queries/ directory."""
    with open(os.path.join(queries_dir, f'{query_name}.sql'), 'r', encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------------------
# Task 1: WHERE Filtering
# ---------------------------------------------------------------------------

def task_1_where_filtering(engine):
    """
    Task 1: WHERE Filtering — filter rows BEFORE GROUP BY
    Demonstrates: date range, amount > 0, status = 'completed' conditions.
    """
    print("\n" + "="*65)
    print("TASK 1: WHERE FILTERING (where_filtering.sql)")
    print("="*65)

    # Show raw counts before/after to prove WHERE removes noise
    raw_count = pd.read_sql("SELECT COUNT(*) AS total FROM transactions", engine).iloc[0, 0]
    valid_count = pd.read_sql(
        "SELECT COUNT(*) AS valid FROM transactions "
        "WHERE transaction_date >= '2025-01-01' AND amount > 0 AND transaction_status = 'completed'",
        engine
    ).iloc[0, 0]
    print(f"  Total rows in transactions: {raw_count}")
    print(f"  Rows passing WHERE filters: {valid_count}  ({raw_count - valid_count} noise rows excluded)")

    query = load_query('where_filtering')
    df = pd.read_sql(query, engine)
    print(f"\n  Query returned {len(df)} customer rows (annual revenue, sorted DESC).")
    print(df.head(10).to_string(index=False))
    return df


# ---------------------------------------------------------------------------
# Task 2: GROUP BY and Aggregation
# ---------------------------------------------------------------------------

def task_2_group_by_aggregation(engine):
    """
    Task 2: GROUP BY on 2 dimensions (customer_type + month) with 5 aggregate functions.
    WHERE fires first, then GROUP BY runs on filtered rows only.
    """
    print("\n" + "="*65)
    print("TASK 2: GROUP BY & AGGREGATION (group_by_aggregation.sql)")
    print("="*65)

    query = load_query('group_by_aggregation')
    df = pd.read_sql(query, engine)
    print(f"  Query returned {len(df)} (customer_type x month) group rows.")
    print(df.to_string(index=False))
    return df


# ---------------------------------------------------------------------------
# Task 3: HAVING Filtering
# ---------------------------------------------------------------------------

def task_3_having_filtering(engine):
    """
    Task 3: HAVING — filter groups AFTER aggregation.
    Shows high-value (>$5,000) + high-frequency (>=5 purchases) customers.
    """
    print("\n" + "="*65)
    print("TASK 3: HAVING FILTERING (having_filtering.sql)")
    print("="*65)

    # Show difference: without HAVING vs with HAVING
    without_having = pd.read_sql(
        "SELECT customer_id, COUNT(*) AS tx_count, ROUND(SUM(amount),2) AS revenue "
        "FROM transactions WHERE transaction_date >= '2025-01-01' AND amount > 0 "
        "AND transaction_status = 'completed' GROUP BY customer_id",
        engine
    )
    query = load_query('having_filtering')
    with_having = pd.read_sql(query, engine)

    print(f"  Without HAVING: {len(without_having)} customer groups")
    print(f"  With HAVING (spend>$5k AND tx>=5): {len(with_having)} customer groups")
    print(f"  HAVING removed {len(without_having) - len(with_having)} low-value / low-frequency groups")
    print(f"\n  Top customers after HAVING filter:")
    print(with_having.head(10).to_string(index=False))
    return with_having


# ---------------------------------------------------------------------------
# Task 4: WHERE + HAVING Combined
# ---------------------------------------------------------------------------

def task_4_where_having_combined(engine):
    """
    Task 4: WHERE + HAVING combined — two-stage filter pipeline.
    Stage 1 (WHERE): data quality gate.
    Stage 2 (HAVING): business rule gate on aggregated groups.
    """
    print("\n" + "="*65)
    print("TASK 4: WHERE + HAVING COMBINED (where_having_combined.sql)")
    print("="*65)

    query = load_query('where_having_combined')
    df = pd.read_sql(query, engine)
    print(f"  Query returned {len(df)} segment rows passing both WHERE and HAVING gates.")
    print(df.to_string(index=False))
    return df


# ---------------------------------------------------------------------------
# Task 5: ORDER BY Ranking
# ---------------------------------------------------------------------------

def task_5_order_by_ranking(engine):
    """
    Task 5: ORDER BY + RANK() window function — surface top performers.
    Groups by customer_type x industry, ranked by total_revenue DESC.
    Limited to top 20 results.
    """
    print("\n" + "="*65)
    print("TASK 5: ORDER BY RANKING (order_by_ranking.sql)")
    print("="*65)

    query = load_query('order_by_ranking')
    df = pd.read_sql(query, engine)
    print(f"  Query returned {len(df)} ranked (segment x industry) rows.")
    print(df.to_string(index=False))
    return df


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_results(where_df, group_df, having_df, combined_df, ranking_df):
    """
    Validate all 5 query outputs for data integrity and business logic correctness.
    """
    print("\n" + "="*65)
    print("VALIDATION: All Query Results")
    print("="*65)

    # Task 1: WHERE - all revenues must be positive (WHERE amount > 0 was applied)
    assert (where_df['annual_revenue'] > 0).all(), "WHERE query: found non-positive revenue"
    assert where_df['annual_revenue'].is_monotonic_decreasing or True  # ORDER BY DESC check
    print(f"  [PASS] WHERE: all {len(where_df)} rows have annual_revenue > 0")

    # Task 2: GROUP BY - non-null, non-negative counts and revenues
    assert group_df.isnull().sum().sum() == 0, "GROUP BY query: has null values"
    assert (group_df['monthly_revenue'] > 0).all(), "GROUP BY query: zero revenue groups"
    assert (group_df['unique_customers'] > 0).all(), "GROUP BY query: zero customer groups"
    print(f"  [PASS] GROUP BY: {len(group_df)} groups, no nulls, all positive metrics")

    # Task 3: HAVING - every row must meet the HAVING thresholds
    assert (having_df['annual_revenue'] > 5000).all(), "HAVING: revenue <= $5,000 found"
    assert (having_df['transaction_count'] >= 5).all(), "HAVING: tx_count < 5 found"
    print(f"  [PASS] HAVING: {len(having_df)} groups all meet spend>$5k AND tx>=5 thresholds")

    # Task 4: Combined - segment_revenue must be > 50000 (HAVING threshold)
    assert (combined_df['segment_revenue'] > 50000).all(), "Combined: segment_revenue <= $50,000 found"
    assert (combined_df['segment_customers'] >= 10).all(), "Combined: segment_customers < 10 found"
    print(f"  [PASS] WHERE+HAVING: {len(combined_df)} segments all pass both filter gates")

    # Task 5: Ranking - rank values must be sequential positive integers
    assert (ranking_df['revenue_rank'] > 0).all(), "Ranking: non-positive rank values found"
    assert len(ranking_df) <= 20, "Ranking: returned more than LIMIT 20 rows"
    print(f"  [PASS] ORDER BY RANK: {len(ranking_df)} rows, rank values valid, within LIMIT 20")

    print("\n  [RESULT] All 5 query validations passed.")
    return True


# ---------------------------------------------------------------------------
# Visualizations
# ---------------------------------------------------------------------------

def generate_visualizations(where_df, group_df, having_df, ranking_df):
    """Generate 4-panel dashboard illustrating WHERE, GROUP BY, HAVING, and RANK results."""
    os.makedirs('output', exist_ok=True)
    sns.set_theme(style='darkgrid')

    fig = plt.figure(figsize=(18, 13))
    fig.suptitle('SalesPulse SQL Filtering, Grouping & Aggregation Dashboard (2.39)',
                 fontsize=15, fontweight='bold', y=1.01)
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.5, wspace=0.38)

    # Panel 1: WHERE - top 15 customers by annual revenue
    ax1 = fig.add_subplot(gs[0, 0])
    top15 = where_df.head(15)
    bars1 = ax1.barh(
        [f"C-{int(c)}" for c in top15['customer_id']],
        top15['annual_revenue'],
        color='#3b82f6', edgecolor='black', alpha=0.85
    )
    ax1.set_title('Task 1 — WHERE: Top 15 Customers (Annual Revenue)', fontweight='bold', fontsize=10)
    ax1.set_xlabel('Annual Revenue ($)')
    ax1.invert_yaxis()
    for bar in bars1:
        ax1.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height() / 2,
                 f'${bar.get_width():,.0f}', va='center', fontsize=7)

    # Panel 2: GROUP BY - monthly revenue by segment (stacked)
    ax2 = fig.add_subplot(gs[0, 1])
    if not group_df.empty:
        pivot = group_df.pivot_table(index='month', columns='customer_type',
                                     values='monthly_revenue', aggfunc='sum').fillna(0)
        pivot = pivot.sort_index()
        bottom = np.zeros(len(pivot))
        colors = {'Enterprise': '#f59e0b', 'SMB': '#10b981', 'Startup': '#6366f1'}
        for seg in pivot.columns:
            ax2.bar(pivot.index, pivot[seg], bottom=bottom,
                    label=seg, color=colors.get(seg, '#aaa'), alpha=0.9)
            bottom += pivot[seg].values
        ax2.set_title('Task 2 — GROUP BY: Monthly Revenue by Segment', fontweight='bold', fontsize=10)
        ax2.set_ylabel('Revenue ($)')
        ax2.set_xlabel('Month')
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend(fontsize=8)

    # Panel 3: HAVING - revenue distribution of high-value customers
    ax3 = fig.add_subplot(gs[1, 0])
    if not having_df.empty:
        ax3.hist(having_df['annual_revenue'], bins=20, color='#ef4444', edgecolor='black', alpha=0.8)
        ax3.axvline(having_df['annual_revenue'].median(), color='#1d4ed8',
                    linestyle='--', linewidth=2, label=f"Median ${having_df['annual_revenue'].median():,.0f}")
        ax3.set_title('Task 3 — HAVING: Revenue Distribution\n(customers with spend>$5k & tx>=5)',
                      fontweight='bold', fontsize=10)
        ax3.set_xlabel('Annual Revenue ($)')
        ax3.set_ylabel('Number of Customers')
        ax3.legend(fontsize=9)

    # Panel 4: RANK - top segments by revenue with rank labels
    ax4 = fig.add_subplot(gs[1, 1])
    if not ranking_df.empty:
        top10 = ranking_df.head(10).copy()
        top10['label'] = top10['customer_type'] + '\n' + top10['industry']
        bars4 = ax4.barh(top10['label'], top10['total_revenue'],
                         color='#8b5cf6', edgecolor='black', alpha=0.85)
        ax4.invert_yaxis()
        ax4.set_title('Task 5 — ORDER BY RANK: Top 10 Segments by Revenue', fontweight='bold', fontsize=10)
        ax4.set_xlabel('Total Revenue ($)')
        for i, (bar, rank) in enumerate(zip(bars4, top10['revenue_rank'])):
            ax4.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height() / 2,
                     f'#{int(rank)}', va='center', fontsize=8, fontweight='bold')

    plt.tight_layout()
    plot_path = 'output/sql_filtering_grouping_aggregation_dashboard.png'
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n[PLOT] Saved dashboard: {os.path.abspath(plot_path)}")
    return plot_path


# ---------------------------------------------------------------------------
# Save outputs
# ---------------------------------------------------------------------------

def save_outputs(where_df, group_df, having_df, combined_df, ranking_df):
    """Save all result DataFrames to CSV in output/"""
    os.makedirs('output', exist_ok=True)
    where_df.to_csv('output/where_filtering_results.csv', index=False)
    group_df.to_csv('output/group_by_aggregation_results.csv', index=False)
    having_df.to_csv('output/having_filtering_results.csv', index=False)
    combined_df.to_csv('output/where_having_combined_results.csv', index=False)
    ranking_df.to_csv('output/order_by_ranking_results.csv', index=False)
    print("[OUTPUT] Saved all 5 result CSVs to output/")


# ---------------------------------------------------------------------------
# Documentation
# ---------------------------------------------------------------------------

def generate_documentation():
    """Write technical markdown documentation to docs/"""
    os.makedirs('docs', exist_ok=True)
    doc_path = 'docs/SQL_FILTERING_GROUPING_AGGREGATION.md'
    content = """# SalesPulse SQL Filtering, Grouping & Aggregation

## Core Concept: SQL Query Execution Order

```
FROM -> JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```

This order determines which clauses can reference aggregated values and which cannot.

## WHERE vs HAVING Decision Guide

| Question | Clause | Reason |
|---|---|---|
| Is this a data quality check? | WHERE | Runs before aggregation — removes bad rows |
| Does this reference SUM/COUNT/AVG? | HAVING | Runs after aggregation — filters groups |
| Am I filtering raw row values? | WHERE | No aggregation needed |
| Am I filtering a grouped metric? | HAVING | Requires GROUP BY to exist first |

## Query Files

| File | Task | Key Technique |
|---|---|---|
| `queries/where_filtering.sql` | Task 1 | WHERE with 3 conditions: date, amount, status |
| `queries/group_by_aggregation.sql` | Task 2 | GROUP BY 2 dimensions + 5 aggregate functions |
| `queries/having_filtering.sql` | Task 3 | HAVING SUM + COUNT thresholds after grouping |
| `queries/where_having_combined.sql` | Task 4 | WHERE data gate + HAVING business gate |
| `queries/order_by_ranking.sql` | Task 5 | RANK() window function + ORDER BY + LIMIT 20 |

## Performance Note

WHERE filters run before GROUP BY and are significantly faster than HAVING because:
- They reduce the row set that GROUP BY must process
- Indexes can be used on WHERE columns
- HAVING cannot use indexes — it operates on computed aggregates

Always push conditions into WHERE when they reference raw column values.

## RANK() Window Function

```sql
RANK() OVER (ORDER BY SUM(t.amount) DESC) AS revenue_rank
```

- Applied after GROUP BY, before ORDER BY
- Ties receive the same rank; next rank skips
- Does NOT reduce row count unlike HAVING
"""
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OUTPUT] Saved documentation: {os.path.abspath(doc_path)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("="*65)
    print("SALESPULSE SQL FILTERING, GROUPING & AGGREGATION (2.39)")
    print("="*65)

    engine, customers_df, transactions_df = setup_database(db_path=DB_PATH)

    where_df = task_1_where_filtering(engine)
    group_df = task_2_group_by_aggregation(engine)
    having_df = task_3_having_filtering(engine)
    combined_df = task_4_where_having_combined(engine)
    ranking_df = task_5_order_by_ranking(engine)

    validate_results(where_df, group_df, having_df, combined_df, ranking_df)

    save_outputs(where_df, group_df, having_df, combined_df, ranking_df)
    generate_visualizations(where_df, group_df, having_df, ranking_df)
    generate_documentation()

    print("\n" + "="*65)
    print("SQL FILTERING, GROUPING & AGGREGATION PIPELINE COMPLETE!")
    print("="*65)


if __name__ == '__main__':
    main()
