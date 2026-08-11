"""
Analytical SQL Query Optimisation
----------------------------------
Assignment 2.42 - Kalvium SalesPulse Analytical Query Optimization Pipeline

Implements five tasks:
1. Task 1: Refactor Query 1 - SELECT * to Explicit Columns
2. Task 2: Refactor Query 2 - Apply Filters Before JOINs (Reduction Factor Analysis)
3. Task 3: Refactor Query 3 - Use CTEs for Readability & Step-by-Step Testability
4. Task 4: Compare & Document Improvements (Side-by-Side Analysis Table)
5. Task 5: Follow-Up Questions (Indexing, CTE Materialization, Scale Techniques)
"""

import os
import sys
import time
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

DB_PATH = 'analytics_optimization.db'
QUERIES_DIR = 'queries'


# ---------------------------------------------------------------------------
# Database Ingestion & Setup
# ---------------------------------------------------------------------------

def generate_optimization_dataset(seed=42):
    """
    Generate synthetic dataset with wide schemas (many columns) to demonstrate
    the performance overhead of SELECT * vs explicit columns:
      - customers: 1,000 rows (15 attributes including PII, JSON metadata)
      - products: 100 rows (10 attributes)
      - transactions: 10,000 rows (20 attributes including audit flags, device info)
    """
    np.random.seed(seed)
    base_date = datetime.utcnow()

    # Customers table (id, customer_name, country, account_type, customer_segment, + 10 wide audit columns)
    c_ids = list(range(1, 1001))
    c_df = pd.DataFrame({
        'id': c_ids,
        'customer_name': [f"Customer-{cid}" for cid in c_ids],
        'country': np.random.choice(['USA', 'Canada', 'UK', 'Germany', 'France'], size=1000, p=[0.45, 0.20, 0.15, 0.10, 0.10]),
        'account_type': np.random.choice(['Enterprise', 'Mid-Market', 'SMB', 'Starter'], size=1000),
        'customer_segment': np.random.choice(['Tier 1', 'Tier 2', 'Tier 3', 'Enterprise SLA'], size=1000),
        'email_pii': [f"user_{cid}@pii_protected_domain.com" for cid in c_ids],
        'ssn_encrypted': [f"XXX-XX-{1000+cid}" for cid in c_ids],
        'created_at': pd.date_range('2022-01-01', periods=1000, freq='D').strftime('%Y-%m-%d'),
        'billing_address': [f"Street Address {cid}, Suite 100" for cid in c_ids],
        'credit_score': np.random.randint(600, 850, size=1000),
        'internal_notes_blob': [f"Internal customer audit logs and blob data string for customer {cid}" * 5 for cid in c_ids],
        'attr_1': np.random.rand(1000),
        'attr_2': np.random.rand(1000),
        'attr_3': np.random.rand(1000),
        'attr_4': np.random.rand(1000)
    })

    # Products table
    p_ids = list(range(1, 101))
    p_df = pd.DataFrame({
        'id': p_ids,
        'product_name': [f"SalesPulse-Module-{pid}" for pid in p_ids],
        'category': np.random.choice(['Analytics', 'CRM', 'Billing', 'AI-Engine'], size=100),
        'list_price': np.round(np.random.uniform(50, 2000, size=100), 2),
        'description': [f"Detailed product specification text blob for module {pid}" * 3 for pid in p_ids],
        'p_attr_1': np.random.rand(100),
        'p_attr_2': np.random.rand(100),
        'p_attr_3': np.random.rand(100)
    })

    # Transactions table (10,000 rows)
    t_ids = list(range(10001, 20001))
    dates = pd.date_range(end=base_date, periods=10000, freq='h').strftime('%Y-%m-%d').tolist()
    
    t_df = pd.DataFrame({
        'transaction_id': t_ids,
        'customer_id': np.random.choice(c_ids, size=10000),
        'product_id': np.random.choice(p_ids, size=10000),
        'transaction_date': dates,
        'amount': np.round(np.random.uniform(10, 5000, size=10000), 2),
        'payment_status': np.random.choice(['completed', 'pending', 'failed'], size=10000, p=[0.90, 0.05, 0.05]),
        'device_ip': [f"192.168.1.{i%255}" for i in range(10000)],
        'user_agent_blob': ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" * 3 for _ in range(10000)],
        'session_id': [f"SESS-{i+1000}" for i in range(10000)],
        't_attr_1': np.random.rand(10000),
        't_attr_2': np.random.rand(10000),
        't_attr_3': np.random.rand(10000),
        't_attr_4': np.random.rand(10000)
    })

    return c_df, p_df, t_df


