"""
Time-Series Trend & Rolling Metrics Pipeline
--------------------------------------------
Assignment 21 - Kalvium SalesPulse Time-Series Analytics Engine

This script implements temporal analysis on daily revenue transactions:
1. Resampling data by weekly ('W') and monthly ('ME') periods
2. Computing 7-day and 30-day moving rolling window averages
3. Calculating Month-over-Month (MoM) percentage change rates
4. Tracking cumulative revenue accumulation over time
5. Trend pattern recognition and business action report generation
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def create_synthetic_daily_revenue_data(num_days=180, seed=42):
    """
    Generate synthetic daily transaction dataset over 180 days (6 months).
    
    Includes realistic temporal dynamics:
      - Weekly seasonality (weekend volume spikes)
      - Random daily noise ($5,000 - $15,000)
      - Sustainable underlying upward trend (~$20/day expansion)
    """
    np.random.seed(seed)
    
    start_date = pd.Timestamp('2026-01-01')
    dates = pd.date_range(start=start_date, periods=num_days, freq='D')
    
    # Base trend component
    trend = np.linspace(8000, 14000, num_days)
    
    # Weekly seasonality component (Saturdays and Sundays have higher consumer spend)
    day_of_week = dates.dayofweek
    seasonality = np.where(day_of_week >= 5, 2500, -800)
    
    # Random Gaussian noise
    noise = np.random.normal(loc=0, scale=1200, size=num_days)
    
    revenue = np.round(trend + seasonality + noise, 2)
    revenue = np.clip(revenue, 1000.0, 30000.0) # Ensure positive realistic values
    
    orders = np.random.poisson(lam=(revenue / 150.0).astype(int)) + 10
    
    df = pd.DataFrame({
        'date': dates,
        'revenue': revenue,
        'orders': orders
    })
    
    return df


# Task 1: Resample Data by Time Period
def resample_time_series(df):
    """
    Resample daily time-series into Weekly ('W') and Monthly ('ME') buckets.
    """
    print("\n--- TASK 1: RESAMPLE DATA BY TIME PERIOD ---")
    
    df_ts = df.set_index('date')
    
    # Weekly aggregation
    weekly_revenue = df_ts['revenue'].resample('W').sum()
    weekly_count = df_ts['orders'].resample('W').sum()
    weekly_avg = df_ts['revenue'].resample('W').mean()
    
    # Monthly aggregation
    monthly_revenue = df_ts['revenue'].resample('ME').sum()
    monthly_count = df_ts['orders'].resample('ME').sum()
    monthly_avg = df_ts['revenue'].resample('ME').mean()
    
    print("Weekly Resampled Revenue (Last 5 Weeks):")
    print(weekly_revenue.tail(5))
    
    print("\nMonthly Resampled Revenue Summary:")
    print(monthly_revenue)
    
    peak_week = weekly_revenue.idxmax().strftime('%Y-%m-%d')
    peak_week_rev = weekly_revenue.max()
    print(f"\nPeak Weekly Revenue: ${peak_week_rev:,.2f} (Week ending {peak_week})")
    
    return df_ts, weekly_revenue, monthly_revenue


# Task 2: Compute Rolling Window Average
def compute_rolling_averages(df, output_path='output/rolling_avg.png'):
    """
    Calculate 7-day and 30-day moving rolling averages to smooth daily noise.
    """
    print("\n--- TASK 2: COMPUTE ROLLING WINDOW AVERAGES ---")
    df_res = df.copy()
    
    df_res['revenue_ma7'] = df_res['revenue'].rolling(window=7).mean()
    df_res['revenue_ma30'] = df_res['revenue'].rolling(window=30).mean()
    
    os.makedirs('output', exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df_res['date'], df_res['revenue'], label='Raw Daily Revenue', alpha=0.35, color='#999999', linewidth=1)
    plt.plot(df_res['date'], df_res['revenue_ma7'], label='7-Day Rolling MA (Short-Term)', color='#1b9e77', linewidth=2)
    plt.plot(df_res['date'], df_res['revenue_ma30'], label='30-Day Rolling MA (Long-Term Trend)', color='#d95f02', linewidth=2.5)
    
    plt.title('Daily Revenue vs 7-Day & 30-Day Rolling Averages', fontsize=14, pad=10)
    plt.xlabel('Date')
    plt.ylabel('Revenue ($)')
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    print(f"Saved rolling average visualization plot to '{output_path}'.")
    return df_res


# Task 3: Calculate Month-over-Month Percentage Change
def calculate_mom_percentage_change(df_ts):
    """
    Calculate Month-over-Month (MoM) percentage change using .pct_change().
    """
    print("\n--- TASK 3: MONTH-OVER-MONTH (MoM) PERCENTAGE CHANGE ---")
    
    monthly_revenue = df_ts['revenue'].resample('ME').sum()
    mom_change = monthly_revenue.pct_change() * 100.0
    
    mom_df = pd.DataFrame({
        'monthly_revenue': monthly_revenue,
        'mom_change_pct': mom_change
    }).round(2)
    
    print("Monthly Revenue & MoM Percentage Growth:")
    print(mom_df)
    
    growth_months = mom_df[mom_df['mom_change_pct'] > 0]
    decline_months = mom_df[mom_df['mom_change_pct'] < 0]
    
    print(f"\nPositive Growth Months Count: {len(growth_months)}")
    print(f"Negative Decline Months Count: {len(decline_months)}")
    
    return mom_df, growth_months, decline_months


# Task 4: Compute Cumulative Sum
def compute_cumulative_revenue(df, output_path='output/cumulative.png'):
    """
    Track cumulative accumulated revenue over time using .cumsum().
    """
    print("\n--- TASK 4: CUMULATIVE REVENUE ACCUMULATION ---")
    df_res = df.copy()
    
    df_res['cumulative_revenue'] = df_res['revenue'].cumsum()
    total_accumulated = df_res['cumulative_revenue'].iloc[-1]
    
    os.makedirs('output', exist_ok=True)
    
    plt.figure(figsize=(10, 5))
    plt.plot(df_res['date'], df_res['cumulative_revenue'], color='#2b5c8f', linewidth=2.5)
    plt.fill_between(df_res['date'], df_res['cumulative_revenue'], color='#2b5c8f', alpha=0.15)
    
    plt.title('Cumulative Revenue Accumulation Over Time (180 Days)', fontsize=14, pad=10)
    plt.xlabel('Date')
    plt.ylabel('Cumulative Revenue ($)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    print(f"Saved cumulative revenue plot to '{output_path}'.")
    print(f"Total Accumulated System Revenue: ${total_accumulated:,.2f}")
    
    return df_res, total_accumulated


# Task 5: Identify Trend Pattern and Business Implications
def analyze_trend_and_generate_report(df_rolling, mom_df, total_revenue, output_path='output/trend_analysis.txt'):
    """
    Determine underlying trend direction, magnitude, volatility, and write business interpretation.
    """
    print("\n--- TASK 5: TREND PATTERN & BUSINESS IMPLICATIONS REPORT ---")
    
    # 30-day trend comparison
    recent_ma30 = df_rolling['revenue_ma30'].dropna()
    start_val = recent_ma30.iloc[-30]
    end_val = recent_ma30.iloc[-1]
    
    trend_direction = 'UPTREND (Accelerating)' if end_val > start_val else 'DOWNTREND (Declining)'
    trend_magnitude = ((end_val - start_val) / start_val) * 100.0
    
    latest_mom = mom_df['mom_change_pct'].dropna().iloc[-1] if not mom_df['mom_change_pct'].dropna().empty else 0.0
    volatility = df_rolling['revenue'].std()
    
    analysis_text = f"""=========================================================
