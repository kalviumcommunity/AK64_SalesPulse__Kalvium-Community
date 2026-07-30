"""
Distribution Analysis for Business Trends
-----------------------------------------
Assignment 18 - Kalvium SalesPulse Distribution Analytics Pipeline

This script implements statistical distribution analysis on customer revenue data:
1. Histogram & Kernel Density Estimation (KDE) Plots
2. Skewness and Kurtosis Calculations
3. Bimodal & Percentile Gap Abnormal Pattern Discovery
4. Comparative Segment Distribution Analysis & Kolmogorov-Smirnov Testing
5. Business Decision Synthesis Report
"""

import os
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns


def create_synthetic_distribution_dataset(num_records=1000, seed=42):
    """
    Generate synthetic dataset containing bimodal, right-skewed revenue distribution.
    
    Structure:
      - 80% Small/SMB Customers: Lognormal distribution ($50 - $1,500)
      - 20% Enterprise Customers: Normal distribution centered around high tier ($45,000 - $80,000)
    """
    np.random.seed(seed)
    
    n_smb = int(num_records * 0.80)
    n_ent = num_records - n_smb
    
    smb_revenue = np.random.lognormal(mean=5.5, sigma=0.8, size=n_smb)
    ent_revenue = np.random.normal(loc=55000, scale=12000, size=n_ent)
    
    revenue = np.concatenate([smb_revenue, ent_revenue])
    revenue = np.clip(revenue, 10.0, 150000.0)
    revenue = np.round(revenue, 2)
    
    np.random.shuffle(revenue)
    
    df = pd.DataFrame({
        'customer_id': [f"CUST_{1000 + i}" for i in range(num_records)],
        'revenue': revenue,
        'customer_type': np.where(revenue > 20000, 'Enterprise', 'SMB')
    })
    
    return df


# Task 1: Distribution Plots (Histogram & KDE)
def plot_revenue_distributions(df, output_path='output/revenue_distribution.png'):
    """
    Generate and save side-by-side Histogram and KDE density plots.
    """
    print("\n--- TASK 1: DISTRIBUTION PLOTS (HISTOGRAM & KDE) ---")
    os.makedirs('output', exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram
    axes[0].hist(df['revenue'], bins=50, color='#2b5c8f', edgecolor='black', alpha=0.8)
    axes[0].set_title('Revenue Distribution (Histogram)')
    axes[0].set_xlabel('Revenue ($)')
    axes[0].set_ylabel('Customer Count')
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)

    # KDE Plot
    df['revenue'].plot(kind='density', ax=axes[1], color='#e7298a', linewidth=2)
    axes[1].set_title('Revenue Distribution (KDE Density Curve)')
    axes[1].set_xlabel('Revenue ($)')
    axes[1].set_ylabel('Probability Density')
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    print(f"Saved distribution plots to '{output_path}'.")


# Task 2: Compute Skewness and Kurtosis
def compute_skewness_and_kurtosis(df, column='revenue'):
    """
    Calculate Fisher-Pearson coefficient of skewness and Kurtosis.
    """
    print(f"\n--- TASK 2: COMPUTE SKEWNESS & KURTOSIS ({column}) ---")
    
    skewness = float(stats.skew(df[column]))
    kurt = float(stats.kurtosis(df[column]))
    
    mean_val = df[column].mean()
    median_val = df[column].median()

    print(f"Mean Revenue:   ${mean_val:.2f}")
    print(f"Median Revenue: ${median_val:.2f}")
    print(f"Skewness:       {skewness:.2f}")
    print(f"Kurtosis:       {kurt:.2f}")

    if abs(skewness) > 1:
        print("  -> Skewness Interpretation: Highly skewed distribution (|Skew| > 1). Use MEDIAN instead of MEAN.")
    else:
        print("  -> Skewness Interpretation: Fairly symmetric distribution.")
        
    if kurt > 3:
        print("  -> Kurtosis Interpretation: Heavy-tailed distribution (Kurtosis > 3). High outlier probability.")
    else:
        print("  -> Kurtosis Interpretation: Light-tailed distribution.")
        
    return skewness, kurt