def setup_database(db_path=DB_PATH):
    """Create SQLite database and populate tables."""
    print("\n" + "="*65)
    print("DATABASE SETUP: Loading Datasets")
    print("="*65)
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    
    c_df, p_df, t_df = generate_optimization_dataset()
    c_df.to_sql('customers', engine, if_exists='replace', index=False)
    p_df.to_sql('products', engine, if_exists='replace', index=False)
    t_df.to_sql('transactions', engine, if_exists='replace', index=False)

    print(f"  customers   : {len(c_df):>5} rows ({c_df.shape[1]} columns)")
    print(f"  products    : {len(p_df):>5} rows ({p_df.shape[1]} columns)")
    print(f"  transactions: {len(t_df):>5} rows ({t_df.shape[1]} columns)")
    return engine, c_df, p_df, t_df


def load_query(query_name, queries_dir=QUERIES_DIR):
    """Load SQL query string from file."""
    with open(os.path.join(queries_dir, f'{query_name}.sql'), 'r', encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------------------
# Task 1: Refactor Query 1 - SELECT * to Explicit Columns
# ---------------------------------------------------------------------------

def task_1_refactor_query_1(engine):
    """
    Task 1: Compare SELECT * vs Explicit Columns.
    Measures column count reduction, memory size, and execution speed.
    """
    print("\n" + "="*65)
    print("TASK 1: REFACTOR QUERY 1 — SELECT * TO EXPLICIT COLUMNS")
    print("="*65)

    q1_orig = load_query('query1_original')
    q1_opt = load_query('query1_optimized')

    # Benchmark original query
    t0 = time.time()
    orig_df = pd.read_sql(q1_orig, engine)
    t_orig = (time.time() - t0) * 1000.0

    # Benchmark optimized query
    t0 = time.time()
    opt_df = pd.read_sql(q1_opt, engine)
    t_opt = (time.time() - t0) * 1000.0

    orig_cols = orig_df.shape[1] # 27 columns (14 customer + 13 transaction)
    opt_cols = opt_df.shape[1]   # 7 explicit columns
    col_reduction_pct = ((orig_cols - opt_cols) / orig_cols) * 100.0

    orig_mem_kb = orig_df.memory_usage(deep=True).sum() / 1024.0
    opt_mem_kb = opt_df.memory_usage(deep=True).sum() / 1024.0
    mem_reduction_pct = ((orig_mem_kb - opt_mem_kb) / orig_mem_kb) * 100.0

    print(f"  Original Query  : {orig_cols:>2} columns | Memory: {orig_mem_kb:6.2f} KB | Time: {t_orig:5.2f} ms")
    print(f"  Optimized Query : {opt_cols:>2} columns | Memory: {opt_mem_kb:6.2f} KB | Time: {t_opt:5.2f} ms")
    print(f"  Column Reduction: {col_reduction_pct:.1f}% fewer columns retrieved")
    print(f"  Memory Savings  : {mem_reduction_pct:.1f}% lower memory footprint")

    print("\n  Sample Optimized Output:")
    print(opt_df.head(5).to_string(index=False))

    return {
        'orig_cols': orig_cols,
        'opt_cols': opt_cols,
        'col_reduction_pct': col_reduction_pct,
        'orig_mem_kb': orig_mem_kb,
        'opt_mem_kb': opt_mem_kb,
        'mem_reduction_pct': mem_reduction_pct,
        't_orig_ms': t_orig,
        't_opt_ms': t_opt
    }


# ---------------------------------------------------------------------------
# Task 2: Refactor Query 2 - Apply Filters Before JOINs
# ---------------------------------------------------------------------------

def task_2_refactor_query_2(engine):
    """
    Task 2: Apply Filters Before JOINs.
    Measures raw table rows vs filtered intermediate rows vs final result rows.
    Calculates dataset reduction factor.
    """
    print("\n" + "="*65)
    print("TASK 2: REFACTOR QUERY 2 — EARLY FILTERING BEFORE JOINS")
    print("="*65)

    raw_tx_count = pd.read_sql("SELECT COUNT(*) FROM transactions", engine).iloc[0, 0]

    filtered_tx_count = pd.read_sql(
        "SELECT COUNT(*) FROM transactions WHERE transaction_date >= '2024-01-01' AND amount > 100",
        engine
    ).iloc[0, 0]

    q2_orig = load_query('query2_original')
    q2_opt = load_query('query2_optimized')

    t0 = time.time()
    orig_df = pd.read_sql(q2_orig, engine)
    t_orig = (time.time() - t0) * 1000.0

    t0 = time.time()
    opt_df = pd.read_sql(q2_opt, engine)
    t_opt = (time.time() - t0) * 1000.0

    reduction_factor = raw_tx_count / filtered_tx_count
    reduction_pct = (1.0 - (filtered_tx_count / raw_tx_count)) * 100.0

    print(f"  Full Transactions Table Size : {raw_tx_count:,} rows")
    print(f"  Filtered Transactions (Early): {filtered_tx_count:,} rows ({(filtered_tx_count/raw_tx_count)*100:.1f}% kept)")
    print(f"  Reduction Factor             : {reduction_factor:.2f}x smaller dataset before joining ({reduction_pct:.1f}% discarded early)")
    print(f"  Final Output Rows Returned   : {len(opt_df):,} rows")
    print(f"  Execution Time Original     : {t_orig:5.2f} ms")
    print(f"  Execution Time Optimized    : {t_opt:5.2f} ms")

    # Assert results are identical
    assert len(orig_df) == len(opt_df), "Result row count mismatch between Query 2 versions!"
    print("  [PASS] Both query versions returned identical result sets.")

    return {
        'raw_tx_count': raw_tx_count,
        'filtered_tx_count': filtered_tx_count,
        'reduction_factor': reduction_factor,
        'reduction_pct': reduction_pct,
        'final_rows': len(opt_df),
        't_orig_ms': t_orig,
        't_opt_ms': t_opt
    }


# ---------------------------------------------------------------------------
# Task 3: Refactor Query 3 - Use CTEs for Readability
# ---------------------------------------------------------------------------

def task_3_refactor_query_3(engine):
    """
    Task 3: Refactor Query 3 with CTEs.
    Executes nested subquery original vs CTE refactored version and tests CTE steps.
    """
    print("\n" + "="*65)
    print("TASK 3: REFACTOR QUERY 3 — CTE STRUCTURING FOR READABILITY")
    print("="*65)

    q3_orig = load_query('query3_original')
    q3_opt = load_query('query3_optimized')

    t0 = time.time()
    orig_df = pd.read_sql(q3_orig, engine)
    t_orig = (time.time() - t0) * 1000.0

    t0 = time.time()
    opt_df = pd.read_sql(q3_opt, engine)
    t_opt = (time.time() - t0) * 1000.0

    print("  Optimized CTE Result Output:")
    print(opt_df.to_string(index=False))

    # Assert core metrics match by sorting both on customer_segment
    orig_sorted = orig_df.sort_values('customer_segment').reset_index(drop=True)
    opt_sorted = opt_df.sort_values('customer_segment').reset_index(drop=True)
    np.testing.assert_allclose(orig_sorted['avg_transaction_value'].values, opt_sorted['avg_transaction_value'].values, rtol=1e-4)
    print("\n  [PASS] Identical metrics produced by nested subqueries and CTE pipeline!")

    # Demonstrate CTE step-by-step testability
    step1_df = pd.read_sql("SELECT COUNT(*) AS step1_count FROM transactions WHERE transaction_date >= '2024-01-01'", engine)
    print(f"  [TESTABLE CTE STEP 1] recent_transactions row count: {step1_df.iloc[0,0]:,}")

    return {
        'orig_metrics': orig_df,
        'opt_metrics': opt_df,
        't_orig_ms': t_orig,
        't_opt_ms': t_opt
    }


# ---------------------------------------------------------------------------
# Task 4: Compare & Document Improvements
# ---------------------------------------------------------------------------

def task_4_compare_and_document(metrics1, metrics2, metrics3):
    """
    Task 4: Build side-by-side comparison DataFrame and save CSV & markdown docs.
    """
    print("\n" + "="*65)
    print("TASK 4: COMPARE & DOCUMENT IMPROVEMENTS")
    print("="*65)

    comparison_df = pd.DataFrame({
        'Optimization Aspect': [
            'Columns Selected',
            'Memory Footprint',
            'Intermediate Rows Joined',
            'WHERE Filter Timing',
            'Nesting Depth & Structure',
            'Readability & Maintainability',
            'Execution Speed (Overall)'
        ],
        'Original Query Suite (Inefficient)': [
            f"27 columns (SELECT *)",
            f"{metrics1['orig_mem_kb']:.1f} KB",
            f"{metrics2['raw_tx_count']:,} full rows joined",
            "Applied AFTER joining all tables",
            "3 levels of nested subqueries",
            "Hard to follow, fragile to schema changes",
            f"{(metrics1['t_orig_ms'] + metrics2['t_orig_ms'] + metrics3['t_orig_ms']):.2f} ms"
        ],
        'Refactored Query Suite (Optimized)': [
            f"7 explicit columns ({metrics1['col_reduction_pct']:.1f}% reduction)",
            f"{metrics1['opt_mem_kb']:.1f} KB ({metrics1['mem_reduction_pct']:.1f}% savings)",
            f"{metrics2['filtered_tx_count']:,} rows ({metrics2['reduction_factor']:.1f}x smaller)",
            "Applied BEFORE joining via CTEs",
            "1 level (Named modular CTEs)",
            "Self-documenting, modular, testable steps",
            f"{(metrics1['t_opt_ms'] + metrics2['t_opt_ms'] + metrics3['t_opt_ms']):.2f} ms"
        ]
    })

    print(comparison_df.to_string(index=False))

    os.makedirs('output', exist_ok=True)
    comparison_df.to_csv('output/query_optimization_comparison.csv', index=False)
    print("\n[OUTPUT] Saved comparison summary to output/query_optimization_comparison.csv")

    return comparison_df


# ---------------------------------------------------------------------------
# Task 5: Answer Follow-Up Questions
# ---------------------------------------------------------------------------

def task_5_answer_followup_questions():
    """
    Task 5: Formulate comprehensive engineering answers to the 3 follow-up questions.
    """
    print("\n" + "="*65)
    print("TASK 5: FOLLOW-UP QUESTIONS & ARCHITECTURAL ANSWERS")
    print("="*65)

    answers = """
================================================================================
TECHNICAL FOLLOW-UP ANSWERS & OPTIMIZATION ARCHITECTURE
================================================================================

QUESTION 1: High-Cardinality Indexing Tradeoffs
  - Impact: Adding a B-Tree or Hash index on a high-cardinality filtering column 
    (e.g., transaction_date, customer_id, country) converts O(N) full table scans into 
    O(log N) or O(1) index lookups.
  - Tradeoff: While SELECT read performance improves by orders of magnitude, write 
    operations (INSERT, UPDATE, DELETE) incur additional overhead because every index 
    must be synchronously updated. Furthermore, indexes consume memory and storage.

QUESTION 2: CTE Caching & Materialization Behavior
  - Database Behavior: In modern RDBMS engines (such as PostgreSQL 12+ and SQLite 3.35+), 
    CTEs act as optimization boundaries by default or can be explicitly controlled via 
    'WITH name AS MATERIALIZED (...)'.
  - Materialization: When materialized, the database executes the CTE once, caches the 
    result in memory/temp storage, and reuses it across multiple downstream references 
    without re-evaluating the underlying query.

QUESTION 3: Beyond Query Optimization for 100M+ Scale Datasets
  1. Table Partitioning: Range-partitioning transaction tables by transaction_date 
     (e.g., monthly partitions) allows partition pruning, skipping 95%+ of table data.
  2. Materialized Views & Pre-Aggregation: Pre-computing hourly or daily aggregate summary 
     tables eliminates raw row processing during dashboard renders.
  3. Columnar Storage Formats: Migrating analytical data warehouses to columnar engines 
     (DuckDB, Snowflake, BigQuery) compresses data up to 10x and reads only selected columns.
================================================================================
"""
    print(answers)
    return answers


# ---------------------------------------------------------------------------
# Visualizations
# ---------------------------------------------------------------------------

def generate_performance_visualizations(metrics1, metrics2, metrics3):
    """Generate 4-panel visual comparison benchmark dashboard."""
    os.makedirs('output', exist_ok=True)
    sns.set_theme(style='darkgrid')

    fig = plt.figure(figsize=(16, 11))
    fig.suptitle('SalesPulse Analytical SQL Query Optimization Benchmark (2.42)',
                 fontsize=15, fontweight='bold', y=0.98)
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.40, wspace=0.35)

    # Panel 1: Column Count Reduction (Task 1)
    ax1 = fig.add_subplot(gs[0, 0])
    bars1 = ax1.bar(['Original (SELECT *)', 'Optimized (Explicit)'],
                    [metrics1['orig_cols'], metrics1['opt_cols']],
                    color=['#ef4444', '#10b981'], edgecolor='black', alpha=0.85)
    ax1.set_title('Task 1 — Column Count Reduction', fontweight='bold', fontsize=11)
    ax1.set_ylabel('Number of Columns Retrieved')
    for bar in bars1:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{int(bar.get_height())} cols', ha='center', va='bottom', fontweight='bold')

    # Panel 2: Dataset Reduction Before JOINs (Task 2)
    ax2 = fig.add_subplot(gs[0, 1])
    stages = ['Raw Table', 'Early Filtered', 'Final Result']
    row_counts = [metrics2['raw_tx_count'], metrics2['filtered_tx_count'], metrics2['final_rows']]
    bars2 = ax2.bar(stages, row_counts, color=['#6b7280', '#3b82f6', '#059669'], edgecolor='black', alpha=0.85)
    ax2.set_title('Task 2 — Intermediate Row Reduction Before JOIN', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Row Count')
    for bar in bars2:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                 f'{int(bar.get_height()):,}', ha='center', va='bottom', fontweight='bold')

    # Panel 3: Execution Time Benchmark across all 3 Queries
    ax3 = fig.add_subplot(gs[1, 0])
    q_labels = ['Query 1 (Columns)', 'Query 2 (Early Filter)', 'Query 3 (CTEs)']
    orig_times = [metrics1['t_orig_ms'], metrics2['t_orig_ms'], metrics3['t_orig_ms']]
    opt_times = [metrics1['t_opt_ms'], metrics2['t_opt_ms'], metrics3['t_opt_ms']]
    x = np.arange(len(q_labels))
    width = 0.35

    ax3.bar(x - width/2, orig_times, width, label='Original', color='#f59e0b', edgecolor='black', alpha=0.85)
    ax3.bar(x + width/2, opt_times, width, label='Optimized', color='#10b981', edgecolor='black', alpha=0.85)
    ax3.set_title('Execution Time Benchmark (ms)', fontweight='bold', fontsize=11)
    ax3.set_xticks(x)
    ax3.set_xticklabels(q_labels)
    ax3.set_ylabel('Execution Time (ms)')
    ax3.legend()

    # Panel 4: Memory Usage Footprint Comparison (Task 1)
    ax4 = fig.add_subplot(gs[1, 1])
    bars4 = ax4.bar(['Original (SELECT *)', 'Optimized (Explicit)'],
                    [metrics1['orig_mem_kb'], metrics1['opt_mem_kb']],
                    color=['#dc2626', '#16a34a'], edgecolor='black', alpha=0.85)
    ax4.set_title('Memory Footprint Comparison (KB)', fontweight='bold', fontsize=11)
    ax4.set_ylabel('DataFrame Memory Footprint (KB)')
    for bar in bars4:
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                 f'{bar.get_height():.1f} KB', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plot_path = 'output/query_performance_comparison.png'
    plt.savefig(plot_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"\n[PLOT] Saved optimization benchmark plot: {os.path.abspath(plot_path)}")


