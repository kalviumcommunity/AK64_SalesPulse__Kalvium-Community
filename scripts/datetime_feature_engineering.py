"""
Date & Time Transformation Pipeline
-----------------------------------
Assignment 12 - Kalvium SalesPulse Temporal Feature Engineering Pipeline

This script implements a date and time feature engineering pipeline for
raw transaction timestamps stored as strings.

Tasks Covered:
1. Parse Timestamp Strings with Explicit Format
2. Extract Day-of-Week and Hour-of-Day
3. Compute Week Number and Resample Data
4. Compute Days-Since-Event Metric (Recency)
5. Build Time-Indexed Aggregation & Heatmap
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def create_synthetic_transaction_data(num_records=150, seed=42):
    """
    Generate synthetic transaction dataset with realistic timestamp strings.
    
    Returns:
        pd.DataFrame with transaction records
    """
    np.random.seed(seed)
    customer_ids = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
    
    # Generate random dates over a 60-day period leading up to 2026-07-25
    base_date = pd.Timestamp('2026-07-25 12:00:00')
    dates = []
    cust_list = []
    amounts = []
    
    for i in range(num_records):
        days_offset = np.random.randint(0, 60)
        # Bimodal hour distribution (lunch peak ~12-14, evening peak ~18-21)
        if np.random.rand() < 0.6:
            hour = np.random.choice([11, 12, 13, 14, 18, 19, 20, 21])
        else:
            hour = np.random.randint(8, 23)
            
        minute = np.random.randint(0, 60)
        second = np.random.randint(0, 60)
        
        tx_dt = base_date - pd.Timedelta(days=days_offset, hours=hour, minutes=minute, seconds=second)
        dates.append(tx_dt.strftime('%Y-%m-%d %H:%M:%S'))
        cust_list.append(np.random.choice(customer_ids))
        amounts.append(round(np.random.uniform(15.0, 450.0), 2))
        
    df = pd.DataFrame({
        'transaction_id': range(1000, 1000 + num_records),
        'customer_id': cust_list,
        'transaction_date': dates,
        'amount': amounts
    })
    
    return df


# Task 1: Parse Timestamp Strings with Explicit Format
def parse_timestamp_column(df, column_name='transaction_date', date_format='%Y-%m-%d %H:%M:%S'):
    """
    Convert string dates to datetime type using explicit format specification.
    
    Why Explicit Format is Required:
        Pandas datetime inference without format can fail or silently misinterpret 
        ambiguous date formats (e.g., '01-02-2025' as Jan 2 vs Feb 1). Supplying 
        explicit format guarantees fast, unambiguous, deterministic parsing.
        
    Args:
        df: pandas DataFrame
        column_name: name of date string column
        date_format: str, explicit format string
        
    Returns:
        df: DataFrame with converted datetime column
    """
    df_parsed = df.copy()
    print("\n--- TASK 1: PARSE TIMESTAMP STRINGS ---")
    print(f"Original dtype of '{column_name}': {df_parsed[column_name].dtype}")
    
    df_parsed[column_name] = pd.to_datetime(
        df_parsed[column_name],
        format=date_format
    )
    
    print(f"Parsed dtype of '{column_name}': {df_parsed[column_name].dtype}")
    print(f"Min transaction timestamp: {df_parsed[column_name].min()}")
    print(f"Max transaction timestamp: {df_parsed[column_name].max()}")
    
    return df_parsed


# Task 2: Extract Day-of-Week and Hour-of-Day
def extract_temporal_features(df, datetime_col='transaction_date'):
    """
    Extract time-of-day and calendar features from parsed datetime column.
    
    Extracted Features:
        1. day_of_week: Full string day name (e.g. 'Monday')
        2. dow_numeric: Integer day of week (0=Monday, 6=Sunday)
        3. hour: Hour of day (0-23)
        4. month: Month of year (1-12)
        5. quarter: Calendar quarter (1-4)
    """
    df_feat = df.copy()
    print("\n--- TASK 2: EXTRACT TEMPORAL FEATURES ---")
    
    df_feat['day_of_week'] = df_feat[datetime_col].dt.day_name()
    df_feat['dow_numeric'] = df_feat[datetime_col].dt.dayofweek
    df_feat['hour'] = df_feat[datetime_col].dt.hour
    df_feat['month'] = df_feat[datetime_col].dt.month
    df_feat['quarter'] = df_feat[datetime_col].dt.quarter
    
    print("Sample extracted temporal features:")
    print(df_feat[['transaction_date', 'day_of_week', 'dow_numeric', 'hour', 'month', 'quarter']].head())
    
    print("\nHourly Transaction Volume Distribution:")
    print(df_feat['hour'].value_counts().sort_index())
    
    print("\nDaily Transaction Volume Distribution:")
    print(df_feat['day_of_week'].value_counts())
    
    return df_feat


# Task 3: Compute Week Number and Resample Data
def resample_weekly_metrics(df, datetime_col='transaction_date', amount_col='amount'):
    """
    Extract week number and perform weekly time-series resampling.
    
    Args:
        df: pandas DataFrame
        datetime_col: timestamp column name
        amount_col: numeric value column name
        
    Returns:
        df: DataFrame with week_num added
        weekly_summary: DataFrame of weekly resampled revenue metrics
    """
    df_res = df.copy()
    print("\n--- TASK 3: WEEK NUMBER & RESAMPLING ---")
    
    df_res['week_num'] = df_res[datetime_col].dt.isocalendar().week
    
    # Resample requires datetime index
    df_ts = df_res.set_index(datetime_col)
    
    weekly_summary = df_ts[amount_col].resample('W').agg(['sum', 'count', 'mean']).rename(
        columns={'sum': 'total_revenue', 'count': 'transaction_count', 'mean': 'avg_order_value'}
    )
    
    print("Weekly Resampled Financial Metrics (Last 5 Weeks):")
    print(weekly_summary.tail(5))
    
    return df_res, weekly_summary


# Task 4: Compute Days-Since-Event Metric (Recency)
def compute_customer_recency(df, datetime_col='transaction_date', reference_date=None):
    """
    Compute days since last purchase for churn risk profiling.
    
    Formula:
        days_since_last_purchase = (reference_date - max(customer_purchase_date)).dt.days
    """
    df_rec = df.copy()
    print("\n--- TASK 4: DAYS-SINCE-EVENT (RECENCY) METRIC ---")
    
    if reference_date is None:
        reference_date = df_rec[datetime_col].max() + pd.Timedelta(days=1)
        
    print(f"Reference evaluation timestamp: {reference_date}")
    
    # Calculate last purchase date per customer
    last_purchases = df_rec.groupby('customer_id')[datetime_col].max().reset_index()
    last_purchases['days_since_last_purchase'] = (reference_date - last_purchases[datetime_col]).dt.days
    
    print("\nCustomer Recency Summary:")
    print(last_purchases[['customer_id', datetime_col, 'days_since_last_purchase']].head(10))
    
    print("\nRecency Statistical Distribution:")
    print(last_purchases['days_since_last_purchase'].describe())
    
    # Merge recency back into original dataset
    df_rec = df_rec.merge(last_purchases[['customer_id', 'days_since_last_purchase']], on='customer_id', how='left')
    
    # Identify churn-risk customers (> 30 days inactive)
    churn_risk = last_purchases[last_purchases['days_since_last_purchase'] > 30]
    print(f"\nIdentified {len(churn_risk)} high churn-risk customers (> 30 days inactive):")
    print(churn_risk[['customer_id', 'days_since_last_purchase']])
    
    return df_rec, last_purchases


# Task 5: Build Time-Indexed Aggregation & Heatmap
def build_time_indexed_aggregations(df):
    """
    Group by day_of_week and hour to create multi-dimensional aggregations and pivot tables.
    """
    print("\n--- TASK 5: TIME-INDEXED MULTI-DIMENSIONAL AGGREGATIONS ---")
    
    # Ordered day names for logical sorting
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=day_order, ordered=True)
    
    # Multi-level groupby aggregation
    hourly_daily_agg = df.groupby(['day_of_week', 'hour'], observed=False)['amount'].agg(
        ['sum', 'count', 'mean']
    ).reset_index()
    
    print("Multi-level GroupBy Aggregation (Sample rows):")
    print(hourly_daily_agg.dropna().head(10))
    
    # Pivot table (Hour x Day of Week)
    pivot_table = pd.pivot_table(
        df,
        values='amount',
        index='hour',
        columns='day_of_week',
        aggfunc='sum',
        observed=False
    ).fillna(0)
    
    print("\nPivot Table Revenue Matrix (Hour vs Day of Week):")
    print(pivot_table.head(10))
    
    # Identify peak revenue window
    max_rev = pivot_table.max().max()
    peak_loc = pivot_table.stack().idxmax()
    print(f"\nPeak Activity Window: Hour {peak_loc[0]} on {peak_loc[1]} with Total Revenue ${max_rev:.2f}")
    
    return hourly_daily_agg, pivot_table


def test_edge_cases_and_timezones():
    """
    Demonstrate testing edge cases and multi-timezone timestamp conversions.
    """
    print("\n" + "="*50)
    print("EDGE CASE & MULTI-TIMEZONE HANDLING TESTS")
    print("="*50)
    
    # Test formats
    test_dates = [
        '2025-01-15 14:30:45',        # Standard format
        '2025-1-15 14:30:45',         # Single digit month
        '2025/01/15 14:30:45',        # Slash separator
        '2025-01-15T14:30:45Z',       # ISO 8601 UTC string
    ]
    
    print("\nTesting timestamp string parsing resilience:")
    for date_str in test_dates:
        try:
            parsed = pd.to_datetime(date_str)
            print(f"[OK] Parsed '{date_str}' -> {parsed} (type: {type(parsed)})")
        except Exception as e:
            print(f"[FAIL] Failed '{date_str}': {e}")
            
    # Multi-timezone handling
    print("\nMulti-Timezone Conversion Demonstration:")
    utc_series = pd.Series(['2026-07-30 10:00:00', '2026-07-30 15:30:00'])
    utc_dt = pd.to_datetime(utc_series).dt.tz_localize('UTC')
    ny_dt = utc_dt.dt.tz_convert('America/New_York')
    ist_dt = utc_dt.dt.tz_convert('Asia/Kolkata')
    
    tz_df = pd.DataFrame({
        'UTC': utc_dt,
        'New_York_EDT': ny_dt,
        'India_IST': ist_dt
    })
    print(tz_df)


def generate_visualizations(df, weekly_summary, pivot_table):
    """Save visualization plots into output directory."""
    os.makedirs('output', exist_ok=True)
    
    # Figure 1: Hourly Distribution
    plt.figure(figsize=(10, 4))
    sns.countplot(data=df, x='hour', hue='hour', palette='viridis', legend=False)
    plt.title('Transaction Volume by Hour of Day')
    plt.xlabel('Hour of Day (0-23)')
    plt.ylabel('Transaction Count')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('output/hourly_distribution.png')
    plt.close()
    
    # Figure 2: Weekly Revenue Trend
    plt.figure(figsize=(10, 4))
    weekly_summary['total_revenue'].plot(kind='line', marker='o', color='#2b5c8f', linewidth=2)
    plt.title('Weekly Revenue Trend (Resampled Weekly)')
    plt.xlabel('Week')
    plt.ylabel('Total Revenue ($)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('output/weekly_revenue_trend.png')
    plt.close()
    
    # Figure 3: Hour x Day Heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, cmap='YlGnBu', annot=False, fmt='.0f', cbar_kws={'label': 'Revenue ($)'})
    plt.title('Transaction Revenue Heatmap (Hour vs Day of Week)')
    plt.xlabel('Day of Week')
    plt.ylabel('Hour of Day')
    plt.tight_layout()
    plt.savefig('output/hour_day_heatmap.png')
    plt.close()
    
    print("\nSaved visualization figures to 'output/' folder:")
    print(" - output/hourly_distribution.png")
    print(" - output/weekly_revenue_trend.png")
    print(" - output/hour_day_heatmap.png")


def run_pipeline():
    """Main execution method for the datetime feature engineering pipeline."""
    print("=========================================================")
    print("      DATE & TIME TRANSFORMATION PIPELINE DEMO           ")
    print("=========================================================")
    
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # 1. Load / Create raw data
    raw_df = create_synthetic_transaction_data()
    raw_df.to_csv('data/raw/raw_transactions.csv', index=False)
    print("\nCreated raw synthetic dataset 'data/raw/raw_transactions.csv'. Sample:")
    print(raw_df.head())
    
    # 2. Task 1: Parse Timestamps
    df_parsed = parse_timestamp_column(raw_df, 'transaction_date', '%Y-%m-%d %H:%M:%S')
    
    # 3. Task 2: Extract Features
    df_feat = extract_temporal_features(df_parsed, 'transaction_date')
    
    # 4. Task 3: Week Number & Resample
    df_res, weekly_summary = resample_weekly_metrics(df_feat, 'transaction_date', 'amount')
    
    # 5. Task 4: Recency Metric
    df_rec, customer_recency = compute_customer_recency(df_res, 'transaction_date')
    
    # 6. Task 5: Multi-dimensional Aggregations
    hourly_daily_agg, pivot_table = build_time_indexed_aggregations(df_rec)
    
    # 7. Edge Cases & Timezones
    test_edge_cases_and_timezones()
    
    # 8. Visualizations & Output Saving
    generate_visualizations(df_rec, weekly_summary, pivot_table)
    
    # Save final dataset
    df_rec.to_csv('data/processed/clean_datetime_data.csv', index=False)
    print("\nSaved final transformed dataset to 'data/processed/clean_datetime_data.csv'.")
    print("Pipeline Execution Completed Successfully.")


if __name__ == '__main__':
    run_pipeline()
