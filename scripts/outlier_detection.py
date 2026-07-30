"""
Outlier Detection with Statistical Methods
------------------------------------------
Assignment 13 - Kalvium SalesPulse Statistical Outlier Pipeline

This script implements Z-score and IQR statistical outlier detection,
applies capping/flagging/removal strategies, generates cleaning logs,
and outputs data quality metrics.

Tasks Covered:
1. Z-Score Outlier Detection
2. IQR Outlier Detection
3. Cap Outliers at Boundaries
4. Flag Outliers with Binary Column
5. Create Audit Cleaning Log
"""

import os
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns


def create_synthetic_customer_data(num_records=200, seed=42):
    """
    Generate synthetic customer dataset containing revenue, age, and spend outliers.
    
    Includes intentional anomalies:
      - Extreme high revenue ($65,000 executive purchase, $150,000 corporate anomaly)
      - Extreme age values (e.g. 150+ years old data entry error)
      - Negative revenue values (data corruption)
    """
    np.random.seed(seed)
    
    # Normal distribution for age (mean 38, std 10) bounded realistically
    age = np.random.normal(loc=38, scale=10, size=num_records).astype(int)
    age = np.clip(age, 18, 70)
    
    # Skewed distribution for revenue (lognormal)
    revenue = np.random.lognormal(mean=5.0, sigma=0.8, size=num_records)
    revenue = np.round(revenue, 2)
    
    df = pd.DataFrame({
        'customer_id': range(1001, 1001 + num_records),
        'age': age,
        'revenue': revenue,
        'loyalty_score': np.round(np.random.uniform(1.0, 10.0, size=num_records), 1)
    })
    
    # Inject intentional extreme outliers
    # 1. Executive / Corporate spend outliers in revenue
    outlier_indices_rev = [5, 23, 87, 142, 189]
    df.loc[outlier_indices_rev[0], 'revenue'] = 65000.00
    df.loc[outlier_indices_rev[1], 'revenue'] = 150000.00
    df.loc[outlier_indices_rev[2], 'revenue'] = 45000.00
    df.loc[outlier_indices_rev[3], 'revenue'] = 82000.00
    df.loc[outlier_indices_rev[4], 'revenue'] = -500.00   # Negative anomaly
    
    # 2. Impossible age outliers
    outlier_indices_age = [12, 58, 119]
    df.loc[outlier_indices_age[0], 'age'] = 150
    df.loc[outlier_indices_age[1], 'age'] = 195
    df.loc[outlier_indices_age[2], 'age'] = -5
    
    return df


# Task 1: Z-Score Outlier Detection
def detect_zscore_outliers(df, column='revenue', threshold=3.0):
    """
    Detect outliers as values beyond +/- threshold standard deviations from mean.
    
    Formula:
        Z = | (X - mean) / std |
        Outlier if Z > 3.0
        
    Note on Assumptions:
        Z-score assumes data is normally distributed. Extreme outliers shift 
        both mean and std, making Z-scores less sensitive on heavily skewed data.
    """
    df_res = df.copy()
    print(f"\n--- TASK 1: Z-SCORE OUTLIER DETECTION ({column}) ---")
    
    z_scores = np.abs(stats.zscore(df_res[column]))
    df_res[f'{column}_zscore'] = z_scores
    df_res[f'is_outlier_zscore_{column}'] = z_scores > threshold
    
    z_outliers = df_res[df_res[f'is_outlier_zscore_{column}']]
    
    print(f"Mean {column}: {df_res[column].mean():.2f}, Std: {df_res[column].std():.2f}")
    print(f"Z-score threshold: |Z| > {threshold}")
    print(f"Detected Z-Score outliers count: {len(z_outliers)}")
    print("Sample Z-Score Outliers:")
    print(z_outliers[['customer_id', column, f'{column}_zscore']].head())
    
    return df_res, z_outliers


