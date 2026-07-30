"""
Feature Engineering & Derived Business Columns
----------------------------------------------
Assignment 16 - Kalvium SalesPulse Feature Engineering Pipeline

This script implements feature engineering techniques to convert raw customer counts
into business-meaningful metrics:
1. Ratio & Velocity Features (transactions per month, avg spend, LTV per month)
2. Equal-Width Binning with pd.cut (Engagement Tiers)
3. Equal-Frequency Binning with pd.qcut (Spend Quartiles)
4. Multi-dimensional Composite Scoring (RFM Score)
5. Feature Validation, Range Checks, & Distribution Auditing
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def create_synthetic_customer_features(num_records=250, seed=42):
    """
    Generate synthetic raw customer dataset with transactional activity.
    
    Columns:
      - customer_id: Unique customer identifier
      - total_transactions: Raw count of transactions
      - days_as_customer: Total customer tenure in days
      - total_spent: Total lifetime revenue ($)
      - days_since_last_purchase: Recency in days
      - purchase_count: Frequency count
    """
    np.random.seed(seed)
    
    days_as_customer = np.random.randint(30, 730, size=num_records) # 1 month to 2 years
    total_transactions = np.random.poisson(lam=15, size=num_records) + 1
    avg_order_val = np.random.uniform(25.0, 200.0, size=num_records)
    total_spent = np.round(total_transactions * avg_order_val, 2)
    
    days_since_last_purchase = np.random.randint(1, 90, size=num_records)
    purchase_count = total_transactions
    
    df = pd.DataFrame({
        'customer_id': [f"CUST_{2000 + i}" for i in range(num_records)],
        'total_transactions': total_transactions,
        'days_as_customer': days_as_customer,
        'total_spent': total_spent,
        'days_since_last_purchase': days_since_last_purchase,
        'purchase_count': purchase_count
    })
    
    return df


# Task 1: Compute Ratio Features
def compute_ratio_features(df):
    """
    Compute normalized ratio and velocity metrics.
    
    Features:
      1. transactions_per_month = total_transactions / (days_as_customer / 30)
      2. avg_spend_per_transaction = total_spent / total_transactions
      3. lifetime_value_per_month = total_spent / (days_as_customer / 30)
    """
    df_feat = df.copy()
    print("\n--- TASK 1: COMPUTE RATIO FEATURES ---")
    
    tenure_months = df_feat['days_as_customer'] / 30.0
    
    df_feat['transactions_per_month'] = df_feat['total_transactions'] / tenure_months
    df_feat['avg_spend_per_transaction'] = df_feat['total_spent'] / df_feat['total_transactions']
    df_feat['lifetime_value_per_month'] = df_feat['total_spent'] / tenure_months
    
    print("Statistical Summary of Computed Ratio Features:")
    print(df_feat[['transactions_per_month', 'avg_spend_per_transaction', 'lifetime_value_per_month']].describe().round(2))
    
    return df_feat


# Task 2: Binning with Equal-Width Bins (pd.cut)
def bin_engagement_tiers(df):
    """
    Segment transactions_per_month into fixed range bins using pd.cut.
    
    Bins:
      - (0, 2]: 'low'
      - (2, 10]: 'medium'
      - (10, inf]: 'high'
    """
    df_feat = df.copy()
    print("\n--- TASK 2: BINNING WITH EQUAL-WIDTH BINS (pd.cut) ---")
    
    df_feat['engagement_tier'] = pd.cut(
        df_feat['transactions_per_month'],
        bins=[0, 2, 10, float('inf')],
        labels=['low', 'medium', 'high'],
        include_lowest=True
    )
    
    print("Engagement Tier Distribution:")
    print(df_feat['engagement_tier'].value_counts())
    
    return df_feat


# Task 3: Binning with Quantiles (pd.qcut)
def bin_spend_quartiles(df):
    """
    Segment total_spent into equal-frequency quartile bins using pd.qcut.
    
    Quantiles: Q1 (0-25%), Q2 (25-50%), Q3 (50-75%), Q4 (75-100%)
    """
    df_feat = df.copy()
    print("\n--- TASK 3: BINNING WITH QUANTILES (pd.qcut) ---")
    
    df_feat['spend_quartile'] = pd.qcut(
        df_feat['total_spent'],
        q=4,
        labels=['Q1', 'Q2', 'Q3', 'Q4']
    )
    
    print("Spend Quartile Distribution:")
    print(df_feat['spend_quartile'].value_counts())
    
    return df_feat


# Task 4: Composite Score (RFM Score)
def compute_composite_rfm_score(df):
    """
    Construct composite RFM (Recency, Frequency, Monetary) score.
    
    Recency: Inverse scoring (1 = old, 5 = recent)
    Frequency & Monetary: Direct scoring (1 = low, 5 = high)
    """
    df_feat = df.copy()
    print("\n--- TASK 4: COMPOSITE SCORE (RFM) ---")
    
    # Use rank(method='first') to ensure unique quantiles without bin edge collisions
    df_feat['recency_score'] = pd.qcut(
        df_feat['days_since_last_purchase'].rank(method='first'), 
        q=5, 
        labels=[5, 4, 3, 2, 1]
    )
    
    df_feat['frequency_score'] = pd.qcut(
        df_feat['purchase_count'].rank(method='first'), 
        q=5, 
        labels=[1, 2, 3, 4, 5]
    )
    
    df_feat['monetary_score'] = pd.qcut(
        df_feat['total_spent'].rank(method='first'), 
        q=5, 
        labels=[1, 2, 3, 4, 5]
    )
    
    df_feat['rfm_score'] = (
        df_feat['recency_score'].astype(int) + 
        df_feat['frequency_score'].astype(int) + 
        df_feat['monetary_score'].astype(int)
    )
    
    print("RFM Composite Score Summary:")
    print(df_feat[['recency_score', 'frequency_score', 'monetary_score', 'rfm_score']].head(10))
    print(f"\nRFM Score Range: {df_feat['rfm_score'].min()} (Lowest) to {df_feat['rfm_score'].max()} (Highest)")
    
    return df_feat


# Task 5: Feature Validation
def validate_engineered_features(df):
    """
    Audit feature distributions, check range bounds, and ensure zero missing values.
    """
    print("\n--- TASK 5: FEATURE VALIDATION ---")
    
    print(f"Engagement Tier Distribution:\n{df['engagement_tier'].value_counts()}")
    print(f"\nSpend Quartile Distribution:\n{df['spend_quartile'].value_counts()}")
    print(f"\nRFM Score Range: Min={df['rfm_score'].min()}, Max={df['rfm_score'].max()}")
    
    # Check for unexpected NaNs
    target_cols = ['transactions_per_month', 'avg_spend_per_transaction', 
                   'engagement_tier', 'spend_quartile', 'rfm_score']
    
    null_counts = df[target_cols].isna().sum()
    print(f"\nMissing Values Check across Engineered Columns:\n{null_counts}")
    
    assert null_counts.sum() == 0, "Validation Failed: Engineered features contain unexpected missing values!"
    print("\n[OK] Validation Passed: Zero missing values detected across all engineered features.")


def generate_feature_plots(df):
    """Generate visual feature distribution plots."""
    os.makedirs('output', exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # 1. Transactions per Month Distribution
    sns.histplot(df['transactions_per_month'], ax=axes[0, 0], kde=True, color='#2b5c8f')
    axes[0, 0].set_title('Transactions Per Month (Ratio Feature)')
    axes[0, 0].set_xlabel('Transactions / Month')
    
    # 2. Engagement Tier Distribution
    sns.countplot(data=df, x='engagement_tier', hue='engagement_tier', ax=axes[0, 1], palette='viridis', legend=False)
    axes[0, 1].set_title('Engagement Tiers (Equal-Width pd.cut)')
    axes[0, 1].set_xlabel('Tier')
    
    # 3. Spend Quartile Distribution
    sns.countplot(data=df, x='spend_quartile', hue='spend_quartile', ax=axes[1, 0], palette='Set2', legend=False)
    axes[1, 0].set_title('Spend Quartiles (Equal-Frequency pd.qcut)')
    axes[1, 0].set_xlabel('Quartile')
    
    # 4. RFM Score Distribution
    sns.histplot(df['rfm_score'], ax=axes[1, 1], bins=13, color='#e7298a', discrete=True)
    axes[1, 1].set_title('RFM Composite Score Distribution (3 to 15)')
    axes[1, 1].set_xlabel('RFM Score')
    
    plt.tight_layout()
    plt.savefig('output/feature_engineering_distributions.png')
    plt.close()
    
    print("\nSaved visualization plot to 'output/feature_engineering_distributions.png'.")


def run_pipeline():
    """Execute full feature engineering pipeline."""
    print("=========================================================")
    print("     FEATURE ENGINEERING & DERIVED COLUMNS PIPELINE      ")
    print("=========================================================")
    
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # 1. Generate synthetic raw data
    raw_df = create_synthetic_customer_features()
    raw_df.to_csv('data/raw/raw_customer_features.csv', index=False)
    print("\nLoaded raw customer dataset ('data/raw/raw_customer_features.csv'):")
    print(raw_df.head())
    
    # 2. Task 1: Ratio Features
    df_t1 = compute_ratio_features(raw_df)
    
    # 3. Task 2: Equal-Width Binning (pd.cut)
    df_t2 = bin_engagement_tiers(df_t1)
    
    # 4. Task 3: Equal-Frequency Binning (pd.qcut)
    df_t3 = bin_spend_quartiles(df_t2)
    
    # 5. Task 4: Composite Score (RFM)
    df_t4 = compute_composite_rfm_score(df_t3)
    
    # 6. Task 5: Feature Validation
    validate_engineered_features(df_t4)
    
    # Save visualizations & final dataset
    generate_feature_plots(df_t4)
    df_t4.to_csv('data/processed/feature_engineered_data.csv', index=False)
    
    print("\nSaved processed feature dataset to 'data/processed/feature_engineered_data.csv'.")
    print("Pipeline Execution Completed Successfully.")


if __name__ == '__main__':
    run_pipeline()
