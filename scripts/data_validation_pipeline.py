"""
Data Consistency & Validation Rules Pipeline
---------------------------------------------
Assignment 14 - Kalvium SalesPulse Data Validation Engine

This script implements systematic data validation rules across 5 categories:
1. Range Checks
2. Null Constraints
3. Format Pattern Validation (Regex)
4. Business Rule Validation
5. Failure Isolation & Structured Reporting
"""

import os
import pandas as pd
import numpy as np


def create_synthetic_unvalidated_data(num_records=100, seed=42):
    """
    Generate synthetic dataset containing deliberate data quality violations.
    
    Violations Injected:
      - Future birth dates (e.g., year 2050)
      - Negative prices
      - Missing customer_id and email values
      - Malformed email strings (missing '@') and invalid phone numbers
      - Business logic violations (campaign end_date before start_date)
    """
    np.random.seed(seed)
    
    customer_ids = [f"CUST_{1000 + i}" for i in range(num_records)]
    emails = [f"user_{i}@example.com" for i in range(num_records)]
    phones = [f"98765432{i:02d}" for i in range(num_records)]
    ages = np.random.randint(20, 65, size=num_records)
    prices = np.round(np.random.uniform(20.0, 500.0, size=num_records), 2)
    
    start_dates = pd.date_range(start='2026-01-01', periods=num_records, freq='D')
    end_dates = start_dates + pd.Timedelta(days=7)
    birth_dates = pd.date_range(start='1970-01-01', periods=num_records, freq='30D')
    
    df = pd.DataFrame({
        'customer_id': customer_ids,
        'email': emails,
        'phone': phones,
        'age': ages,
        'price': prices,
        'start_date': start_dates,
        'end_date': end_dates,
        'birth_date': birth_dates
    })
    
    # Inject deliberate violations
    # 1. Invalid age and future birth dates
    df.loc[3, 'age'] = -10
    df.loc[7, 'age'] = 180
    df.loc[12, 'birth_date'] = pd.Timestamp('2050-06-15')
    
    # 2. Negative price
    df.loc[15, 'price'] = -150.00
    df.loc[22, 'price'] = -45.50
    
    # 3. Null constraints
    df.loc[5, 'customer_id'] = np.nan
    df.loc[18, 'email'] = np.nan
    
    # 4. Malformed format patterns
    df.loc[25, 'email'] = 'invalid_email_string.com'
    df.loc[30, 'phone'] = '12345'  # Invalid phone (less than 10 digits)
    
    # 5. Business rule violation: end_date before start_date
    df.loc[40, 'start_date'] = pd.Timestamp('2026-05-10')
    df.loc[40, 'end_date'] = pd.Timestamp('2026-05-01')
    
    df.loc[45, 'start_date'] = pd.Timestamp('2026-06-20')
    df.loc[45, 'end_date'] = pd.Timestamp('2026-06-15')
    
    return df


# Task 1: Range Checks
def run_range_checks(df):
    """
    Validate numeric boundaries and date range constraints.
    
    Rules:
      - valid_age: 0 <= age <= 150
      - valid_price: price >= 0
      - valid_date: '1920-01-01' <= birth_date <= current_timestamp
    """
    df_val = df.copy()
    print("\n--- TASK 1: RANGE CHECKS ---")
    
    now_ts = pd.Timestamp.now()
    min_birth = pd.Timestamp('1920-01-01')
    
    df_val['valid_age'] = (df_val['age'] >= 0) & (df_val['age'] <= 150)
    df_val['valid_price'] = df_val['price'] >= 0
    df_val['valid_date'] = (df_val['birth_date'] >= min_birth) & (df_val['birth_date'] <= now_ts)
    
    invalid_age_count = (~df_val['valid_age']).sum()
    invalid_price_count = (~df_val['valid_price']).sum()
    invalid_date_count = (~df_val['valid_date']).sum()
    
    print(f"Invalid Age violations (< 0 or > 150): {invalid_age_count}")
    print(f"Invalid Price violations (< 0): {invalid_price_count}")
    print(f"Invalid Birth Date violations (< 1920 or future): {invalid_date_count}")
    
    return df_val


# Task 2: Null Constraints
def run_null_constraints(df):
    """
    Ensure critical columns never contain null values.
    
    Rules:
      - valid_customer_id: customer_id is not null
      - valid_email: email is not null
    """
    df_val = df.copy()
    print("\n--- TASK 2: NULL CONSTRAINTS ---")
    
    df_val['valid_customer_id'] = df_val['customer_id'].notna()
    df_val['valid_email'] = df_val['email'].notna()
    
    missing_cust_id = (~df_val['valid_customer_id']).sum()
    missing_email = (~df_val['valid_email']).sum()
    
    print(f"Missing customer ID violations: {missing_cust_id}")
    print(f"Missing email violations: {missing_email}")
    
    return df_val


