"""
validate_intake.py
------------------
Dataset intake validation script for the SalesPulse B2B analytics project.

This script runs a series of checks on an incoming data file before it is
allowed to enter the processing pipeline:
  1. File existence and non-emptiness
  2. File format (extension) validation
  3. Column schema validation
  4. File encoding detection
  5. Dataset dimension capture (rows, columns, file size)
  6. Generates a structured JSON intake report in output/

Usage:
    python scripts/validate_intake.py

Author: SalesPulse Analytics Team
"""

import os
import json
import chardet
import pandas as pd
from datetime import datetime


# ---------------------------------------------------------------------------
# Task 1 – File Existence and Format Checks
# ---------------------------------------------------------------------------

def validate_file_exists(filepath):
    """
    Check if a file exists on disk and is non-empty.

    Input:
        filepath (str): Path to the file to check.

    Output:
        tuple(bool, str): (True, success message) or (False, error message).

    Assumptions:
        - 'Empty' means zero bytes on disk.
    """
    # Verify the path points to an actual file
    if not os.path.exists(filepath):
        return False, f"FAIL - File does not exist: {filepath}"

    # A zero-byte file is considered empty and unprocessable
    if os.path.getsize(filepath) == 0:
        return False, f"FAIL - File is empty: {filepath}"

    return True, "PASS - File exists and has content"


def validate_file_format(filepath, allowed_formats=None):
    """
    Check that the file's extension is in the list of supported formats.

    Input:
        filepath (str): Path to the file.
        allowed_formats (list): Allowed extensions. Defaults to csv, json, xlsx.

    Output:
        tuple(bool, str): (True, success message) or (False, error message).
    """
    if allowed_formats is None:
        allowed_formats = ['csv', 'json', 'xlsx']

    # Extract extension from the filename (lowercased for case-insensitivity)
    extension = filepath.split('.')[-1].lower()

    if extension not in allowed_formats:
        return False, (
            f"FAIL - Unsupported format: '{extension}'. "
            f"Allowed formats: {allowed_formats}"
        )

    return True, f"PASS - Format valid: {extension}"


# ---------------------------------------------------------------------------
# Task 2 – Column Schema Validation
# ---------------------------------------------------------------------------

def validate_schema(df, expected_columns):
    """
    Compare the DataFrame's actual columns against an expected schema.

    Input:
        df (pd.DataFrame): The loaded dataset.
        expected_columns (list): Column names that must be present.

    Output:
        tuple(bool, str): (True, success message) or (False, details of mismatches).

    Behaviour:
        - Reports MISSING columns (required but absent).
        - Reports UNEXPECTED columns (present but not required).
        - Both conditions are flagged; they do not cancel each other out.
    """
    actual_cols = set(df.columns)
    expected_cols = set(expected_columns)

    # Columns that are required but absent from the file
    missing = expected_cols - actual_cols

    # Columns that exist in the file but were not expected
    extra = actual_cols - expected_cols

    issues = []
    if missing:
        issues.append(f"Missing columns: {sorted(missing)}")
    if extra:
        issues.append(f"Unexpected columns: {sorted(extra)}")

    if not issues:
        return True, f"PASS - Schema valid: {len(df.columns)} columns present"

    return False, "FAIL - " + " | ".join(issues)


# ---------------------------------------------------------------------------
# Task 3 – File Encoding Detection
# ---------------------------------------------------------------------------

def detect_encoding(filepath):
    """
    Detect the character encoding of a file using the chardet library.

    Input:
        filepath (str): Path to the file.

    Output:
        tuple(str, str): (encoding_name, human-readable message).

    Assumptions:
        - Reads only the first 10,000 bytes for efficiency on large files.
        - Falls back to 'utf-8' if chardet cannot determine encoding.
    """
    # Read a sample of the file in binary mode for encoding detection
    with open(filepath, 'rb') as f:
        raw_bytes = f.read(10000)

    result = chardet.detect(raw_bytes)

    # Use detected encoding; fall back to utf-8 if result is None
    encoding = result.get('encoding') or 'utf-8'
    confidence = result.get('confidence', 0)

    msg = f"PASS - Detected: {encoding} (confidence: {confidence:.1%})"
    return encoding, msg


# ---------------------------------------------------------------------------
# Task 4 – Dataset Dimension Capture
# ---------------------------------------------------------------------------