# Task 3: Identify Abnormal Patterns (Bimodality & Percentiles)
def identify_abnormal_patterns(df, column='revenue'):
    """
    Inspect detailed summary statistics and percentiles to uncover bimodal gaps.
    """
    print(f"\n--- TASK 3: IDENTIFY ABNORMAL PATTERNS ({column}) ---")
    
    print("Descriptive Statistics:")
    print(df[column].describe().round(2))

    percentile_levels = [0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
    percentiles = df[column].quantile(percentile_levels)
    
    print("\nDetailed Percentile Breakdown:")
    for p, val in percentiles.items():
        print(f"  {int(p*100):>2}th Percentile: ${val:10.2f}")
        
    gap_75_90 = percentiles[0.90] - percentiles[0.75]
    print(f"\nPercentile Gap (90th - 75th percentile): ${gap_75_90:,.2f}")
    if gap_75_90 > 10000:
        print("  -> Abnormal Pattern Detected: Massive gap between 75th and 90th percentiles indicates a BIMODAL customer distribution (SMB vs Enterprise).")
        
    return percentiles


# Task 4: Compare Segment Distributions & Statistical Testing
def compare_segment_distributions(df, column='revenue'):
    """
    Split customers into High-Value (Q4) vs Low-Value (Q1) and perform Kolmogorov-Smirnov test.
    """
    print("\n--- TASK 4: COMPARE SEGMENT DISTRIBUTIONS & STATISTICAL TESTING ---")
    
    q75 = df[column].quantile(0.75)
    q25 = df[column].quantile(0.25)
    
    high_value = df[df[column] >= q75]
    low_value = df[df[column] <= q25]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Segment Histogram
    axes[0].hist(high_value[column], bins=30, alpha=0.7, color='#1b9e77', label='High-Value (Top 25%)')
    axes[0].hist(low_value[column], bins=30, alpha=0.7, color='#d95f02', label='Low-Value (Bottom 25%)')
    axes[0].legend()
    axes[0].set_title('Revenue Comparison: High vs Low Value')
    axes[0].set_xlabel('Revenue ($)')
    axes[0].set_ylabel('Customer Count')
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)

    # Segment Boxplot
    sns.boxplot(data=df, x='customer_type', y=column, ax=axes[1], hue='customer_type', palette='Set2', legend=False)
    axes[1].set_title('Revenue Boxplot by Customer Segment')
    axes[1].set_xlabel('Customer Segment')
    axes[1].set_ylabel('Revenue ($)')

    plt.tight_layout()
    plt.savefig('output/segment_distribution_comparison.png')
    plt.close()

    high_mean, high_median = high_value[column].mean(), high_value[column].median()
    low_mean, low_median = low_value[column].mean(), low_value[column].median()

    print(f"High-Value Segment (Top 25%):   Mean = ${high_mean:,.2f}, Median = ${high_median:,.2f}")
    print(f"Low-Value Segment (Bottom 25%): Mean = ${low_mean:,.2f}, Median = ${low_median:,.2f}")

    # Two-sample Kolmogorov-Smirnov Test for distribution equality
    ks_stat, p_value = stats.ks_2samp(high_value[column], low_value[column])
    print(f"\nTwo-Sample Kolmogorov-Smirnov Test:")
    print(f"  - KS Statistic: {ks_stat:.4f}")
    print(f"  - p-value:      {p_value:.4e}")
    if p_value < 0.05:
        print("  -> Statistically Significant Difference: The two customer segments come from entirely different underlying distributions (p < 0.05).")

    return high_value, low_value


# Task 5: Business Interpretation
def generate_business_interpretation(df, skewness, kurtosis, percentiles):
    """
    Synthesize statistical results into actionable business decisions and save report.
    """
    print("\n--- TASK 5: BUSINESS INTERPRETATION & ACTION REPORT ---")
    
    mean_val = df['revenue'].mean()
    median_val = df['revenue'].median()
    max_val = df['revenue'].max()
    p99_val = percentiles[0.99]

    interpretation = f"""=========================================================
REVENUE DISTRIBUTION ANALYSIS & BUSINESS ACTION REPORT
=========================================================

1. STATISTICAL SUMMARY:
   - Total Customers Evaluated: {len(df):,}
   - Skewness Metric: {skewness:.2f} ({"Highly Right-Skewed" if skewness > 1 else "Symmetric"})
   - Kurtosis Metric: {kurtosis:.2f} ({"Fat Tails / Heavy Outliers" if kurtosis > 3 else "Normal Tails"})
   - Mean Revenue:   ${mean_val:,.2f}
   - Median Revenue: ${median_val:,.2f}
   - Max Revenue:    ${max_val:,.2f}
   - Top 1% (99th Pct): ${p99_val:,.2f}

2. DISTRIBUTION INTERPRETATION:
   - The mean (${mean_val:,.2f}) is over {mean_val/median_val:.1f}x higher than the median (${median_val:,.2f}).
   - Reporting the average revenue gives a false impression of typical customer spend.
   - The dataset exhibits a BIMODAL right-skewed distribution: a high-volume SMB tier and a high-value Enterprise tier.

3. RECOMMENDED BUSINESS ACTIONS:
   - Product & Pricing: Establish separate pricing tiers for SMB self-serve vs. Enterprise contract sales.
   - Sales Strategy: Assign dedicated Account Executives to high-value Enterprise leads (> $40,000 spend).
   - Analytical Forecasting: Use Median-based metrics and log-transformed modeling instead of linear mean-based forecasts.
========================================================="""

    print(interpretation)
    
    os.makedirs('output', exist_ok=True)
    with open('output/distribution_business_report.txt', 'w') as f:
        f.write(interpretation)
        
    print("\nSaved text report to 'output/distribution_business_report.txt'.")
    return interpretation


def run_pipeline():
    """Execute complete distribution analysis pipeline."""
    print("=========================================================")
    print("     DISTRIBUTION ANALYSIS FOR BUSINESS TRENDS DEMO      ")
    print("=========================================================")
    
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # 1. Create synthetic dataset
    raw_df = create_synthetic_distribution_dataset()
    raw_df.to_csv('data/raw/revenue_distribution_data.csv', index=False)
    print(f"\nGenerated synthetic dataset 'data/raw/revenue_distribution_data.csv' ({len(raw_df)} records).")
    
    # 2. Task 1: Distribution Plots
    plot_revenue_distributions(raw_df)
    
    # 3. Task 2: Compute Skewness & Kurtosis
    skewness, kurtosis = compute_skewness_and_kurtosis(raw_df)
    
    # 4. Task 3: Identify Abnormal Patterns
    percentiles = identify_abnormal_patterns(raw_df)
    
    # 5. Task 4: Compare Segment Distributions
    high_val, low_val = compare_segment_distributions(raw_df)
    
    # 6. Task 5: Business Interpretation
    report_text = generate_business_interpretation(raw_df, skewness, kurtosis, percentiles)
    
    # Save processed clean data
    raw_df.to_csv('data/processed/clean_distribution_data.csv', index=False)
    print("\nSaved processed clean dataset to 'data/processed/clean_distribution_data.csv'.")
    print("Pipeline Execution Completed Successfully.")


if __name__ == '__main__':
    run_pipeline()