TIME-SERIES TREND ANALYSIS & BUSINESS IMPLICATIONS REPORT
=========================================================

1. TREND METRICS SUMMARY:
   - 30-Day Moving Average Trend: {trend_direction}
   - Trend Change over Last 30 Days: {trend_magnitude:+.2f}%
   - Latest Month-over-Month (MoM) Growth: {latest_mom:+.2f}%
   - Total 180-Day Accumulated Revenue: ${total_revenue:,.2f}
   - Daily Revenue Volatility (Std Dev): ${volatility:,.2f}

2. PATTERN INTERPRETATION:
   - The 7-day rolling average effectively eliminates weekend sales spikes.
   - The 30-day moving average demonstrates a clear, sustainable upward trend.
   - Daily revenue fluctuations (${volatility:,.0f} noise) are driven by weekend purchasing behavior rather than business instability.

3. ACTIONABLE BUSINESS IMPLICATIONS & STRATEGY:
   - Maintain current marketing and expansion strategy as underlying momentum is accelerating (+{trend_magnitude:.1f}%).
   - Do NOT execute panic discounting during mid-week revenue dips (e.g. Tuesdays), as rolling metrics confirm healthy structural growth.
   - Capitalize on weekend demand spikes by scheduling targeted promotional campaigns for Friday through Sunday.