# Task 2: IQR Outlier Detection
def detect_iqr_outliers(df, column='revenue', multiplier=1.5):
    """
    Detect outliers beyond Q1 - 1.5*IQR and Q3 + 1.5*IQR.
    
    Formula:
        IQR = Q3 - Q1
        Lower Bound = Q1 - 1.5 * IQR
        Upper Bound = Q3 + 1.5 * IQR
        
    Note on Robustness:
        IQR relies on median and quartiles, making it robust against non-normal, 
        heavily skewed distributions.
    """
    df_res = df.copy()
    print(f"\n--- TASK 2: IQR OUTLIER DETECTION ({column}) ---")
    
    Q1 = df_res[column].quantile(0.25)
    Q3 = df_res[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    df_res[f'is_outlier_iqr_{column}'] = (df_res[column] < lower_bound) | (df_res[column] > upper_bound)
    iqr_outliers = df_res[df_res[f'is_outlier_iqr_{column}']]
    
    print(f"Q1 (25th percentile): {Q1:.2f}")
    print(f"Q3 (75th percentile): {Q3:.2f}")
    print(f"IQR (Q3 - Q1): {IQR:.2f}")
    print(f"Lower Bound (Q1 - 1.5*IQR): {lower_bound:.2f}")
    print(f"Upper Bound (Q3 + 1.5*IQR): {upper_bound:.2f}")
    print(f"Detected IQR outliers count: {len(iqr_outliers)}")
    print("Sample IQR Outliers:")
    print(iqr_outliers[['customer_id', column, f'is_outlier_iqr_{column}']].head())
    
    return df_res, lower_bound, upper_bound, iqr_outliers


# Task 3: Cap Outliers at Boundaries
def cap_outliers(df, column='revenue', lower_bound=None, upper_bound=None):
    """
    Apply Winsorization / Capping strategy.
    Replaces extreme values outside bounds with lower and upper boundary values.
    
    Benefits:
        Preserves all rows in the dataset while bounding extreme statistical influence.
    """
    df_res = df.copy()
    print(f"\n--- TASK 3: CAP OUTLIERS AT BOUNDARIES ({column}) ---")
    
    before_min = df_res[column].min()
    before_max = df_res[column].max()
    
    df_res[f'{column}_capped'] = df_res[column].clip(lower=lower_bound, upper=upper_bound)
    
    after_min = df_res[f'{column}_capped'].min()
    after_max = df_res[f'{column}_capped'].max()
    
    print(f"Before capping '{column}': min = {before_min:.2f}, max = {before_max:.2f}")
    print(f"After capping '{column}':  min = {after_min:.2f}, max = {after_max:.2f}")
    print(f"Total values capped: {((df_res[column] < lower_bound) | (df_res[column] > upper_bound)).sum()}")
    
    return df_res


# Task 4: Flag Outliers with Binary Column
def flag_combined_outliers(df, column='revenue', zscore_threshold=3.0, lower_bound=None, upper_bound=None):
    """
    Create a composite binary flag (0 = Normal, 1 = Outlier) combining Z-score and IQR.
    
    Preserves original raw data integrity while empowering downstream models 
    to filter, weight, or inspect anomalies separately.
    """
    df_res = df.copy()
    print(f"\n--- TASK 4: FLAG OUTLIERS WITH BINARY COLUMN ({column}) ---")
    
    is_iqr_outlier = (df_res[column] < lower_bound) | (df_res[column] > upper_bound)
    is_zscore_outlier = df_res[f'{column}_zscore'] > zscore_threshold
    
    df_res[f'is_outlier_{column}'] = (is_iqr_outlier | is_zscore_outlier).astype(int)
    
    normal_df = df_res[df_res[f'is_outlier_{column}'] == 0]
    anomaly_df = df_res[df_res[f'is_outlier_{column}'] == 1]
    
    print(f"Normal records: {len(normal_df)}")
    print(f"Anomaly/Outlier records: {len(anomaly_df)}")
    print(f"Anomaly ratio: {(len(anomaly_df) / len(df_res))*100:.2f}%")
    
    return df_res, normal_df, anomaly_df


# Task 5: Create Cleaning Log
def create_cleaning_audit_log(logs_list, output_path='output/cleaning_log.csv'):
    """
    Document all outlier transformations in a structured audit log CSV.
    """
    print("\n--- TASK 5: CREATE CLEANING AUDIT LOG ---")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    log_df = pd.DataFrame(logs_list)
    log_df.to_csv(output_path, index=False)
    
    print(f"Saved cleaning log to '{output_path}'. Log preview:")
    print(log_df.to_string())
    
    return log_df


def generate_outlier_plots(df_raw, df_clean, lower_bound, upper_bound):
    """Generate visual boxplots and histograms showing before vs after capping."""
    os.makedirs('output', exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # 1. Raw Revenue Distribution (skewed + outliers)
    sns.boxplot(x=df_raw['revenue'], ax=axes[0, 0], color='#d95f02')
    axes[0, 0].set_title('Raw Revenue Boxplot (With Outliers)')
    axes[0, 0].set_xlabel('Revenue ($)')
    
    # 2. Capped Revenue Distribution
    sns.boxplot(x=df_clean['revenue_capped'], ax=axes[0, 1], color='#1b9e77')
    axes[0, 1].set_title('Capped Revenue Boxplot (IQR Bounded)')
    axes[0, 1].set_xlabel('Capped Revenue ($)')
    
    # 3. Histogram Revenue Before vs After
    sns.histplot(df_raw['revenue'], ax=axes[1, 0], kde=True, color='#d95f02', bins=30)
    axes[1, 0].set_title('Raw Revenue Histogram')
    axes[1, 0].set_yscale('log')  # Log scale to visualize extreme values
    axes[1, 0].set_xlabel('Revenue ($)')
    
    # 4. Age Distribution & Outlier Capping
    sns.histplot(df_clean['revenue_capped'], ax=axes[1, 1], kde=True, color='#1b9e77', bins=30)
    axes[1, 1].set_title('Capped Revenue Histogram')
    axes[1, 1].set_xlabel('Capped Revenue ($)')
    
    plt.tight_layout()
    plt.savefig('output/outlier_distribution_plots.png')
    plt.close()
    
    print("\nSaved visualization plot to 'output/outlier_distribution_plots.png'.")


def run_pipeline():
    """Execute full outlier detection and handling pipeline."""
    print("=========================================================")
    print("      OUTLIER DETECTION & HANDLING PIPELINE DEMO         ")
    print("=========================================================")
    
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # 1. Create synthetic dataset
    raw_df = create_synthetic_customer_data()
    raw_df.to_csv('data/raw/customer_revenue.csv', index=False)
    print("\nLoaded raw customer revenue dataset ('data/raw/customer_revenue.csv'):")
    print(raw_df.head(10))
    
    # 2. Task 1: Z-Score Detection
    df_step1, z_outliers = detect_zscore_outliers(raw_df, column='revenue', threshold=3.0)
    
    # 3. Task 2: IQR Detection
    df_step2, lower_b, upper_b, iqr_outliers = detect_iqr_outliers(df_step1, column='revenue', multiplier=1.5)
    
    # 4. Task 3: Cap Outliers (Winsorization)
    df_step3 = cap_outliers(df_step2, column='revenue', lower_bound=lower_b, upper_bound=upper_b)
    
    # Also handle age column: invalid age (< 0 or > 120) capped/filtered
    age_lower, age_upper = 18.0, 100.0
    df_step3['age_capped'] = df_step3['age'].clip(lower=age_lower, upper=age_upper)
    
    # 5. Task 4: Flag Outliers with Binary Column
    df_step4, normal_df, anomaly_df = flag_combined_outliers(
        df_step3, 
        column='revenue', 
        zscore_threshold=3.0, 
        lower_bound=lower_b, 
        upper_bound=upper_b
    )
    
    # 6. Task 5: Document in Cleaning Log
    cleaning_log = [
        {
            'column': 'revenue',
            'method': 'Z-Score (|Z| > 3.0)',
            'action': 'flag',
            'threshold_lower': None,
            'threshold_upper': df_raw_mean_std(raw_df['revenue']),
            'affected_rows': len(z_outliers),
            'business_reasoning': 'Flagged extreme revenue spikes (> $45k) for separate high-value client audit.',
            'date': str(pd.Timestamp.now())
        },
        {
            'column': 'revenue',
            'method': 'IQR (1.5x Multiplier)',
            'action': 'cap',
            'threshold_lower': round(lower_b, 2),
            'threshold_upper': round(upper_b, 2),
            'affected_rows': len(iqr_outliers),
            'business_reasoning': 'Capped extreme revenue values at IQR bounds to prevent skewing linear regression models.',
            'date': str(pd.Timestamp.now())
        },
        {
            'column': 'age',
            'method': 'Domain Rule Boundary (18-100)',
            'action': 'cap',
            'threshold_lower': age_lower,
            'threshold_upper': age_upper,
            'affected_rows': ((raw_df['age'] < 18) | (raw_df['age'] > 100)).sum(),
            'business_reasoning': 'Capped negative and 150+ age data-entry errors to realistic adult customer age range.',
            'date': str(pd.Timestamp.now())
        }
    ]
    
    log_df = create_cleaning_audit_log(cleaning_log, 'output/cleaning_log.csv')
    
    # Generate visualization plots
    generate_outlier_plots(raw_df, df_step4, lower_b, upper_b)
    
    # Save processed clean dataset
    df_step4.to_csv('data/processed/clean_outlier_data.csv', index=False)
    print("\nSaved processed clean dataset to 'data/processed/clean_outlier_data.csv'.")
    print("Pipeline Execution Completed Successfully.")


def df_raw_mean_std(series):
    """Helper method to format threshold summary."""
    return f"{series.mean() + 3*series.std():.2f}"


if __name__ == '__main__':
    run_pipeline()
