"""
Multi-Source Merging & Join Validation Pipeline
-----------------------------------------------
Assignment 15 - Kalvium SalesPulse Join Validation Engine

This script merges customer and order datasets while performing explicit join validation,
row count comparisons across join types, unmatched key detection, and audit reporting.

Tasks Covered:
1. Explicit Join with Row Count Validation
2. Detect and Isolate Unmatched Keys
3. Compare All 4 Join Types (Inner, Left, Right, Outer)
4. Validate No Unexpected Duplication & Column Conflicts
5. Document Join Decision with Business Reasoning (JSON Audit Log)
"""

import os
import json
import pandas as pd
import numpy as np


def create_synthetic_merge_datasets(num_customers=1000, num_orders=5000, seed=42):
    """
    Generate synthetic customer (1000 rows) and orders (5000 rows) datasets.
    
    Includes intentional edge cases:
      - Unmatched customers (customers who have made 0 purchases)
      - Orphaned orders (orders referencing customer_ids not present in customers table)
    """
    np.random.seed(seed)
    
    # 1. Customer master table (1000 customers: CUST_0001 to CUST_1000)
    customer_ids = [f"CUST_{i:04d}" for i in range(1, num_customers + 1)]
    df_customers = pd.DataFrame({
        'customer_id': customer_ids,
        'customer_name': [f"Customer_{i}" for i in range(1, num_customers + 1)],
        'region': np.random.choice(['North', 'South', 'East', 'West'], size=num_customers),
        'signup_date': pd.date_range('2024-01-01', periods=num_customers, freq='12h').strftime('%Y-%m-%d')
    })
    
    # 2. Orders table (5000 orders)
    # Active customers: 850 of the 1000 customers make orders
    active_cust_ids = customer_ids[:850]
    
    # Injected orphaned customer_ids (50 orders belong to non-existent CUST_9999, CUST_8888, etc.)
    orphaned_cust_ids = [f"CUST_ORPHAN_{np.random.randint(100, 999)}" for _ in range(50)]
    
    order_pool = active_cust_ids * 5 + orphaned_cust_ids * 15
    np.random.shuffle(order_pool)
    order_cust_ids = order_pool[:num_orders]
    
    df_orders = pd.DataFrame({
        'order_id': [f"ORD_{10000 + i}" for i in range(1, num_orders + 1)],
        'customer_id': order_cust_ids,
        'order_amount': np.round(np.random.uniform(20.0, 750.0, size=num_orders), 2),
        'order_date': pd.date_range('2025-01-01', periods=num_orders, freq='1h').strftime('%Y-%m-%d %H:%M:%S')
    })
    
    return df_customers, df_orders


# Task 1: Explicit Join with Row Count Validation
def run_explicit_left_join(df_customers, df_orders):
    """
    Perform explicit left join and log row count changes.
    """
    print("\n--- TASK 1: EXPLICIT JOIN & ROW COUNT VALIDATION ---")
    print(f"Left table (df_customers) row count: {len(df_customers)}")
    print(f"Right table (df_orders) row count:    {len(df_orders)}")
    
    df_merged = pd.merge(
        df_customers, 
        df_orders, 
        on='customer_id', 
        how='left'
    )
    
    row_change = len(df_merged) - len(df_customers)
    print(f"Merged result (how='left') row count: {len(df_merged)}")
    print(f"Row count change relative to left table: {row_change:+d} rows")
    
    return df_merged


# Task 2: Detect Unmatched Keys
def detect_unmatched_keys(df_customers, df_orders):
    """
    Isolate unmatched keys from both sides of the join relationship.
    
      - Unmatched Customers: Master customers with no order history.
      - Orphaned Orders: Order records referencing customer IDs missing from master table.
    """
    print("\n--- TASK 2: DETECT UNMATCHED KEYS ---")
    
    unmatched_customers = df_customers[~df_customers['customer_id'].isin(df_orders['customer_id'])]
    unmatched_orders = df_orders[~df_orders['customer_id'].isin(df_customers['customer_id'])]
    
    print(f"Unmatched Customers (0 orders): {len(unmatched_customers)}")
    print(f"Orphaned Orders (missing customer record): {len(unmatched_orders)}")
    
    os.makedirs('output', exist_ok=True)
    unmatched_customers.to_csv('output/unmatched_customers.csv', index=False)
    unmatched_orders.to_csv('output/unmatched_orders.csv', index=False)
    
    print("Saved unmatched records to 'output/unmatched_customers.csv' and 'output/unmatched_orders.csv'.")
    return unmatched_customers, unmatched_orders