def capture_dataset_stats(filepath, df):
    """
    Capture baseline metrics about the dataset for the intake report.

    Input:
        filepath (str): Path to the file (used to calculate size).
        df (pd.DataFrame): The loaded dataset.

    Output:
        dict: Dictionary with keys 'rows', 'columns', 'file_size_mb', 'bytes'.

    Assumptions:
        - File size is read directly from the OS (before any in-memory transformations).
    """
    file_bytes = os.path.getsize(filepath)

    # Convert bytes to megabytes, rounded to 6 decimal places for small files
    file_size_mb = round(file_bytes / (1024 * 1024), 6)

    return {
        'rows': len(df),
        'columns': len(df.columns),
        'file_size_mb': file_size_mb,
        'bytes': file_bytes
    }


# ---------------------------------------------------------------------------
# Task 5 – Generate and Save Intake Validation Report
# ---------------------------------------------------------------------------

def generate_intake_report(filepath, expected_columns):
    """
    Run all validation checks and compile results into a structured JSON report.

    Input:
        filepath (str): Path to the data file to validate.
        expected_columns (list): Column names required in the schema.

    Output:
        dict: The full validation report (also saved to output/intake_report.json).

    Report Structure:
        - timestamp: ISO-format datetime of when the report was generated.
        - filepath: The file that was validated.
        - validations: Pass/fail messages for each check.
        - statistics: Baseline dataset metrics (only present if file is valid).
    """
    # Initialise the report structure
    report = {
        'timestamp': datetime.now().isoformat(),
        'filepath': filepath,
        'validations': {}
    }

    # ---- Check 1: File existence ----
    file_exists, msg = validate_file_exists(filepath)
    report['validations']['file_exists'] = msg
    if not file_exists:
        # Cannot proceed further if the file is missing or empty
        _save_report(report)
        return report

    # ---- Check 2: File format ----
    format_valid, msg = validate_file_format(filepath)
    report['validations']['format'] = msg

    # ---- Load data for subsequent checks ----
    df = pd.read_csv(filepath)

    # ---- Check 3: Schema validation ----
    schema_valid, msg = validate_schema(df, expected_columns)
    report['validations']['schema'] = msg

    # ---- Check 4: Encoding detection ----
    encoding, msg = detect_encoding(filepath)
    report['validations']['encoding'] = msg

    # ---- Check 5: Dataset dimensions ----
    stats = capture_dataset_stats(filepath, df)
    report['statistics'] = stats

    # ---- Persist report ----
    _save_report(report)

    return report


def _save_report(report, output_path='output/intake_report.json'):
    """
    Internal helper: save the report dict to a JSON file.

    Input:
        report (dict): The validation report to serialise.
        output_path (str): Destination file path.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)

    print(f"  -> Report saved to: {output_path}")


# ---------------------------------------------------------------------------
# Main execution block
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 55)
    print("  SalesPulse Dataset Intake Validation")
    print("=" * 55)

    # --- Configuration ---
    # Path to the file being validated
    TARGET_FILE = "data/raw/sample.csv"

    # Expected schema for this dataset
    EXPECTED_COLUMNS = [
        "customer_id",
        "customer_name",
        "transaction_amount",
        "transaction_date"
    ]

    print(f"\nTarget file : {TARGET_FILE}")
    print(f"Expected schema : {EXPECTED_COLUMNS}\n")

    # --- Run all validations ---
    report = generate_intake_report(TARGET_FILE, EXPECTED_COLUMNS)

    # --- Print human-readable summary ---
    print("\n" + "-" * 55)
    print("  Validation Results")
    print("-" * 55)
    for check, result in report['validations'].items():
        status_icon = "✓" if result.startswith("PASS") else "✗"
        print(f"  {status_icon}  [{check}] {result}")

    if 'statistics' in report:
        print("\n" + "-" * 55)
        print("  Dataset Statistics")
        print("-" * 55)
        stats = report['statistics']
        print(f"  Rows         : {stats['rows']}")
        print(f"  Columns      : {stats['columns']}")
        print(f"  File size    : {stats['file_size_mb']} MB ({stats['bytes']} bytes)")

    print("\n" + "=" * 55)
    print("  Validation complete.")
    print("=" * 55)
