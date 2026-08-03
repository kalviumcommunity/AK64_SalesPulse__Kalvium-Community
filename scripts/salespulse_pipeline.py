"""
SalesPulse â€” Real Data Pipeline
================================
Assignment 22 - Kalvium SalesPulse End-to-End Data Pipeline

Ingests, cleans, joins, and outputs all 5 real CRM datasets:
  - users.csv        â†’ 15 sales reps + managers
  - customers.csv    â†’ 450 B2B customer companies
  - deals.csv        â†’ 921 deal records
  - activities.csv   â†’ 1,836 activity logs (calls, meetings, emails, notes)
  - emails.csv       â†’ 966 email communications

Data issues fixed per table:
  Users    : broken emails, ALLCAPS names, whitespace, missing role
  Customers: 8 exact duplicate IDs, whitespace, mixed casing, malformed emails
  Deals    : 5 date formats, money as "$x,xxx.xx" / "x USD", 20+ stage variants,
             date logic errors (closed < created), missing values
  Activities: ALLCAPS/inconsistent types, 5 date formats, whitespace in notes,
              orphaned deal references
  Emails   : stray dots in sender/receiver, missing @, ALLCAPS subjects,
              5 date formats, orphan deal references

Output files (all to data/processed/ and output/):
  data/processed/clean_users.csv
  data/processed/clean_customers.csv
  data/processed/clean_deals.csv
  data/processed/clean_activities.csv
  data/processed/clean_emails.csv
  data/processed/master_salespulse.csv   â† unified master join table
  output/salespulse_data_quality_report.json
"""

import os
import re
import io
import sys
import json
import warnings
import pandas as pd
import numpy as np
from datetime import datetime

# Force UTF-8 output on Windows (avoids CP1252 encoding errors with special chars)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

warnings.filterwarnings("ignore")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# PATHS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT, "data", "raw_new")
PROC_DIR = os.path.join(ROOT, "data", "processed")
OUT_DIR = os.path.join(ROOT, "output")

