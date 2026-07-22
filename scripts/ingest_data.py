"""
ingest_data.py
--------------
Multi-format data ingestion script for the SalesPulse B2B analytics project.

Supports:
  - CSV files with explicit delimiter and encoding parameters (Task 1)
  - JSON files including nested structure flattening (Task 2)
  - Encoding fallback strategy for non-standard files (Task 3)
  - Comprehensive ingestion documentation with shape and dtypes (Task 4)
  - Combined main execution block for all formats (Task 5)

Usage:
    python scripts/ingest_data.py

Author: SalesPulse Analytics Team
"""

import os
import pandas as pd


# ---------------------------------------------------------------------------
# Task 1 – Load CSV With Explicit Parameters
# ---------------------------------------------------------------------------

def ingest_csv(filepath, delimiter=',', encoding='utf-8', dtype_dict=None):
    """
    Load a CSV file into a Pandas DataFrame with all parameters specified explicitly.

    Args:
        filepath (str): Path to the CSV file to load.
        delimiter (str): Field separator character.
            - ',' is standard CSV (most CRM exports).
            - ';' is common in European locale systems.
            - '\\t' is used in TSV (tab-separated) exports.
            We default to ',' because our source system (Salesforce) exports standard CSV.
        encoding (str): Character encoding of the file.
            - 'utf-8' covers the vast majority of modern files.
            - 'latin-1' or 'cp1252' may be required for older Windows exports.
            We default to 'utf-8' as it is the universal standard.
        dtype_dict (dict or None): Explicit column-to-dtype mapping.
            Providing this prevents Pandas from inferring types incorrectly
            (e.g., customer IDs being read as integers instead of strings).

    Returns:
        pd.DataFrame: Loaded data with shape and column names printed.

    Raises:
        FileNotFoundError: If the file path does not exist.
        UnicodeDecodeError: If the encoding does not match the file content.
    """
    try:
        df = pd.read_csv(
            filepath,
            delimiter=delimiter,    # Explicit: don't rely on Pandas auto-detection
            encoding=encoding,      # Explicit: prevents silent data corruption
            dtype=dtype_dict        # Explicit: prevents integer ID coercion issues
        )
        print(f"  CSV loaded: {filepath}")
        print(f"  Shape: {df.shape[0]} rows x {df.shape[1]} columns")
        print(f"  Columns: {list(df.columns)}")
        return df

    except FileNotFoundError:
        # Clear error for operators: tells them exactly what path was missing
        print(f"  ERROR: File not found - {filepath}")
        raise

    except UnicodeDecodeError:
        # Guide the operator towards common encoding fixes
        print(f"  ERROR: Could not decode '{filepath}' with encoding='{encoding}'")
        print("  Hint: Try encoding='latin-1', 'iso-8859-1', or 'cp1252'")
        raise


# ---------------------------------------------------------------------------
# Task 2 – Load JSON Including Nested Structures
# ---------------------------------------------------------------------------

def ingest_json(filepath, is_nested=False):
    """
    Load a JSON file into a Pandas DataFrame, optionally flattening nested structures.

    Args:
        filepath (str): Path to the JSON file.
        is_nested (bool): If True, applies pd.json_normalize() to expand
            nested dicts into dot-notation columns.
            Example: {"customer": {"name": "Alice"}} becomes "customer.name": "Alice"
            This is required for most API responses which return nested JSON.

    Returns:
        pd.DataFrame: Loaded (and optionally flattened) data.

    Raises:
        FileNotFoundError: If the file path does not exist.
        ValueError: If the JSON content cannot be parsed into a DataFrame.
    """
    try:
        if is_nested:
            # Read raw JSON first, then normalize nested dicts into flat columns
            import json
            with open(filepath, 'r', encoding='utf-8') as f:
                raw = json.load(f)

            # json_normalize handles both list-of-dicts and nested dict structures
            df = pd.json_normalize(raw)
            print(f"  Nested JSON flattened to tabular format")
        else:
            # Flat JSON: a simple list of records — direct read is sufficient
            df = pd.read_json(filepath)

        print(f"  JSON loaded: {filepath}")
        print(f"  Shape: {df.shape[0]} rows x {df.shape[1]} columns")
        return df

    except FileNotFoundError:
        print(f"  ERROR: File not found - {filepath}")
        raise

    except ValueError as e:
        print(f"  ERROR: Could not parse JSON from '{filepath}': {e}")
        raise


# ---------------------------------------------------------------------------
# Task 3 – Encoding Fallback Strategy
# ---------------------------------------------------------------------------