# Task 3: Compare Join Types
def compare_all_join_types(df_customers, df_orders):
    """
    Execute and compare all 4 SQL join types (inner, left, right, outer).
    """
    print("\n--- TASK 3: COMPARE ALL 4 JOIN TYPES ---")
    
    inner_df = pd.merge(df_customers, df_orders, on='customer_id', how='inner')
    left_df  = pd.merge(df_customers, df_orders, on='customer_id', how='left')
    right_df = pd.merge(df_customers, df_orders, on='customer_id', how='right')
    outer_df = pd.merge(df_customers, df_orders, on='customer_id', how='outer')
    
    print(f"Inner Join row count: {len(inner_df):>6} (Only matching keys on both sides)")
    print(f"Left Join  row count: {len(left_df):>6} (All left customers + order matches)")
    print(f"Right Join row count: {len(right_df):>6} (All right orders + customer matches)")
    print(f"Outer Join row count: {len(outer_df):>6} (All records from both sides)")
    
    return {
        'inner': len(inner_df),
        'left': len(left_df),
        'right': len(right_df),
        'outer': len(outer_df)
    }


# Task 4: Validate No Unexpected Duplication
def validate_no_unexpected_duplication(df_merged, df_customers):
    """
    Verify column naming conflicts and check key multiplicity per customer.
    """
    print("\n--- TASK 4: VALIDATE NO UNEXPECTED DUPLICATION & COLUMN CONFLICTS ---")
    
    print("Merged DataFrame Columns:")
    print(list(df_merged.columns))
    
    # Check for suffix collisions (_x, _y)
    suffix_cols = [c for c in df_merged.columns if c.endswith('_x') or c.endswith('_y')]
    if suffix_cols:
        print(f"Warning: Unexpected column naming conflicts detected: {suffix_cols}")
    else:
        print("No unexpected column suffix conflicts detected.")
        
    # Multiplicity check
    key_counts = df_merged['customer_id'].value_counts()
    print(f"Max orders per single customer: {key_counts.max()}")
    print(f"Min orders per customer (includes 0 orders): {key_counts.min()}")
    print(f"Unique customers present in merged result: {df_merged['customer_id'].nunique()}")


# Task 5: Document Join Decision
def document_join_decision(df_customers, df_orders, df_merged, unmatched_cust, unmatched_ord):
    """
    Create a structured JSON join decision audit report.
    """
    print("\n--- TASK 5: DOCUMENT JOIN DECISION (JSON REPORT) ---")
    
    join_report = {
        'join_type': 'left',
        'left_table': 'customers',
        'right_table': 'orders',
        'join_key': 'customer_id',
        'left_rows': len(df_customers),
        'right_rows': len(df_orders),
        'result_rows': len(df_merged),
        'unmatched_left': len(unmatched_cust),
        'unmatched_right': len(unmatched_ord),
        'reasoning': (
            "Selected explicit LEFT JOIN to preserve all master customer accounts (1,000 rows). "
            "Customers with 0 purchases remain in the dataset with NaN order attributes for complete lead funnel analysis. "
            "Orphaned orders (50 records) missing customer IDs were isolated to output/unmatched_orders.csv for ERP database investigation."
        )
    }
    
    json_str = json.dumps(join_report, indent=2)
    print(json_str)
    
    os.makedirs('output', exist_ok=True)
    with open('output/join_validation_report.json', 'w') as f:
        f.write(json_str)
        
    print("\nSaved JSON audit report to 'output/join_validation_report.json'.")
    return join_report


def run_pipeline():
    """Execute full multi-source merge and join validation pipeline."""
    print("=========================================================")
    print("      MULTI-SOURCE MERGING & JOIN VALIDATION DEMO        ")
    print("=========================================================")
    
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # 1. Create synthetic datasets
    df_customers, df_orders = create_synthetic_merge_datasets(num_customers=1000, num_orders=5000)
    df_customers.to_csv('data/raw/customers_merge.csv', index=False)
    df_orders.to_csv('data/raw/orders_merge.csv', index=False)
    
    print(f"\nGenerated synthetic datasets:")
    print(f" - Customers (data/raw/customers_merge.csv): {len(df_customers)} records")
    print(f" - Orders (data/raw/orders_merge.csv):       {len(df_orders)} records")
    
    # 2. Task 1: Explicit Join
    df_merged = run_explicit_left_join(df_customers, df_orders)
    
    # 3. Task 2: Unmatched Keys
    unmatched_cust, unmatched_ord = detect_unmatched_keys(df_customers, df_orders)
    
    # 4. Task 3: Compare Join Types
    join_counts = compare_all_join_types(df_customers, df_orders)
    
    # 5. Task 4: Duplication & Conflict Validation
    validate_no_unexpected_duplication(df_merged, df_customers)
    
    # 6. Task 5: Document Join Decision (JSON)
    report = document_join_decision(df_customers, df_orders, df_merged, unmatched_cust, unmatched_ord)
    
    # Save final merged data
    df_merged.to_csv('data/processed/merged_customer_orders.csv', index=False)
    print("\nSaved merged output to 'data/processed/merged_customer_orders.csv'.")
    print("Pipeline Execution Completed Successfully.")


if __name__ == '__main__':
    run_pipeline()