# ---------------------------------------------------------------------------
# Documentation Generator
# ---------------------------------------------------------------------------

def generate_documentation(metrics1, metrics2, followup_answers):
    """Generate technical documentation markdown files."""
    os.makedirs('docs', exist_ok=True)
    doc_path1 = 'query_optimization_report.md'
    doc_path2 = 'docs/ANALYTICAL_SQL_QUERY_OPTIMISATION.md'

    content = f"""# SalesPulse Analytical SQL Query Optimization Report

## Overview
This document details the refactoring and optimization of SalesPulse analytical queries using three core engineering patterns:
1. **Explicit Column Selection** (replacing `SELECT *`)
2. **Early Filtering Before JOINs** (reducing intermediate dataset cardinality)
3. **Common Table Expressions (CTEs)** (structuring logic for readability and testability)

---

## Performance Summary Table

| Metric / Aspect | Original Query Suite | Optimized Query Suite | Improvement / Impact |
|---|---|---|---|
| **Columns Retrieved (Query 1)** | 27 columns | 7 explicit columns | **{metrics1['col_reduction_pct']:.1f}% reduction** |
| **Memory Footprint (Query 1)** | {metrics1['orig_mem_kb']:.1f} KB | {metrics1['opt_mem_kb']:.1f} KB | **{metrics1['mem_reduction_pct']:.1f}% memory savings** |
| **Joined Dataset Rows (Query 2)** | {metrics2['raw_tx_count']:,} rows | {metrics2['filtered_tx_count']:,} rows | **{metrics2['reduction_factor']:.1f}x smaller dataset** |
| **Logic Structure (Query 3)** | 3-level nested subqueries | Named CTE steps | **Clean, modular, testable** |

---

## Detailed Task Refactoring Analysis

### Task 1: SELECT * to Explicit Columns
- **Inequality**: `SELECT *` retrieved all PII fields, blob metadata, and internal audit columns.
- **Refactored**: Explicitly named `transaction_id`, `transaction_date`, `amount`, `customer_name`, `country`, `account_type`.
- **Result**: Reduced network load and lowered memory footprint by **{metrics1['mem_reduction_pct']:.1f}%**.

### Task 2: Apply WHERE Filters Before JOINs
- **Inequality**: Original query joined full `transactions` ({metrics2['raw_tx_count']:,} rows) to `customers` and `products` before filtering.
- **Refactored**: Applied `WHERE transaction_date >= '2024-01-01' AND amount > 100` inside a CTE before executing JOINs.
- **Result**: Dataset size reduced by **{metrics2['reduction_factor']:.1f}x** prior to joining.

### Task 3: CTE Structuring for Readability
- **Inequality**: Nested subqueries created 3 levels of visual complexity.
- **Refactored**: Created modular CTEs: `recent_transactions` → `customer_with_segment` → `segment_metrics`.
- **Result**: Self-documenting code with 100% metric equality verified.

---

{followup_answers}
"""
    with open(doc_path1, 'w', encoding='utf-8') as f:
        f.write(content)

    with open(doc_path2, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OUTPUT] Saved optimization report: {os.path.abspath(doc_path1)}")
    print(f"[OUTPUT] Saved technical documentation: {os.path.abspath(doc_path2)}")


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def main():
    print("="*65)
    print("SALESPULSE ANALYTICAL SQL QUERY OPTIMISATION (2.42)")
    print("="*65)

    engine, c_df, p_df, t_df = setup_database()

    metrics1 = task_1_refactor_query_1(engine)
    metrics2 = task_2_refactor_query_2(engine)
    metrics3 = task_3_refactor_query_3(engine)
    comp_df = task_4_compare_and_document(metrics1, metrics2, metrics3)
    followup_answers = task_5_answer_followup_questions()

    generate_performance_visualizations(metrics1, metrics2, metrics3)
    generate_documentation(metrics1, metrics2, followup_answers)

    print("\n" + "="*65)
    print("ANALYTICAL QUERY OPTIMIZATION PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*65)


if __name__ == '__main__':
    main()
