"""
data_workflow.py
----------------
A modular data pipeline script for the SalesPulse B2B analytics project.

This script ingests raw CRM data, processes and cleans it,
and outputs an analysis-ready CSV file.

Usage:
    python scripts/data_workflow.py

Author: SalesPulse Analytics Team
"""

import os
import sys
import io
import pandas as pd

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Function 1: Ingest
# ---------------------------------------------------------------------------

def ingest_data(filepath):
    """
    Load data from a CSV file into a Pandas DataFrame.

    Input:
        filepath (str): Relative or absolute path to the source CSV file.

    Output:
        pd.DataFrame: Raw data loaded from the file.

    Assumptions:
        - The file exists and is a valid, header-bearing CSV.
        - The encoding is UTF-8 (Pandas default).
    """
    # Verify the file exists before attempting to read it
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Input file not found: '{filepath}'. "
            "Please ensure the file exists in the data/raw/ directory."
        )

    print(f"  → Reading data from: {filepath}")

    # Read the CSV file into a DataFrame
    df = pd.read_csv(filepath)

    print(f"  → Loaded {len(df)} rows and {len(df.columns)} columns.")
    return df


# ---------------------------------------------------------------------------
# Function 2: Process
# ---------------------------------------------------------------------------

def process_data(df):
    """
    Transform raw data into an analysis-ready format.

    Input:
        df (pd.DataFrame): Raw DataFrame as returned by ingest_data().

    Output:
        pd.DataFrame: Cleaned and enriched DataFrame ready for analysis.

    Transformations applied:
        1. Remove exact duplicate rows (all column values identical).
        2. Fill missing values in numerical columns with the column median.
        3. Fill missing values in text columns with 'Unknown'.
        4. Add a derived column: deal_tier (categorises deal_value into buckets).
    """
    initial_rows = len(df)

    # Step 1 – Remove exact duplicate rows
    # Duplicates distort aggregations and model training.
    df = df.drop_duplicates()
    dupes_removed = initial_rows - len(df)
    print(f"  → Duplicates removed: {dupes_removed}")

    # Step 2 – Fill missing numerical values with the column median
    # Using median (not mean) to resist the effect of outliers.
    for col in df.select_dtypes(include=["number"]).columns:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"  → Filled {missing_count} missing value(s) in '{col}' with median ({median_val:.2f})")

    # Step 3 – Fill missing categorical / text values with 'Unknown'
    for col in df.select_dtypes(include=["object"]).columns:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            df[col] = df[col].fillna("Unknown")
            print(f"  → Filled {missing_count} missing value(s) in '{col}' with 'Unknown'")

    # Step 4 – Add a derived 'deal_tier' column for segmentation analysis
    # Bucketing deal_value helps the sales team prioritise coaching efforts.
    def assign_tier(value):
        if value < 5000:
            return "Small"
        elif value < 12000:
            return "Medium"
        else:
            return "Large"

    val_col = "deal_value" if "deal_value" in df.columns else ("transaction_amount" if "transaction_amount" in df.columns else None)
    if val_col:
        df["deal_tier"] = df[val_col].apply(assign_tier)
        print(f"  → Added derived column: 'deal_tier' based on '{val_col}'")

    print(f"  → Rows after processing: {len(df)}")
    return df


# ---------------------------------------------------------------------------
# Function 3: Output
# ---------------------------------------------------------------------------

def output_results(df, output_path):
    """
    Save the processed DataFrame to a CSV file and print a summary.

    Input:
        df (pd.DataFrame): Cleaned and processed DataFrame.
        output_path (str): Path where the output CSV should be written.

    Output:
        None (writes file to disk and prints confirmation to stdout).

    Assumptions:
        - The parent directory of output_path already exists.
    """
    # Ensure the output directory exists; create it if necessary
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"  → Created output directory: {output_dir}")

    # Write the DataFrame to CSV without the Pandas row index
    df.to_csv(output_path, index=False)

    # Print a confirmation summary for the execution log
    print(f"\n✓ Data successfully processed")
    print(f"✓ Rows processed: {len(df)}")
    print(f"✓ Columns in output: {list(df.columns)}")
    print(f"✓ Output saved to {output_path}")


# ---------------------------------------------------------------------------
# Main execution block
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("  SalesPulse Data Pipeline")
    print("=" * 50)

    # --- Ingest ---
    print("\n[1/3] Ingesting raw data...")
    data = ingest_data("data/raw/sample.csv")

    # --- Process ---
    print("\n[2/3] Processing data...")
    processed = process_data(data)

    # --- Output ---
    print("\n[3/3] Saving results...")
    output_results(processed, "output/processed.csv")

    print("\n" + "=" * 50)
    print("  Pipeline complete.")
    print("=" * 50)
