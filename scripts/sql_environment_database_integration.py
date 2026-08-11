"""
SQL Environment & Database Integration
---------------------------------------
Assignment 2.37 - Kalvium SalesPulse Database Integration Pipeline

This script demonstrates production database integration for analytics:
1. Setup Database Connection (SQLAlchemy SQLite engine creation & connection test)
2. Load Cleaned DataFrame as Table (to_sql, table verification, row count query)
3. Validate Schema (inspector column types, nullability, expected datatype verification)
4. Query and Return Results (simple filtered SELECT & complex multi-metric aggregation)
5. Make Loading Repeatable (reusable function load_cleaned_data_to_database with engine return)
"""

import os
import sys
import json
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text, inspect

# Ensure UTF-8 stdout encoding on Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def create_sample_cleaned_dataset(num_records=500, seed=42):
    """
    Create a clean, structured SalesPulse customer dataset representing:
    - Enterprise (5% of base, high LTV ~$150,000)
    - SMB (40% of base, medium LTV ~$8,500)
    - Startup (55% of base, startup LTV ~$3,200)
    """
    np.random.seed(seed)
    
    n_ent = int(num_records * 0.05)
    n_smb = int(num_records * 0.40)
    n_startup = num_records - n_ent - n_smb
    
    customer_ids = list(range(1001, 1001 + num_records))
    customer_types = ['Enterprise'] * n_ent + ['SMB'] * n_smb + ['Startup'] * n_startup
    
    emails = [f"customer_{cid}@company{cid % 20}.com" for cid in customer_ids]
    
    signup_dates = pd.date_range(start='2025-01-01', periods=num_records, freq='D').strftime('%Y-%m-%d').tolist()
    
    ltv_ent = np.random.uniform(120000, 180000, size=n_ent)
    ltv_smb = np.random.uniform(4000, 12000, size=n_smb)
    ltv_startup = np.random.uniform(1500, 5000, size=n_startup)
    lifetime_values = np.concatenate([ltv_ent, ltv_smb, ltv_startup])
    
    churn_ent = (np.random.rand(n_ent) < 0.02).astype(int)
    churn_smb = (np.random.rand(n_smb) < 0.12).astype(int)
    churn_startup = (np.random.rand(n_startup) < 0.08).astype(int)
    churn_status = np.concatenate([churn_ent, churn_smb, churn_startup])
    
    regions = np.random.choice(['US', 'EU', 'APAC', 'LATAM'], size=num_records, p=[0.45, 0.30, 0.15, 0.10])
    
    df_clean = pd.DataFrame({
        'customer_id': customer_ids,
        'email': emails,
        'customer_type': customer_types,
        'signup_date': signup_dates,
        'lifetime_value': np.round(lifetime_values, 2),
        'is_churned': churn_status,
        'region': regions
    })
    
    return df_clean


def task_1_setup_database_connection(db_path='analytics.db'):
    """
    Task 1: Setup Database Connection
    - Create SQLite engine with SQLAlchemy
    - Test database connection using context manager
    - Document connection string parameterization
    """
    print("\n" + "="*65)
    print("TASK 1: SETUP DATABASE CONNECTION")
    print("="*65)
    
    # SQLite connection string
    connection_string = f'sqlite:///{db_path}'
    print(f"Database Connection String: {connection_string}")
    
    # Create SQLAlchemy engine
    engine = create_engine(connection_string, echo=False)
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 AS status"))
        val = result.scalar()
        print(f"[STATUS] Connection Test Result: {val}")
        print("✓ Database connection successful")
        
    return engine


def task_2_load_cleaned_dataframe(df_clean, engine, table_name='customers_cleaned'):
    """
    Task 2: Load Cleaned DataFrame as Table
    - Load DataFrame to database table via to_sql with if_exists='replace'
    - Verify table created using inspector
    - Check and print row count via SQL query
    """
    print("\n" + "="*65)
    print("TASK 2: LOAD CLEANED DATAFRAME AS TABLE")
    print("="*65)
    
    # Write DataFrame to SQL database table
    df_clean.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"[INFO] Loaded DataFrame with {len(df_clean)} rows to table '{table_name}'")
    
    # Verify table created using inspector
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in Database: {tables}")
    
    # Check row count via SQL query
    count_df = pd.read_sql(f"SELECT COUNT(*) as row_count FROM {table_name}", engine)
    rows_loaded = count_df.iloc[0]['row_count']
    print(f"Verified Rows Loaded via SQL: {rows_loaded}")
    
    return tables, rows_loaded