os.makedirs(PROC_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# UTILITY: MULTI-FORMAT DATE PARSER
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def parse_flexible_dates(series: pd.Series) -> pd.Series:
    """
    Parses dates across all formats found in this dataset:
      - 'DD-MM-YYYY'  â†’ Dashed day-first
      - 'YYYY/MM/DD'  â†’ Slashed ISO
      - 'N/A'         â†’ NaT
    Returns a datetime Series with unparseable values as NaT.
    """
    # Replace any N/A, n/a, na strings with NaN first
    cleaned = series.astype(str).str.strip()
    cleaned = cleaned.replace({"N/A": np.nan, "n/a": np.nan, "NA": np.nan, "nan": np.nan, "": np.nan})

    # Try dayfirst=False first (handles YYYY-MM-DD, MM/DD/YYYY, YYYY/MM/DD well)
    parsed = pd.to_datetime(cleaned, errors="coerce", dayfirst=False)

    # For values that still failed, retry with dayfirst=True (handles DD/MM/YYYY, DD-MM-YYYY)
    still_null = parsed.isna() & cleaned.notna()
    if still_null.any():
        retry = pd.to_datetime(cleaned[still_null], errors="coerce", dayfirst=True)
        parsed[still_null] = retry

    return parsed


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# UTILITY: EMAIL VALIDATOR
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
PLACEHOLDER_DOMAINS = {"company.com"}


def validate_email(email: str) -> str:
    """
    Returns:
      'valid'        - properly formatted real email
      'placeholder'  - uses a known internal placeholder domain (e.g. @COMPANY.COM)
      'malformed'    - missing @, stray dots, otherwise broken
      'missing'      - null / empty
    """
    if pd.isna(email) or str(email).strip() == "":
        return "missing"
    email_str = str(email).strip().lower()
    domain = email_str.split("@")[-1] if "@" in email_str else ""
    if domain in PLACEHOLDER_DOMAINS:
        return "placeholder"
    if EMAIL_REGEX.match(email_str):
        return "valid"
    return "malformed"


def fix_stray_dots_email(email: str) -> str:
    """
    Fixes common stray-dot patterns:
      '..cristian.santos...@yahoo.com'  â†’ 'cristian.santos@yahoo.com'
      'mrs..janet.chase@yahoo.com'      â†’ 'mrs.janet.chase@yahoo.com'
    """
    if pd.isna(email):
        return email
    email_str = str(email).strip()
    if "@" not in email_str:
        return email_str
    local, domain = email_str.split("@", 1)
    # Strip leading/trailing dots from local part
    local = local.strip(".")
    # Replace consecutive dots with single dot
    local = re.sub(r"\.{2,}", ".", local)
    return f"{local}@{domain}"


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# STEP 1: CLEAN USERS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def clean_users(path: str) -> tuple[pd.DataFrame, dict]:
    """
    Cleans the users table.
    Fixes: ALLCAPS names, leading/trailing whitespace, broken emails, missing role.
    """
    print("\n" + "=" * 60)
    print("STEP 1: Cleaning users.csv")
    print("=" * 60)

    df = pd.read_csv(path)
    report = {"source": "users.csv", "raw_rows": len(df), "issues": {}}

    print(f"  Loaded {len(df)} rows | Columns: {list(df.columns)}")

    # 1a. Strip whitespace from name
    ws_names = df["name"].str.strip() != df["name"].fillna("")
    df["name"] = df["name"].str.strip()
    report["issues"]["whitespace_in_name"] = int(ws_names.sum())
    print(f"  [fix] Stripped whitespace from {ws_names.sum()} name(s)")

    # 1b. Normalise name casing â†’ Title Case
    allcaps = df["name"].str.isupper().fillna(False)
    df["name"] = df["name"].str.title()
    report["issues"]["allcaps_names_normalised"] = int(allcaps.sum())
    print(f"  [fix] Normalised {allcaps.sum()} ALLCAPS name(s) to Title Case")

    # 1c. Validate emails
    df["email_status"] = df["email"].apply(validate_email)
    email_issues = df[df["email_status"] != "valid"]
    report["issues"]["email_invalid_or_missing"] = len(email_issues)
    print(f"  [flag] {len(email_issues)} email(s) flagged â€” breakdown:")
    for status, grp in email_issues.groupby("email_status"):
        ids = grp["user_id"].tolist()
        print(f"         {status}: {ids}")

    # 1d. Fill missing role
    missing_role = df["role"].isna() | (df["role"].str.strip() == "")
    df["role"] = df["role"].str.strip().replace("", np.nan).fillna("unknown")
    report["issues"]["missing_role_filled"] = int(missing_role.sum())
    print(f"  [fix] Filled {missing_role.sum()} missing role(s) with 'unknown'")

    # Drop trailing empty row if present
    df = df.dropna(how="all").reset_index(drop=True)
    report["clean_rows"] = len(df)

    print(f"  âœ“ Users clean: {len(df)} rows")
    return df, report


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# STEP 2: CLEAN CUSTOMERS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def clean_customers(path: str) -> tuple[pd.DataFrame, dict]:
    """
    Cleans the customers table.
    Fixes: exact duplicates, whitespace in company_name, mixed casing,
           malformed emails (placeholder domains, missing @, double dots).
    """
    print("\n" + "=" * 60)
    print("STEP 2: Cleaning customers.csv")
    print("=" * 60)

    df = pd.read_csv(path)
    report = {"source": "customers.csv", "raw_rows": len(df), "issues": {}}
    print(f"  Loaded {len(df)} rows | Columns: {list(df.columns)}")

    # Drop fully empty rows
    df = df.dropna(how="all").reset_index(drop=True)

    # 2a. Remove exact duplicate rows
    dupes = df.duplicated()
    n_dupes = dupes.sum()
    dupe_ids = df[dupes]["customer_id"].tolist()
    df = df.drop_duplicates().reset_index(drop=True)
    report["issues"]["exact_duplicates_removed"] = n_dupes
    report["issues"]["duplicate_customer_ids"] = dupe_ids
    print(f"  [fix] Removed {n_dupes} exact duplicate rows: {dupe_ids}")

    # 2b. Strip whitespace from company_name, then Title Case
    df["company_name"] = df["company_name"].str.strip()
    ws_count = (df["company_name"].str.strip() != df["company_name"].fillna("")).sum()
    # Normalise casing: title case (handles ALL CAPS, all lowercase, mixed)
    df["company_name"] = df["company_name"].str.title()
    report["issues"]["company_name_whitespace_fixed"] = int(ws_count)
    print(f"  [fix] Stripped whitespace + Title-cased all company names")

    # 2c. Fix stray dots in email then validate
    df["email"] = df["email"].apply(fix_stray_dots_email)
    df["email_status"] = df["email"].apply(validate_email)
    email_counts = df["email_status"].value_counts().to_dict()
    report["issues"]["email_status_breakdown"] = email_counts
    print(f"  [flag] Email validation results: {email_counts}")

    # 2d. Fix contact_person whitespace and title case
    df["contact_person"] = df["contact_person"].str.strip().str.title()
    missing_contact = df["contact_person"].isna().sum()
    report["issues"]["missing_contact_person"] = int(missing_contact)
    print(f"  [flag] {missing_contact} row(s) have no contact_person (kept as null)")

    # 2e. Missing phone
    missing_phone = df["phone_number"].isna().sum()
    report["issues"]["missing_phone_number"] = int(missing_phone)
    print(f"  [flag] {missing_phone} row(s) have no phone number (kept as null)")

    report["clean_rows"] = len(df)
    print(f"  âœ“ Customers clean: {len(df)} rows")
    return df, report


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# STEP 3: CLEAN DEALS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

# All known stage variants â†’ canonical label
STAGE_MAP = {
    # Prospecting / Prospect
    "prospecting": "Prospecting",
    "prospect": "Prospecting",
    "PROSPECT": "Prospecting",
    # Qualified / Qualification
    "qualified": "Qualified",
    "qualification": "Qualified",
    # Proposal Sent
    "proposal sent": "Proposal Sent",
    "proposal": "Proposal Sent",
    # Negotiation
    "negotiation": "Negotiation",
    "negotiation ": "Negotiation",  # trailing space variant
    # Closed Won
    "closed won": "Closed Won",
    "closed-won": "Closed Won",
    "won": "Closed Won",
    # Closed Lost
    "closed lost": "Closed Lost",
    "closed-lost": "Closed Lost",
    "lost": "Closed Lost",
}

STATUS_MAP = {
    "open": "open",
    "won": "won",
    "lost": "lost",
    "closed": "closed",
}


def parse_deal_value(val) -> float | None:
    """
    Converts money strings to float:
      "$10,346.37"  â†’  10346.37
      "60345 USD"   â†’  60345.0
      "1728.62"     â†’  1728.62
      ""            â†’  NaN
    """
    if pd.isna(val) or str(val).strip() == "":
        return np.nan
    s = str(val).strip()
    s = s.replace("$", "").replace(",", "").replace(" USD", "").strip()
    try:
        return float(s)
    except ValueError:
        return np.nan


def normalise_stage(stage) -> str | None:
    """Maps all stage variants to a canonical label."""
    if pd.isna(stage) or str(stage).strip() == "":
        return np.nan
    key = str(stage).strip().lower().replace("-", " ").rstrip()
    return STAGE_MAP.get(key, str(stage).strip().title())


def normalise_status(status) -> str | None:
    """Maps all status variants to lowercase canonical."""
    if pd.isna(status) or str(status).strip() == "":
        return np.nan
    return STATUS_MAP.get(str(status).strip().lower(), str(status).strip().lower())


def clean_deals(path: str) -> tuple[pd.DataFrame, dict]:
    """
    Cleans the deals table.
    Fixes: deal_value formats, current_stage variants, status casing,
           5 date formats, N/A â†’ NaT, date logic errors.
    """
    print("\n" + "=" * 60)
    print("STEP 3: Cleaning deals.csv")
    print("=" * 60)

    df = pd.read_csv(path, dtype=str)
    report = {"source": "deals.csv", "raw_rows": len(df), "issues": {}}
    print(f"  Loaded {len(df)} rows | Columns: {list(df.columns)}")

    # Drop fully empty rows
    df = df.dropna(how="all").reset_index(drop=True)

    # 3a. Parse deal_value
    raw_missing = df["deal_value"].isna().sum()
    df["deal_value"] = df["deal_value"].apply(parse_deal_value)
    parsed_missing = df["deal_value"].isna().sum()
    report["issues"]["deal_value_missing_raw"] = int(raw_missing)
    report["issues"]["deal_value_missing_after_parse"] = int(parsed_missing)
    report["issues"]["deal_value_fixed_currency_strings"] = int(parsed_missing - raw_missing if parsed_missing > raw_missing else 0)
    print(f"  [fix] Parsed deal_value â†’ float. Missing after parse: {parsed_missing}")

    # 3b. Normalise current_stage
    df["current_stage"] = df["current_stage"].apply(normalise_stage)
    missing_stage = df["current_stage"].isna().sum()
    report["issues"]["missing_current_stage"] = int(missing_stage)
    stage_dist = df["current_stage"].value_counts().to_dict()
    report["issues"]["stage_distribution"] = stage_dist
    print(f"  [fix] Normalised current_stage. Distribution: {stage_dist}")

    # 3c. Normalise status
    df["status"] = df["status"].apply(normalise_status)
    missing_status = df["status"].isna().sum()
    report["issues"]["missing_status"] = int(missing_status)
    status_dist = df["status"].value_counts().to_dict()
    report["issues"]["status_distribution"] = status_dist
    print(f"  [fix] Normalised status. Distribution: {status_dist}")

    # 3d. Parse dates
    df["created_date"] = parse_flexible_dates(df["created_date"])
    df["closed_date"] = parse_flexible_dates(df["closed_date"])
    missing_created = df["created_date"].isna().sum()
    missing_closed = df["closed_date"].isna().sum()
    report["issues"]["missing_created_date"] = int(missing_created)
    report["issues"]["missing_closed_date"] = int(missing_closed)
    print(f"  [fix] Parsed all dates. Missing created: {missing_created} | Missing closed: {missing_closed}")

    # 3e. Flag date logic errors (closed_date < created_date)
    df["date_logic_error"] = (
        df["closed_date"].notna()
        & df["created_date"].notna()
        & (df["closed_date"] < df["created_date"])
    )
    n_logic_errors = df["date_logic_error"].sum()
    report["issues"]["date_logic_errors"] = int(n_logic_errors)
    print(f"  [flag] {n_logic_errors} deal(s) have closed_date BEFORE created_date (flagged)")

    # 3f. Compute deal_duration_days for deals with both dates and no logic error
    df["deal_duration_days"] = np.nan
    valid_dates = df["closed_date"].notna() & df["created_date"].notna() & ~df["date_logic_error"]
    df.loc[valid_dates, "deal_duration_days"] = (
        (df.loc[valid_dates, "closed_date"] - df.loc[valid_dates, "created_date"]).dt.days
    )
    print(f"  [feature] Computed deal_duration_days for {valid_dates.sum()} deals")

    report["clean_rows"] = len(df)
    print(f"  âœ“ Deals clean: {len(df)} rows")
    return df, report


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# STEP 4: CLEAN ACTIVITIES
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

ACTIVITY_TYPE_MAP = {
    "call": "call",
    "email": "email",
    "meeting": "meeting",
    "note": "note",
    "follow up": "follow_up",
    "follow-up": "follow_up",
    "follow_up": "follow_up",
}


def normalise_activity_type(atype) -> str:
    """Maps all activity type variants to a clean canonical label."""
    if pd.isna(atype) or str(atype).strip() == "":
        return "unknown"
    key = str(atype).strip().lower().replace("-", " ")
    return ACTIVITY_TYPE_MAP.get(key, key)


def clean_activities(path: str, valid_deal_ids: set) -> tuple[pd.DataFrame, dict]:
    """
    Cleans the activities table.
    Fixes: ALLCAPS/inconsistent type, 5 date formats, whitespace + ALLCAPS in notes,
           orphaned deal references (deal_id not in deals table).
    """
    print("\n" + "=" * 60)
    print("STEP 4: Cleaning activities.csv")
    print("=" * 60)

    df = pd.read_csv(path, dtype=str)
    report = {"source": "activities.csv", "raw_rows": len(df), "issues": {}}
    print(f"  Loaded {len(df)} rows | Columns: {list(df.columns)}")

    # Drop fully empty rows
    df = df.dropna(how="all").reset_index(drop=True)

    # 4a. Normalise activity_type
    df["activity_type"] = df["activity_type"].apply(normalise_activity_type)
    type_dist = df["activity_type"].value_counts().to_dict()
    report["issues"]["activity_type_distribution"] = type_dist
    print(f"  [fix] Normalised activity_type. Distribution: {type_dist}")

    # 4b. Parse activity_date
    df["activity_date"] = parse_flexible_dates(df["activity_date"])
    missing_date = df["activity_date"].isna().sum()
    report["issues"]["missing_activity_date"] = int(missing_date)
    print(f"  [fix] Parsed activity_date. Missing: {missing_date}")

    # 4c. Clean notes: strip whitespace, title-case ALL-CAPS notes
    df["notes"] = df["notes"].astype(str).str.strip()
    df["notes"] = df["notes"].replace({"nan": np.nan, "": np.nan})
    # Fix ALL-CAPS notes: if 80%+ uppercase letters, convert to title case
    def fix_note_casing(note):
        if pd.isna(note):
            return note
        letters = [c for c in str(note) if c.isalpha()]
        if letters and sum(1 for c in letters if c.isupper()) / len(letters) > 0.8:
            return str(note).capitalize()
        return note
    df["notes"] = df["notes"].apply(fix_note_casing)
    missing_notes = df["notes"].isna().sum()
    report["issues"]["missing_notes"] = int(missing_notes)
    print(f"  [fix] Cleaned notes text. {missing_notes} activities have no notes")

    # 4d. Flag orphaned activities (deal_id not found in deals table)
    df["orphaned_deal"] = ~df["deal_id"].isin(valid_deal_ids)
    n_orphaned = df["orphaned_deal"].sum()
    orphaned_deal_ids = df[df["orphaned_deal"]]["deal_id"].unique().tolist()
    report["issues"]["orphaned_activities"] = int(n_orphaned)
    report["issues"]["orphaned_deal_ids"] = orphaned_deal_ids
    print(f"  [flag] {n_orphaned} activities reference non-existent deal IDs: {orphaned_deal_ids}")

    report["clean_rows"] = len(df)
    print(f"  âœ“ Activities clean: {len(df)} rows")
    return df, report


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# STEP 5: CLEAN EMAILS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def clean_emails(path: str, valid_deal_ids: set) -> tuple[pd.DataFrame, dict]:
    """
    Cleans the emails table.
    Fixes: stray dots in sender/receiver, missing @, ALLCAPS subjects,
           whitespace in subject, 5 timestamp formats, orphan deal refs.
    """
    print("\n" + "=" * 60)
    print("STEP 5: Cleaning emails.csv")
    print("=" * 60)

    df = pd.read_csv(path, dtype=str)
    report = {"source": "emails.csv", "raw_rows": len(df), "issues": {}}
    print(f"  Loaded {len(df)} rows | Columns: {list(df.columns)}")

    # Drop fully empty rows
    df = df.dropna(how="all").reset_index(drop=True)

    # 5a. Fix stray dots and validate sender/receiver emails
    df["sender"] = df["sender"].apply(fix_stray_dots_email)
    df["receiver"] = df["receiver"].apply(fix_stray_dots_email)
    df["sender_status"] = df["sender"].apply(validate_email)
    df["receiver_status"] = df["receiver"].apply(validate_email)
    sender_counts = df["sender_status"].value_counts().to_dict()
    receiver_counts = df["receiver_status"].value_counts().to_dict()
    report["issues"]["sender_email_status"] = sender_counts
    report["issues"]["receiver_email_status"] = receiver_counts
    print(f"  [fix+flag] Sender status: {sender_counts}")
    print(f"  [fix+flag] Receiver status: {receiver_counts}")

    # 5b. Clean subject: strip whitespace, title-case ALL-CAPS subjects
    df["subject"] = df["subject"].astype(str).str.strip()
    df["subject"] = df["subject"].replace({"nan": np.nan, "": np.nan})

    def fix_subject_casing(subj):
        if pd.isna(subj):
            return subj
        letters = [c for c in str(subj) if c.isalpha()]
        if letters and sum(1 for c in letters if c.isupper()) / len(letters) > 0.8:
            return str(subj).capitalize()
        return str(subj).strip()
    df["subject"] = df["subject"].apply(fix_subject_casing)
    missing_subject = df["subject"].isna().sum()
    report["issues"]["missing_subject"] = int(missing_subject)
    print(f"  [fix] Cleaned subject text. {missing_subject} emails have no subject")

    # 5c. Parse sent_timestamp
    df["sent_timestamp"] = parse_flexible_dates(df["sent_timestamp"])
    missing_ts = df["sent_timestamp"].isna().sum()
    report["issues"]["missing_sent_timestamp"] = int(missing_ts)
    print(f"  [fix] Parsed sent_timestamp. Missing: {missing_ts}")

    # 5d. Flag orphaned emails (deal_id not found in deals table)
    df["orphaned_deal"] = ~df["deal_id"].isin(valid_deal_ids)
    n_orphaned = df["orphaned_deal"].sum()
    orphaned_deal_ids = df[df["orphaned_deal"]]["deal_id"].unique().tolist()
    report["issues"]["orphaned_emails"] = int(n_orphaned)
    report["issues"]["orphaned_deal_ids"] = orphaned_deal_ids
    print(f"  [flag] {n_orphaned} emails reference non-existent deal IDs: {orphaned_deal_ids}")

    # 5e. Derive sentiment hint from email_body keywords
    POSITIVE_KEYWORDS = [
        "appreciate", "great", "excited", "forward", "quick turnaround",
        "looks great", "schedule", "thank"
    ]
    NEGATIVE_KEYWORDS = [
        "not happy", "escalate", "delay", "longer than expected", "asap",
        "other vendors", "isn't resolved", "resolved"
    ]
    NEUTRAL_KEYWORDS = [
        "attached", "documents", "pricing", "conversation", "call"
    ]

    def classify_sentiment(body):
        if pd.isna(body) or str(body).strip() == "":
            return "unknown"
        b = str(body).lower()
        pos = any(kw in b for kw in POSITIVE_KEYWORDS)
        neg = any(kw in b for kw in NEGATIVE_KEYWORDS)
        if pos and not neg:
            return "positive"
        if neg and not pos:
            return "negative"
        if neg and pos:
            return "mixed"
        return "neutral"

    df["sentiment"] = df["email_body"].apply(classify_sentiment)
    sentiment_dist = df["sentiment"].value_counts().to_dict()
    report["issues"]["email_sentiment_distribution"] = sentiment_dist
    print(f"  [feature] Email sentiment distribution: {sentiment_dist}")

    report["clean_rows"] = len(df)
    print(f"  âœ“ Emails clean: {len(df)} rows")
    return df, report


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# STEP 6: BUILD MASTER JOIN TABLE
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def build_master_table(
    deals: pd.DataFrame,
    customers: pd.DataFrame,
    users: pd.DataFrame,
    activities: pd.DataFrame,
    emails: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """
    Joins all 5 clean tables into a single master analytics table.

    Join strategy:
      deals â† LEFT JOIN customers  ON customer_id
      deals â† LEFT JOIN users       ON salesperson_id = user_id
      deals â† LEFT JOIN activity counts  (grouped by deal_id)
      deals â† LEFT JOIN email counts     (grouped by deal_id)

    Result: one row per deal, enriched with customer, rep, and engagement data.
    """
    print("\n" + "=" * 60)
    print("STEP 6: Building Master Join Table")
    print("=" * 60)

    report = {"source": "master_salespulse", "issues": {}}

    # 6a. Activity counts per deal (excluding orphaned)
    act_counts = (
        activities[~activities["orphaned_deal"]]
        .groupby("deal_id")
        .agg(
            activity_count=("activity_id", "count"),
            last_activity_date=("activity_date", "max"),
        )
        .reset_index()
    )
    print(f"  Activity aggregation: {len(act_counts)} deals have activity records")

    # 6b. Activity type breakdown per deal (pivot)
    act_types = (
        activities[~activities["orphaned_deal"]]
        .groupby(["deal_id", "activity_type"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    act_types.columns = ["deal_id"] + [f"act_{c}" for c in act_types.columns[1:]]

    # 6c. Email counts per deal (excluding orphaned)
    email_counts = (
        emails[~emails["orphaned_deal"]]
        .groupby("deal_id")
        .agg(
            email_count=("email_id", "count"),
            last_email_date=("sent_timestamp", "max"),
            positive_emails=("sentiment", lambda x: (x == "positive").sum()),
            negative_emails=("sentiment", lambda x: (x == "negative").sum()),
        )
        .reset_index()
    )
    print(f"  Email aggregation: {len(email_counts)} deals have email records")

    # 6d. Prepare customers for join (keep essential cols, rename for clarity)
    cust_cols = {
        "customer_id": "customer_id",
        "company_name": "customer_company",
        "contact_person": "customer_contact",
        "email": "customer_email",
        "phone_number": "customer_phone",
        "email_status": "customer_email_status",
    }
    cust_join = customers[list(cust_cols.keys())].rename(columns=cust_cols)

    # 6e. Prepare users for join
    user_cols = {
        "user_id": "salesperson_id",
        "name": "salesperson_name",
        "email": "salesperson_email",
        "role": "salesperson_role",
        "email_status": "salesperson_email_status",
    }
    user_join = users[list(user_cols.keys())].rename(columns=user_cols)

    # 6f. Build master â€” start from deals
    master = deals.copy()

    # Join customers
    before = len(master)
    master = master.merge(cust_join, on="customer_id", how="left")
    unmatched_customers = master["customer_company"].isna().sum()
    report["issues"]["deals_without_matching_customer"] = int(unmatched_customers)
    print(f"  Joined customers: {unmatched_customers} deals have no matching customer")

    # Join users (salesperson)
    master = master.merge(user_join, on="salesperson_id", how="left")
    unmatched_reps = master["salesperson_name"].isna().sum()
    report["issues"]["deals_without_matching_salesperson"] = int(unmatched_reps)
    print(f"  Joined users: {unmatched_reps} deals have no matching salesperson")

    # Join activity counts
    master = master.merge(act_counts, on="deal_id", how="left")
    master = master.merge(act_types, on="deal_id", how="left")
    master["activity_count"] = master["activity_count"].fillna(0).astype(int)

    # Join email counts
    master = master.merge(email_counts, on="deal_id", how="left")
    master["email_count"] = master["email_count"].fillna(0).astype(int)
    master["positive_emails"] = master["positive_emails"].fillna(0).astype(int)
    master["negative_emails"] = master["negative_emails"].fillna(0).astype(int)

    # 6g. Derive engagement score: weighted mix of activities + emails
    master["engagement_score"] = (master["activity_count"] * 2) + master["email_count"]

    # 6h. Verify row count preserved (should match deals)
    assert len(master) == before, f"Row count changed after joins! {before} â†’ {len(master)}"
    print(f"  âœ“ Row count preserved: {len(master)} rows (= deals count)")

    report["master_rows"] = len(master)
    report["master_columns"] = list(master.columns)
    print(f"  âœ“ Master table: {len(master)} rows Ã— {len(master.columns)} columns")
    return master, report


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# STEP 7: SAVE OUTPUTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def save_outputs(
    users: pd.DataFrame,
    customers: pd.DataFrame,
    deals: pd.DataFrame,
    activities: pd.DataFrame,
    emails: pd.DataFrame,
    master: pd.DataFrame,
    full_report: dict,
):
    """Saves all clean DataFrames and the quality report to disk."""
    print("\n" + "=" * 60)
    print("STEP 7: Saving Outputs")
    print("=" * 60)

    files = {
        "clean_users.csv": users,
        "clean_customers.csv": customers,
        "clean_deals.csv": deals,
        "clean_activities.csv": activities,
        "clean_emails.csv": emails,
        "master_salespulse.csv": master,
    }

    for fname, df in files.items():
        path = os.path.join(PROC_DIR, fname)
        df.to_csv(path, index=False)
        print(f"  âœ“ Saved {fname} â†’ {path} ({len(df)} rows)")

    # Save JSON quality report
    report_path = os.path.join(OUT_DIR, "salespulse_data_quality_report.json")
    # Convert numpy int64 to Python int for JSON serialisation
    def convert(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        raise TypeError(f"Not JSON serialisable: {type(obj)}")

    with open(report_path, "w") as f:
        json.dump(full_report, f, indent=2, default=convert)
    print(f"  âœ“ Saved quality report â†’ {report_path}")


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# MAIN PIPELINE RUNNER
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def run_pipeline():
    start_time = datetime.now()

    print("\n" + "â–ˆ" * 60)
    print("  SALESPULSE REAL DATA PIPELINE  â€”  START")
    print("  " + start_time.strftime("%Y-%m-%d %H:%M:%S"))
    print("â–ˆ" * 60)

    full_report = {
        "pipeline": "SalesPulse Real Data Pipeline",
        "run_timestamp": start_time.isoformat(),
        "source_directory": RAW_DIR,
        "tables": {},
    }

    # â”€â”€ Step 1: Users
    clean_users_df, user_report = clean_users(
        os.path.join(RAW_DIR, "users.csv")
    )
    full_report["tables"]["users"] = user_report

    # â”€â”€ Step 2: Customers
    clean_customers_df, cust_report = clean_customers(
        os.path.join(RAW_DIR, "customers.csv")
    )
    full_report["tables"]["customers"] = cust_report

    # â”€â”€ Step 3: Deals
    clean_deals_df, deal_report = clean_deals(
        os.path.join(RAW_DIR, "deals.csv")
    )
    full_report["tables"]["deals"] = deal_report

    # Build set of valid deal IDs for orphan detection
    valid_deal_ids = set(clean_deals_df["deal_id"].dropna().unique())

    # â”€â”€ Step 4: Activities
    clean_activities_df, act_report = clean_activities(
        os.path.join(RAW_DIR, "activities.csv"), valid_deal_ids
    )
    full_report["tables"]["activities"] = act_report

    # â”€â”€ Step 5: Emails
    clean_emails_df, email_report = clean_emails(
        os.path.join(RAW_DIR, "emails.csv"), valid_deal_ids
    )
    full_report["tables"]["emails"] = email_report

    # â”€â”€ Step 6: Master join
    master_df, master_report = build_master_table(
        clean_deals_df,
        clean_customers_df,
        clean_users_df,
        clean_activities_df,
        clean_emails_df,
    )
    full_report["tables"]["master"] = master_report

    # â”€â”€ Step 7: Save everything
    save_outputs(
        clean_users_df,
        clean_customers_df,
        clean_deals_df,
        clean_activities_df,
        clean_emails_df,
        master_df,
        full_report,
    )

    # â”€â”€ Summary
    elapsed = (datetime.now() - start_time).total_seconds()
    print("\n" + "â–ˆ" * 60)
    print("  PIPELINE COMPLETE")
    print(f"  Elapsed: {elapsed:.2f}s")
    print("  Output files:")
    print(f"    data/processed/clean_users.csv        ({len(clean_users_df)} rows)")
    print(f"    data/processed/clean_customers.csv     ({len(clean_customers_df)} rows)")
    print(f"    data/processed/clean_deals.csv         ({len(clean_deals_df)} rows)")
    print(f"    data/processed/clean_activities.csv    ({len(clean_activities_df)} rows)")
    print(f"    data/processed/clean_emails.csv        ({len(clean_emails_df)} rows)")
    print(f"    data/processed/master_salespulse.csv   ({len(master_df)} rows Ã— {len(master_df.columns)} cols)")
    print(f"    output/salespulse_data_quality_report.json")
    print("â–ˆ" * 60)

    return master_df


if __name__ == "__main__":
    run_pipeline()