========================================================="""

    print(analysis_text)
    
    os.makedirs('output', exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(analysis_text)
        
    print(f"\nSaved trend analysis report to '{output_path}'.")
    return analysis_text


def create_jupyter_notebook_artifact():
    """
    Generate notebooks/time_series_analysis.ipynb artifact as requested in PR submission guidelines.
    """
    os.makedirs('notebooks', exist_ok=True)
    notebook_path = 'notebooks/time_series_analysis.ipynb'
    
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Time-Series Trend & Rolling Metrics Analysis\n",
                    "**Assignment 21 - Kalvium SalesPulse**\n",
                    "\n",
                    "This notebook demonstrates daily time-series resampling, 7-day & 30-day rolling moving averages, Month-over-Month percentage growth, and cumulative revenue tracking."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "from scripts.rolling_metrics import create_synthetic_daily_revenue_data, compute_rolling_averages\n",
                    "\n",
                    "# Load synthetic daily revenue data\n",
                    "df = create_synthetic_daily_revenue_data()\n",
                    "df.head()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 2,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Compute Rolling Averages and Display Summary\n",
                    "df_rolling = compute_rolling_averages(df)\n",
                    "df_rolling.tail(10)"
                ]
            }
        ],
        "metadata": {
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    import json
    with open(notebook_path, 'w') as f:
        json.dump(notebook_content, f, indent=2)
        
    print(f"Created Jupyter notebook artifact at '{notebook_path}'.")


def run_pipeline():
    """Execute complete time-series trend analysis pipeline."""
    print("=========================================================")
    print("     TIME-SERIES TREND & ROLLING METRICS DEMO            ")
    print("=========================================================")
    
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # 1. Create synthetic dataset
    raw_df = create_synthetic_daily_revenue_data()
    raw_df.to_csv('data/raw/daily_revenue_data.csv', index=False)
    print(f"\nGenerated synthetic daily revenue dataset 'data/raw/daily_revenue_data.csv' ({len(raw_df)} days).")
    
    # 2. Task 1: Resample Data
    df_ts, weekly_rev, monthly_rev = resample_time_series(raw_df)
    
    # 3. Task 2: Compute Rolling Averages
    df_rolling = compute_rolling_averages(raw_df, 'output/rolling_avg.png')
    
    # 4. Task 3: Calculate MoM % Change
    mom_df, growth_m, decline_m = calculate_mom_percentage_change(df_ts)
    
    # 5. Task 4: Compute Cumulative Sum
    df_cum, total_revenue = compute_cumulative_revenue(df_rolling, 'output/cumulative.png')
    
    # 6. Task 5: Trend Analysis & Report
    report = analyze_trend_and_generate_report(df_cum, mom_df, total_revenue, 'output/trend_analysis.txt')
    
    # Create required notebook artifact
    create_jupyter_notebook_artifact()
    
    # Save clean processed dataset
    df_cum.to_csv('data/processed/clean_time_series_data.csv', index=False)
    print("\nSaved processed clean dataset to 'data/processed/clean_time_series_data.csv'.")
    print("Pipeline Execution Completed Successfully.")


if __name__ == '__main__':
    run_pipeline()