def task_3_validate_schema(engine, table_name='customers_cleaned'):
    """
    Task 3: Validate Schema
    - Inspect table schema using SQLAlchemy inspector
    - Print all column names, datatypes, and nullability flags
    - Validate actual datatypes against expected type dictionary
    """
    print("\n" + "="*65)
    print("TASK 3: VALIDATE SCHEMA")
    print("="*65)
    
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    
    print(f"TABLE SCHEMA FOR '{table_name}':")
    print(f"  {'COLUMN NAME':20} {'SQL TYPE':15} {'NULLABLE'}")
    print("  " + "-"*45)
    for col in columns:
        null_flag = "NOT NULL" if col['nullable'] == False else "NULLABLE"
        print(f"  {col['name']:20} {str(col['type']):15} {null_flag}")
        
    print("\nDATATYPE VALIDATION MATRIX:")
    expected_types = {
        'customer_id': 'INTEGER',
        'email': 'TEXT',          # SQLite text storage class
        'customer_type': 'TEXT',
        'signup_date': 'TEXT',
        'lifetime_value': 'FLOAT',# or REAL
        'is_churned': 'INTEGER',
        'region': 'TEXT'
    }
    
    validation_report = []
    for col_name, expected_type in expected_types.items():
        matched_cols = [c for c in columns if c['name'] == col_name]
        if matched_cols:
            actual_type = str(matched_cols[0]['type']).upper()
            # Flexibly match INTEGER/BIGINT/INT, TEXT/VARCHAR, FLOAT/REAL
            is_valid = (
                (expected_type == 'INTEGER' and any(t in actual_type for t in ['INT', 'INTEGER', 'BIGINT', 'SMALLINT'])) or
                (expected_type == 'FLOAT' and any(t in actual_type for t in ['FLOAT', 'REAL', 'DOUBLE', 'NUMERIC'])) or
                (expected_type == 'TEXT' and any(t in actual_type for t in ['TEXT', 'VARCHAR', 'CHAR', 'CLOB']))
            )
            status = '✓' if is_valid else '✗'
            print(f"  {status} {col_name:20} -> Expected: {expected_type:10} | Actual: {actual_type}")
            validation_report.append({
                'column': col_name,
                'expected_type': expected_type,
                'actual_type': actual_type,
                'status': 'PASSED' if is_valid else 'FAILED'
            })
        else:
            print(f"  ✗ {col_name:20} -> MISSING IN TABLE")
            validation_report.append({
                'column': col_name,
                'expected_type': expected_type,
                'actual_type': 'MISSING',
                'status': 'FAILED'
            })
            
    # Save schema validation report JSON
    os.makedirs('output', exist_ok=True)
    with open('output/schema_validation_report.json', 'w', encoding='utf-8') as f:
        json.dump(validation_report, f, indent=2)
    print("\n[OUTPUT] Saved schema validation report to: output/schema_validation_report.json")
    
    return columns, validation_report


def task_4_query_and_return_results(engine, table_name='customers_cleaned'):
    """
    Task 4: Query and Return Results
    - Execute simple filtered SELECT query from Python
    - Execute complex aggregation query with GROUP BY, AVG, COUNT, ORDER BY
    - Return results into Pandas DataFrames
    """
    print("\n" + "="*65)
    print("TASK 4: QUERY AND RETURN RESULTS")
    print("="*65)
    
    # 1. Simple filtered query
    query_simple = f"SELECT customer_id, email, customer_type, lifetime_value, region FROM {table_name} WHERE customer_type = 'Enterprise' LIMIT 5"
    results_simple = pd.read_sql(query_simple, engine)
    print(f"Query 1: Simple Filtered Query (Enterprise Customers)")
    print(results_simple.to_string(index=False))
    
    # 2. Complex aggregation query
    query_agg = f"""
    SELECT 
        customer_type,
        COUNT(*) as customer_count,
        ROUND(AVG(lifetime_value), 2) as avg_lifetime_value,
        ROUND(SUM(lifetime_value), 2) as total_revenue,
        ROUND(AVG(is_churned) * 100, 2) as churn_rate_pct
    FROM {table_name}
    GROUP BY customer_type
    ORDER BY avg_lifetime_value DESC
    """
    results_agg = pd.read_sql(query_agg, engine)
    print(f"\nQuery 2: Multi-Dimensional Aggregation Query by Segment")
    print(results_agg.to_string(index=False))
    
    # Save aggregation summary to CSV
    results_agg.to_csv('output/segment_aggregation_summary.csv', index=False)
    print(f"\n[OUTPUT] Saved aggregation query summary to: output/segment_aggregation_summary.csv")
    
    return results_simple, results_agg


