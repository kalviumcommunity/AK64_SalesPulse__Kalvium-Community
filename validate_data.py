"""
SalesPulse Data Validation Engine
----------------------------------
Assignment 2.59 - GitHub Workflow Automation & Validation

Performs automated data quality & schema validation:
  1. Checks presence of required columns (customer_id, order_id, amount, date, segment)
  2. Validates numeric data types for amount/revenue
  3. Verifies minimum row count threshold
  4. Detects fully null columns (schema drift prevention)
Exits with status code 0 on pass, or status code 1 on failure to block PR merge.
"""

import sys
import os
import pandas as pd


def validate(file_path, min_rows=5):
    """
    Run all schema and data quality validation checks on specified file_path.
    Exits with status code 1 if errors occur, or code 0 if all checks pass.
    """
    print("=" * 65)
    print(f"STARTING SALESPULSE DATA VALIDATION: {file_path}")
    print("=" * 65)

    if not os.path.exists(file_path):
        print(f"\nVALIDATION FAILED:\n  ERROR: Specified data file does not exist: {file_path}")
        sys.exit(1)

    try:
        if file_path.endswith(".json"):
            df = pd.read_json(file_path)
        else:
            df = pd.read_csv(file_path)
    except Exception as e:
        print(f"\nVALIDATION FAILED:\n  ERROR: Could not parse input file: {e}")
        sys.exit(1)

    # Standardize column name lookup
    df.columns = [str(col).strip().lower() for col in df.columns]

    # Map column aliases for resilience
    if "revenue" in df.columns and "amount" not in df.columns:
        df["amount"] = df["revenue"]
    if "transaction_date" in df.columns and "date" not in df.columns:
        df["date"] = df["transaction_date"]
    if "order_date" in df.columns and "date" not in df.columns:
        df["date"] = df["order_date"]

    errors = []

    # Check 1: Required columns exist
    required_cols = ["customer_id", "order_id", "amount", "date", "segment"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        errors.append(f"Missing required columns: {missing}")
    else:
        print("  PASS: Required columns present (customer_id, order_id, amount, date, segment)")

    # Check 2: Data types validation
    if "amount" in df.columns:
        if not pd.api.types.is_numeric_dtype(df["amount"]):
            errors.append(f"Column 'amount' is not numeric (found type: {df['amount'].dtype})")
        else:
            print(f"  PASS: amount column is numeric ({df['amount'].dtype})")
    else:
        errors.append("Column 'amount' not found in dataset")

    # Check 3: Minimum row count threshold
    if len(df) < min_rows:
        errors.append(f"Row count {len(df):,} is below required minimum threshold of {min_rows}")
    else:
        print(f"  PASS: Row count ({len(df):,} rows) meets minimum threshold ({min_rows})")

    # Check 4: No fully null columns
    null_cols = [c for c in df.columns if df[c].isnull().all()]
    if null_cols:
        errors.append(f"Fully null columns detected: {null_cols}")
    else:
        print("  PASS: No fully null columns detected in dataset")

    print("-" * 65)

    # Task 3 & Task 4: Report results and set exit status code
    if errors:
        print("\nVALIDATION FAILED:")
        for err in errors:
            print(f"  ERROR: {err}")
        print("=" * 65)
        sys.exit(1)
    else:
        print("\nALL CHECKS PASSED SUCCESSFULLY")
        print("=" * 65)
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        target_path = os.path.join("output", "cleaned.csv")
        if not os.path.exists(target_path):
            target_path = os.path.join("data", "raw", "latest.csv")
    else:
        target_path = sys.argv[1]

    validate(target_path)