def ingest_csv_with_fallback(filepath, delimiters=None, fallback_encodings=None):
    """
    Load a CSV file by trying multiple encodings and delimiters until one succeeds.

    This is especially useful when receiving data from external vendors or legacy
    systems that do not consistently label their file encoding.

    Args:
        filepath (str): Path to the CSV file.
        delimiters (list): List of delimiter characters to try. Defaults to [','].
        fallback_encodings (list): Ordered list of encodings to attempt.
            Defaults to ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252'].
            We try utf-8 first (the modern standard), then fall back to
            Windows-1252 / Latin-1 variants used by older tools.

    Returns:
        pd.DataFrame: Successfully loaded data.

    Raises:
        ValueError: If no combination of delimiter and encoding succeeds.
    """
    if delimiters is None:
        delimiters = [',']

    if fallback_encodings is None:
        # Try the most common encodings in order of likelihood
        fallback_encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']

    # Iterate through every delimiter × encoding combination
    for delimiter in delimiters:
        for encoding in fallback_encodings:
            try:
                df = pd.read_csv(filepath, delimiter=delimiter, encoding=encoding)
                print(f"  Successfully loaded with delimiter='{delimiter}', encoding='{encoding}'")
                return df
            except (UnicodeDecodeError, pd.errors.ParserError):
                # This combination failed — silently try the next one
                continue

    # All combinations exhausted without success
    raise ValueError(
        f"Could not load '{filepath}' with any encoding/delimiter combination.\n"
        f"  Tried delimiters: {delimiters}\n"
        f"  Tried encodings: {fallback_encodings}"
    )


# ---------------------------------------------------------------------------
# Task 4 – Document Ingestion Output With Shape and Types
# ---------------------------------------------------------------------------

def document_ingestion(df, source_file):
    """
    Print a comprehensive ingestion audit report for a loaded DataFrame.

    This creates a clear, human-readable record of exactly what was loaded,
    which is essential for data lineage tracking and debugging pipeline issues.

    Args:
        df (pd.DataFrame): The DataFrame to document.
        source_file (str): Name/path of the source file (used in the report header).

    Returns:
        pd.DataFrame: The same DataFrame, unchanged (for method chaining).
    """
    print(f"\n{'=' * 60}")
    print(f"  INGESTION REPORT: {source_file}")
    print(f"{'=' * 60}")

    # Basic dimensions
    print(f"  Rows    : {df.shape[0]}")
    print(f"  Columns : {df.shape[1]}")

    # Column names with their inferred data types
    # This helps catch type inference errors early (e.g., dates read as objects)
    print(f"\n  Column Names & Data Types:")
    for col, dtype in df.dtypes.items():
        print(f"    {col:<25} {dtype}")

    # Null value counts per column — critical for pipeline quality gating
    print(f"\n  Null Values Per Column:")
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        flag = " <-- WARNING" if count > 0 else ""
        print(f"    {col:<25} {count}{flag}")

    # Preview first 3 rows so operators can visually confirm data looks correct
    print(f"\n  First 3 Rows:")
    print(df.head(3).to_string(index=False))

    print(f"{'=' * 60}\n")
    return df


# ---------------------------------------------------------------------------
# Task 5 – Main Ingestion Script Combining Multiple Formats
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  SalesPulse Multi-Format Data Ingestion")
    print("=" * 60)

    # Ensure processed output directory exists
    os.makedirs("data/processed", exist_ok=True)

    # ------------------------------------------------------------------ #
    # 1. Load CSV with explicit parameters
    # ------------------------------------------------------------------ #
    print("\n[1/3] Loading CSV: customers.csv")
    csv_df = ingest_csv(
        "data/raw/customers.csv",
        delimiter=',',          # Standard comma-separated — matches CRM export format
        encoding='utf-8',       # UTF-8 — confirmed by charset detection in validate_intake.py
        dtype_dict={
            'customer_id': str  # Keep IDs as strings to prevent numeric coercion issues
        }
    )
    document_ingestion(csv_df, "customers.csv")

    # ------------------------------------------------------------------ #
    # 2. Load JSON with flattening
    # ------------------------------------------------------------------ #
    print("[2/3] Loading JSON: transactions.json")
    json_df = ingest_json(
        "data/raw/transactions.json",
        is_nested=True   # Apply json_normalize in case records contain nested dicts
    )
    document_ingestion(json_df, "transactions.json")

    # ------------------------------------------------------------------ #
    # 3. Demonstrate encoding fallback (runs on customers.csv as demo)
    # ------------------------------------------------------------------ #
    print("[3/3] Demonstrating encoding fallback strategy...")
    fallback_df = ingest_csv_with_fallback(
        "data/raw/customers.csv",
        delimiters=[',', ';'],
        fallback_encodings=['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    )

    # ------------------------------------------------------------------ #
    # Save ingested data to processed/
    # ------------------------------------------------------------------ #
    csv_output = "data/processed/customers_ingested.csv"
    json_output = "data/processed/transactions_ingested.csv"

    csv_df.to_csv(csv_output, index=False)
    json_df.to_csv(json_output, index=False)

    print(f"\n  Saved: {csv_output}")
    print(f"  Saved: {json_output}")

    print("\n" + "=" * 60)
    print("  All data ingested and saved to data/processed/")
    print("=" * 60)