def task_5_make_loading_repeatable(df_clean, db_path='analytics.db'):
    """
    Task 5: Make Loading Repeatable
    - Wrap loading and validation into reusable function load_cleaned_data_to_database
    - Verify row counts automatically
    - Return engine object for downstream queries
    - Test repeatability across multiple tables
    """
    print("\n" + "="*65)
    print("TASK 5: MAKE LOADING REPEATABLE")
    print("="*65)
    
    def load_cleaned_data_to_database(df, table_name, database_path='analytics.db'):
        """
        Load cleaned DataFrame to database - repeatable production helper.
        
        Parameters:
            df (pd.DataFrame): Cleaned input DataFrame
            table_name (str): Target SQL table name
            database_path (str): SQLite database file path
            
        Returns:
            sqlalchemy.engine.Engine: Database engine instance ready for queries
        """
        engine = create_engine(f'sqlite:///{database_path}')
        
        # Load data safely
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        # Validate row count
        count = pd.read_sql(f"SELECT COUNT(*) as ct FROM {table_name}", engine)
        rows_loaded = count.iloc[0]['ct']
        
        print(f"✓ Successfully loaded {rows_loaded} rows to SQL table '{table_name}'")
        return engine

    # Test repeatable loading function on primary table
    print("Testing repeatable function on 'customers_cleaned':")
    eng1 = load_cleaned_data_to_database(df_clean, 'customers_cleaned', db_path)
    
    # Test repeatable loading function on secondary table ('deals_cleaned')
    deals_data = pd.DataFrame({
        'deal_id': [f"D-{2000+i}" for i in range(100)],
        'customer_id': np.random.choice(df_clean['customer_id'], size=100),
        'deal_amount': np.round(np.random.uniform(500, 25000, size=100), 2),
        'stage': np.random.choice(['Closed Won', 'Closed Lost', 'In Negotiation'], size=100)
    })
    print("\nTesting repeatable function on secondary table 'deals_cleaned':")
    eng2 = load_cleaned_data_to_database(deals_data, 'deals_cleaned', db_path)
    
    # Query verifying multiple tables exist
    inspector = inspect(eng2)
    print(f"\nFinal Registered Tables in Database: {inspector.get_table_names()}")
    
    return load_cleaned_data_to_database


def generate_performance_visualization(engine):
    """Generate database query benchmark visualization plot"""
    os.makedirs('output', exist_ok=True)
    sns.set_theme(style='whitegrid')
    
    # Benchmark query times across different operations
    query_times = []
    queries = [
        ("SELECT COUNT(*)", "SELECT COUNT(*) FROM customers_cleaned"),
        ("SELECT Enterprise", "SELECT * FROM customers_cleaned WHERE customer_type = 'Enterprise'"),
        ("GROUP BY Segment", "SELECT customer_type, AVG(lifetime_value) FROM customers_cleaned GROUP BY customer_type"),
        ("JOIN Customers-Deals", "SELECT c.customer_type, COUNT(d.deal_id) FROM customers_cleaned c JOIN deals_cleaned d ON c.customer_id = d.customer_id GROUP BY c.customer_type")
    ]
    
    for label, q in queries:
        start_t = time.time()
        for _ in range(50): # Run 50 times for accurate timing
            pd.read_sql(q, engine)
        elapsed_ms = (time.time() - start_t) / 50.0 * 1000.0
        query_times.append({'query_label': label, 'execution_time_ms': elapsed_ms})
        
    bench_df = pd.DataFrame(query_times)
    
    plt.figure(figsize=(9, 4.5))
    bars = plt.barh(bench_df['query_label'], bench_df['execution_time_ms'], color='#2b5c8f', edgecolor='black', alpha=0.85)
    plt.title('SQL Query Execution Time Benchmark (SQLite / SQLAlchemy)', fontsize=13, fontweight='bold')
    plt.xlabel('Average Execution Time per Query (ms)', fontsize=11, fontweight='bold')
    plt.ylabel('Query Benchmark Type', fontsize=11, fontweight='bold')
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.05, bar.get_y() + bar.get_height()/2., f'{width:.2f} ms', ha='left', va='center', fontweight='bold')
        
    plt.tight_layout()
    plot_path = 'output/sql_query_performance.png'
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"[PLOT] Saved query performance benchmark plot: {os.path.abspath(plot_path)}")