# Task 3: Format Pattern Validation
def run_format_pattern_checks(df):
    r"""
    Validate text structure against regex patterns.
    
    Rules:
      - valid_email_format: contains '@' symbol
      - valid_phone: matches exactly 10 digits r'^\d{10}$'
    """
    df_val = df.copy()
    print("\n--- TASK 3: FORMAT PATTERN VALIDATION ---")
    
    df_val['valid_email_format'] = df_val['email'].str.contains('@', na=False)
    df_val['valid_phone'] = df_val['phone'].str.match(r'^\d{10}$', na=False)
    
    invalid_email_fmt = (~df_val['valid_email_format']).sum()
    invalid_phone_fmt = (~df_val['valid_phone']).sum()
    
    print(f"Malformed email violations (missing '@'): {invalid_email_fmt}")
    print(f"Malformed phone violations (not 10 digits): {invalid_phone_fmt}")
    
    return df_val


# Task 4: Business Rule Validation
def run_business_rule_checks(df):
    """
    Validate domain-specific cross-column business rules.
    
    Rules:
      - valid_date_order: end_date >= start_date
    """
    df_val = df.copy()
    print("\n--- TASK 4: BUSINESS RULE VALIDATION ---")
    
    df_val['valid_date_order'] = df_val['end_date'] >= df_val['start_date']
    invalid_date_order = (~df_val['valid_date_order']).sum()
    
    print(f"Business Rule violations (end_date < start_date): {invalid_date_order}")
    
    return df_val


# Task 5: Validation Report & Failure Isolation
def generate_validation_report_and_isolate(df):
    """
    Combine all validation checks, isolate failing records, and build a summary report.
    """
    df_val = df.copy()
    print("\n--- TASK 5: VALIDATION REPORT & FAILURE ISOLATION ---")
    
    validation_cols = [
        'valid_age', 
        'valid_price', 
        'valid_date', 
        'valid_customer_id', 
        'valid_email',
        'valid_email_format', 
        'valid_phone',
        'valid_date_order'
    ]
    
    df_val['passes_all_checks'] = df_val[validation_cols].all(axis=1)
    
    # Separate passed vs failed records
    df_clean = df_val[df_val['passes_all_checks']]
    failures = df_val[~df_val['passes_all_checks']]
    
    os.makedirs('output', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    failures.to_csv('output/validation_failures.csv', index=False)
    df_clean.to_csv('data/processed/clean_validated_data.csv', index=False)
    
    print(f"Total Dataset Records Processed: {len(df_val)}")
    print(f"Passed All Validation Checks:  {len(df_clean)} ({(len(df_clean)/len(df_val))*100:.2f}%)")
    print(f"Failed One or More Validation Checks: {len(failures)} ({(len(failures)/len(df_val))*100:.2f}%)")
    
    # Construct detailed rule summary report table
    total_records = len(df_val)
    report_rows = []
    
    rule_descriptions = {
        'valid_age': ('Range Check', '0 <= age <= 150'),
        'valid_price': ('Range Check', 'price >= 0'),
        'valid_date': ('Range Check', '1920-01-01 <= birth_date <= current_time'),
        'valid_customer_id': ('Null Constraint', 'customer_id is NOT NULL'),
        'valid_email': ('Null Constraint', 'email is NOT NULL'),
        'valid_email_format': ('Format Pattern', "email contains '@'"),
        'valid_phone': ('Format Pattern', 'phone is 10 digits'),
        'valid_date_order': ('Business Rule', 'end_date >= start_date')
    }
    
    for col in validation_cols:
        pass_cnt = df_val[col].sum()
        fail_cnt = (~df_val[col]).sum()
        category, desc = rule_descriptions[col]
        
        report_rows.append({
            'rule_name': col,
            'category': category,
            'condition': desc,
            'total_tested': total_records,
            'pass_count': pass_cnt,
            'fail_count': fail_cnt,
            'pass_rate_pct': round((pass_cnt / total_records) * 100, 2)
        })
        
    report_df = pd.DataFrame(report_rows)
    report_df.to_csv('output/validation_report.csv', index=False)
    
    print("\nGenerated Validation Summary Report ('output/validation_report.csv'):")
    print(report_df.to_string())
    
    return df_clean, failures, report_df


def run_pipeline():
    """Execute full data consistency and validation pipeline."""
    print("=========================================================")
    print("     DATA CONSISTENCY & VALIDATION RULES PIPELINE        ")
    print("=========================================================")
    
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # 1. Generate unvalidated raw data
    raw_df = create_synthetic_unvalidated_data()
    raw_df.to_csv('data/raw/unvalidated_customer_data.csv', index=False)
    print("\nLoaded unvalidated raw dataset ('data/raw/unvalidated_customer_data.csv'):")
    print(raw_df.head(10))
    
    # 2. Execute Task 1: Range Checks
    df_t1 = run_range_checks(raw_df)
    
    # 3. Execute Task 2: Null Constraints
    df_t2 = run_null_constraints(df_t1)
    
    # 4. Execute Task 3: Format Patterns
    df_t3 = run_format_pattern_checks(df_t2)
    
    # 5. Execute Task 4: Business Rules
    df_t4 = run_business_rule_checks(df_t3)
    
    # 6. Execute Task 5: Report & Isolation
    df_clean, failures, report_df = generate_validation_report_and_isolate(df_t4)
    
    print("\nValidation Pipeline Execution Completed Successfully.")


if __name__ == '__main__':
    run_pipeline()
