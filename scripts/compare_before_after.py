"""
compare_before_after.py
-----------------------
Shows a before/after summary of all data cleaning applied
to the raw_new CRM datasets (users, customers, deals, activities, emails).

Usage:
    python scripts/compare_before_after.py
"""

import os
import sys
import io
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW  = os.path.join(ROOT, "data", "raw_new")
PROC = os.path.join(ROOT, "data", "processed")


def divider(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def sub(title):
    print(f"\n  -- {title}")


# ===========================================================================
# USERS
# ===========================================================================
divider("USERS  (users.csv)")
u_raw   = pd.read_csv(os.path.join(RAW,  "users.csv"))
u_clean = pd.read_csv(os.path.join(PROC, "clean_users.csv"))

sub("Row counts")
print(f"    BEFORE : {len(u_raw):>6} rows")
print(f"    AFTER  : {len(u_clean):>6} rows")

sub("Name casing fixes (ALL-CAPS + trailing whitespace)")
raw_names = u_raw["name"].str.strip().tolist()
cln_names = u_clean["name"].tolist()
for b, a in zip(raw_names, cln_names):
    if b != a:
        print(f"      BEFORE: {b!r}  ->  AFTER: {a!r}")

sub("Missing role filled with 'unknown'")
before_nulls = u_raw["role"].isna().sum()
after_nulls  = u_clean["role"].isna().sum()
print(f"    BEFORE nulls: {before_nulls}  |  AFTER nulls: {after_nulls}")

sub("Email status flags (new column added)")
if "email_status" in u_clean.columns:
    print("   ", u_clean["email_status"].value_counts().to_dict())


# ===========================================================================
# CUSTOMERS
# ===========================================================================
divider("CUSTOMERS  (customers.csv)")
c_raw   = pd.read_csv(os.path.join(RAW,  "customers.csv"))
c_clean = pd.read_csv(os.path.join(PROC, "clean_customers.csv"))

sub("Row counts (duplicate removal)")
print(f"    BEFORE : {len(c_raw):>6} rows")
removed = len(c_raw) - len(c_clean)
print(f"    AFTER  : {len(c_clean):>6} rows  (removed {removed} exact duplicates)")

sub("Duplicate customer_ids found & removed")
dup_mask = c_raw.duplicated(subset=["customer_id"], keep=False)
dup_ids  = c_raw.loc[dup_mask, "customer_id"].unique()
print(f"    {list(dup_ids)}")

sub("Company name casing (sample of changes)")
shown = 0
raw_names = c_raw["company_name"].str.strip().tolist()
cln_names = c_clean["company_name"].tolist()
for b, a in zip(raw_names, cln_names):
    if b != a and shown < 5:
        print(f"      BEFORE: {b!r}  ->  AFTER: {a!r}")
        shown += 1

sub("Null counts per column")
for col in ["contact_person", "phone_number", "email"]:
    r = c_raw[col].isna().sum()  if col in c_raw.columns   else "N/A"
    c = c_clean[col].isna().sum() if col in c_clean.columns else "N/A"
    print(f"    {col:<20}: BEFORE={r}  ->  AFTER={c}")

sub("Email validation breakdown (new 'email_status' column)")
if "email_status" in c_clean.columns:
    print("   ", c_clean["email_status"].value_counts().to_dict())


# ===========================================================================
# DEALS
# ===========================================================================
divider("DEALS  (deals.csv)")
d_raw   = pd.read_csv(os.path.join(RAW,  "deals.csv"))
d_clean = pd.read_csv(os.path.join(PROC, "clean_deals.csv"))

sub("Row counts")
print(f"    BEFORE : {len(d_raw):>6} rows")
print(f"    AFTER  : {len(d_clean):>6} rows")

sub("deal_value: mixed string formats  ->  clean float")
print("    RAW   (first 8):", d_raw["deal_value"].head(8).tolist())
print("    CLEAN (first 8):", d_clean["deal_value"].head(8).tolist())
before_null = d_raw["deal_value"].isna().sum()
after_null  = d_clean["deal_value"].isna().sum()
print(f"    Nulls: BEFORE={before_null}  ->  AFTER={after_null}")

sub("current_stage: 20+ raw variants  ->  6 canonical labels")
print("    RAW (top 12 variants):")
for val, cnt in d_raw["current_stage"].value_counts().head(12).items():
    print(f"      {cnt:>4}x  {val!r}")
print("    CLEAN (canonical):")
for val, cnt in d_clean["current_stage"].value_counts().items():
    print(f"      {cnt:>4}x  {val!r}")

sub("status: mixed case normalised to lowercase")
print("    RAW  :", d_raw["status"].value_counts().to_dict())
print("    CLEAN:", d_clean["status"].value_counts().to_dict())

sub("Dates: multi-format parsed to standard datetime")
for col in ["created_date", "closed_date"]:
    r = d_raw[col].isna().sum()  if col in d_raw.columns   else "?"
    c = d_clean[col].isna().sum() if col in d_clean.columns else "?"
    print(f"    {col:<20}: BEFORE={r}  ->  AFTER={c}")

if "date_logic_error" in d_clean.columns:
    bad = d_clean[d_clean["date_logic_error"] == True]
    sub(f"Date logic errors flagged (closed_date before created_date): {len(bad)}")
    if len(bad):
        print(bad[["deal_id", "created_date", "closed_date"]].head(6).to_string(index=False))

if "deal_duration_days" in d_clean.columns:
    sub("New derived column: deal_duration_days")
    non_null = d_clean["deal_duration_days"].dropna()
    print(f"    Computed for {len(non_null)} deals | min={non_null.min():.0f} max={non_null.max():.0f} mean={non_null.mean():.1f} days")


# ===========================================================================
# ACTIVITIES
# ===========================================================================
divider("ACTIVITIES  (activities.csv)")
a_raw   = pd.read_csv(os.path.join(RAW,  "activities.csv"))
a_clean = pd.read_csv(os.path.join(PROC, "clean_activities.csv"))

sub("Row counts")
print(f"    BEFORE : {len(a_raw):>6} rows")
print(f"    AFTER  : {len(a_clean):>6} rows")

sub("activity_type: ALLCAPS + dashes  ->  snake_case")
print("    RAW:")
for val, cnt in a_raw["activity_type"].value_counts().items():
    print(f"      {cnt:>4}x  {val!r}")
print("    CLEAN:")
for val, cnt in a_clean["activity_type"].value_counts().items():
    print(f"      {cnt:>4}x  {val!r}")

sub("activity_date null counts")
r = a_raw["activity_date"].isna().sum()  if "activity_date" in a_raw.columns   else "N/A"
c = a_clean["activity_date"].isna().sum() if "activity_date" in a_clean.columns else "N/A"
print(f"    BEFORE={r}  ->  AFTER={c}")

sub("notes: leading/trailing whitespace")
if "notes" in a_raw.columns and "notes" in a_clean.columns:
    nr = a_raw["notes"].dropna()
    nc = a_clean["notes"].dropna()
    raw_ws  = (nr.str.strip() != nr).sum()
    cln_ws  = (nc.str.strip() != nc).sum()
    print(f"    RAW   with extra whitespace: {raw_ws}")
    print(f"    CLEAN with extra whitespace: {cln_ws}")


# ===========================================================================
# EMAILS
# ===========================================================================
divider("EMAILS  (emails.csv)")
e_raw   = pd.read_csv(os.path.join(RAW,  "emails.csv"))
e_clean = pd.read_csv(os.path.join(PROC, "clean_emails.csv"))

sub("Row counts")
print(f"    BEFORE : {len(e_raw):>6} rows")
print(f"    AFTER  : {len(e_clean):>6} rows")

sub("Malformed senders in raw (sample)")
valid_re = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
bad_send = e_raw["sender"].dropna()
bad_send = bad_send[~bad_send.str.match(valid_re, na=False)]
print("    RAW malformed (sample):", bad_send.head(5).tolist())
if "sender_status" in e_clean.columns:
    print("    CLEAN sender_status:", e_clean["sender_status"].value_counts().to_dict())

sub("Subject normalisation (ALLCAPS  ->  sentence/title case)")
print("    RAW  (sample):", e_raw["subject"].dropna().head(5).tolist())
print("    CLEAN(sample):", e_clean["subject"].dropna().head(5).tolist())

sub("sent_timestamp null counts")
r = e_raw["sent_timestamp"].isna().sum()  if "sent_timestamp" in e_raw.columns   else "N/A"
c = e_clean["sent_timestamp"].isna().sum() if "sent_timestamp" in e_clean.columns else "N/A"
print(f"    BEFORE={r}  ->  AFTER={c}")

if "sentiment" in e_clean.columns:
    sub("Sentiment (new derived column via keyword scoring)")
    print("   ", e_clean["sentiment"].value_counts().to_dict())


# ===========================================================================
# MASTER TABLE SUMMARY
# ===========================================================================
divider("MASTER SALESPULSE TABLE  (master_salespulse.csv)")
master = pd.read_csv(os.path.join(PROC, "master_salespulse.csv"))
print(f"\n    Shape  : {master.shape[0]} rows x {master.shape[1]} columns")
print(f"    Columns: {list(master.columns)}")

print("\n" + "=" * 70)
print("  CLEANING COMPLETE -- all processed files in data/processed/")
print("=" * 70 + "\n")