def generate_documentation():
    """Generate technical documentation markdown file in docs/"""
    docs_dir = 'docs'
    os.makedirs(docs_dir, exist_ok=True)
    doc_path = os.path.join(docs_dir, 'SQL_ENVIRONMENT_DATABASE_INTEGRATION.md')
    
    content = """# SalesPulse SQL Environment & Database Integration

## Overview
This document outlines the architecture, database integration patterns, and schema validation standards used to establish a single, reproducible source of truth for SalesPulse analytics data.

## 1. SQLite vs. PostgreSQL Architectural Comparison
| Dimension | SQLite | PostgreSQL |
|---|---|---|
| **Architecture** | File-based, zero setup | Client-server daemon architecture |
| **Concurrency** | Single-writer file lock | Multi-user MVCC concurrent writers |
| **Scale Limit** | Ideal for datasets < 1-2 GB | Scalable to terabytes / enterprise clusters |
| **Use Case in SalesPulse** | Local analytics, development & CI testing | Production reporting & data warehouse integration |

## 2. SQLAlchemy Abstraction Layer
Using `sqlalchemy.create_engine()` allows SalesPulse analytics scripts to remain engine-agnostic:
- Development: `create_engine('sqlite:///analytics.db')`
- Production: `create_engine('postgresql://user:password@localhost:5432/salespulse_db')`

## 3. Pandas Integration Patterns
- **Writing Data**: `df.to_sql(table_name, engine, if_exists='replace', index=False)`
- **Reading Data**: `pd.read_sql(sql_query, engine)`

## 4. Schema Validation & Audit Checklist
1. **Inspection**: Use `sqlalchemy.inspect(engine).get_columns(table_name)` to audit schema definitions.
2. **Type Checking**: Verify SQL data types (`INTEGER`, `TEXT`, `FLOAT`, `DATE`) match Pandas DataFrame dtypes.
3. **Nullability Checks**: Verify non-nullable primary keys and mandatory foreign key attributes.
4. **Repeatable Pipelines**: Encapsulate ingestion logic inside reusable helper functions to prevent data fragmentation across notebooks.
"""
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OUTPUT] Saved technical documentation: {os.path.abspath(doc_path)}")


def main():
    print("="*65)
    print("SALESPULSE SQL ENVIRONMENT & DATABASE INTEGRATION ENGINE")
    print("="*65)
    
    # Data Ingestion / Generation
    print("\n[STEP 0] Ingesting Cleaned Customer Data...")
    df_clean = create_sample_cleaned_dataset(num_records=500, seed=42)
    os.makedirs('data/processed', exist_ok=True)
    df_clean.to_csv('data/processed/clean_customers.csv', index=False)
    print(f"Prepared cleaned dataset with {len(df_clean)} records.")
    
    # Task 1
    engine = task_1_setup_database_connection(db_path='analytics.db')
    
    # Task 2
    tables, rows_loaded = task_2_load_cleaned_dataframe(df_clean, engine, table_name='customers_cleaned')
    
    # Task 3
    columns, validation_report = task_3_validate_schema(engine, table_name='customers_cleaned')
    
    # Task 4
    results_simple, results_agg = task_4_query_and_return_results(engine, table_name='customers_cleaned')
    
    # Task 5
    repeatable_fn = task_5_make_loading_repeatable(df_clean, db_path='analytics.db')
    
    # Visualizations & Documentation
    generate_performance_visualization(engine)
    generate_documentation()
    
    print("\n" + "="*65)
    print("DATABASE INTEGRATION WORKFLOW COMPLETED SUCCESSFULLY!")
    print("="*65)


if __name__ == '__main__':
    main()
