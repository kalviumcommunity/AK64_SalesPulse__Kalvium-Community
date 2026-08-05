"""
GroupBy Aggregation & Segment Insights Pipeline
------------------------------------------------
Assignment 20 - Kalvium SalesPulse Segment Analytics Engine

This script implements single-level and multi-dimensional GroupBy aggregations,
pivot tables, segment ranking, percentage share calculations, and actionable business insights.

Tasks Covered:
1. Single-Level GroupBy with Multiple Aggregations
2. Multi-Level GroupBy (customer_type x product)
3. Two-Dimensional Pivot Table Creation
4. Rank and Identify Top/Bottom Performing Segments
5. Surface Actionable Business Segment Insights & Audit Export
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def create_synthetic_segment_dataset(num_records=1000, seed=42):
    """
    Generate synthetic customer dataset representing 3 realistic segments:
      - Enterprise (5% of base, ~1% churn, ~70% total revenue)
      - SMB (40% of base, ~12% churn, ~15% total revenue)
      - Startups (55% of base, ~8% churn, ~15% total revenue)
    """
    np.random.seed(seed)
    
    n_ent = int(num_records * 0.05)   # 50 customers
    n_smb = int(num_records * 0.40)   # 400 customers
    n_startup = num_records - n_ent - n_smb # 550 customers
    
    # Customer IDs & Segments
    types = ['Enterprise'] * n_ent + ['SMB'] * n_smb + ['Startups'] * n_startup
    
    # Revenue distributions
    rev_ent = np.random.uniform(120000, 180000, size=n_ent)      # ~$7.5M total
    rev_smb = np.random.uniform(2000, 6000, size=n_smb)           # ~$1.6M total
    rev_startup = np.random.uniform(1500, 4000, size=n_startup)    # ~$1.5M total
    revenue = np.concatenate([rev_ent, rev_smb, rev_startup])
    
    # Churn probabilities matching business scenario
    churn_ent = (np.random.rand(n_ent) < 0.01).astype(int)
    churn_smb = (np.random.rand(n_smb) < 0.12).astype(int)
    churn_startup = (np.random.rand(n_startup) < 0.08).astype(int)
    churn = np.concatenate([churn_ent, churn_smb, churn_startup])
    
    # Support tickets
    tickets_ent = np.random.poisson(lam=1.5, size=n_ent)
    tickets_smb = np.random.poisson(lam=4.2, size=n_smb)
    tickets_startup = np.random.poisson(lam=3.0, size=n_startup)
    tickets = np.concatenate([tickets_ent, tickets_smb, tickets_startup])
    
    # Product distribution
    products_ent = np.random.choice(['Enterprise Suite', 'Business Pro'], size=n_ent, p=[0.9, 0.1])
    products_smb = np.random.choice(['Enterprise Suite', 'Business Pro', 'Starter Kit'], size=n_smb, p=[0.1, 0.6, 0.3])
    products_startup = np.random.choice(['Business Pro', 'Starter Kit'], size=n_startup, p=[0.3, 0.7])
    products = np.concatenate([products_ent, products_smb, products_startup])
    
    df = pd.DataFrame({
        'customer_id': [f"CUST_{4000 + i}" for i in range(num_records)],
        'customer_type': types,
        'product': products,
        'revenue': np.round(revenue, 2),
        'churn': churn,
        'support_tickets': tickets
    })
    
    # Shuffle records for realism
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    return df


# Task 1: Single-Level GroupBy with Multiple Aggregations
def run_single_level_groupby(df):
    """
    Group by customer_type and compute summary aggregations.
    """
    print("\n--- TASK 1: SINGLE-LEVEL GROUPBY WITH MULTIPLE AGGREGATIONS ---")
    
    segment_metrics = df.groupby('customer_type').agg({
        'churn': 'mean',
        'revenue': 'sum',
        'customer_id': 'count',
        'support_tickets': 'mean'
    })
    
    segment_metrics.columns = ['churn_rate', 'total_revenue', 'customer_count', 'avg_support_tickets']
    
    print("Segment-Level Key Performance Indicators:")
    print(segment_metrics.round({'churn_rate': 4, 'total_revenue': 2, 'avg_support_tickets': 2}))
    
    return segment_metrics


# Task 2: Multi-Level GroupBy
def run_multi_level_groupby(df):
    """
    Group by customer_type AND product simultaneously and unstack for cleaner viewing.
    """
    print("\n--- TASK 2: MULTI-LEVEL GROUPBY (CUSTOMER TYPE x PRODUCT) ---")
    
    product_segment = df.groupby(['customer_type', 'product']).agg({
        'revenue': 'sum',
        'customer_id': 'count'
    })
    product_segment.columns = ['total_revenue', 'customer_count']
    
    # Unstack for pivot-like MultiIndex presentation
    product_segment_pivot = product_segment.unstack()
    
    print("Multi-Level Aggregation Unstacked Matrix:")
    print(product_segment_pivot)
    
    return product_segment, product_segment_pivot


# Task 3: Pivot Table
def generate_two_dimensional_pivot_table(df):
    """
    Create a clean 2D pivot table showing revenue breakdown by customer_type and product.
    """
    print("\n--- TASK 3: TWO-DIMENSIONAL PIVOT TABLE ---")
    
    pivot = pd.pivot_table(
        df,
        values='revenue',
        index='customer_type',
        columns='product',
        aggfunc='sum',
        fill_value=0
    )
    
    print("Pivot Table Revenue Matrix ($):")
    print(pivot.round(2))
    
    return pivot


# Task 4: Rank and Identify Top/Bottom Performers
def rank_and_analyze_performers(segment_metrics):
    """
    Compute churn rank and calculate percentage revenue contribution per segment.
    """
    print("\n--- TASK 4: RANK & IDENTIFY TOP/BOTTOM PERFORMERS ---")
    
    df_metrics = segment_metrics.copy()
    
    # Churn ranking (1 = lowest churn / best performance)
    df_metrics['churn_rank'] = df_metrics['churn_rate'].rank(ascending=True)
    
    # Revenue percentage share calculation
    total_sys_revenue = df_metrics['total_revenue'].sum()
    df_metrics['revenue_contribution'] = (df_metrics['total_revenue'] / total_sys_revenue) * 100
    df_metrics['customer_share'] = (df_metrics['customer_count'] / df_metrics['customer_count'].sum()) * 100
    
    worst_first = df_metrics.sort_values(by='churn_rate', ascending=False)
    
    print("Segments Sorted by Churn Rate (Highest Risk First):")
    print(worst_first[['churn_rate', 'churn_rank', 'revenue_contribution', 'customer_share']].round(2))
    
    return df_metrics


# Task 5: Surface Actionable Segment Insights & Audit Export
def surface_actionable_insights(df_metrics):
    """
    Generate structured, actionable business recommendations for each customer segment.
    """
    print("\n--- TASK 5: SURFACE ACTIONABLE SEGMENT INSIGHTS ---")
    
    insights = []
    for segment in df_metrics.index:
        row = df_metrics.loc[segment]
        
        churn_pct = row['churn_rate']
        rev_share = row['revenue_contribution']
        cust_cnt = int(row['customer_count'])
        tot_rev = row['total_revenue']
        
        insight = {
            'segment': segment,
            'customer_count': cust_cnt,
            'churn_rate': f"{churn_pct:.1%}",
            'total_revenue': f"${tot_rev:,.0f}",
            'revenue_contribution': f"{rev_share:.1f}%",
            'action': ''
        }
        
        # Evidence-based decision rules
        if churn_pct > 0.10:
            insight['action'] = 'HIGH PRIORITY: Churn above 10%. Investigate onboarding friction and product pain points.'
        elif churn_pct < 0.02:
            insight['action'] = 'HEALTHY & CRITICAL: Low churn (1%) generating majority revenue (70%+). Maintain dedicated VIP service.'
        else:
            insight['action'] = 'MODERATE RISK: Monitor startup engagement. Implement automated product adoption workflows.'
            
        insights.append(insight)

    insights_df = pd.DataFrame(insights)
    
    print("Actionable Segment Insights Summary Table:")
    print(insights_df.to_string(index=False))
    
    os.makedirs('output', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    insights_df.to_csv('output/segment_insights.csv', index=False)
    df_metrics.to_csv('data/processed/segmented_customer_summary.csv')
    
    print("\nSaved insights summary to 'output/segment_insights.csv'.")
    print("Saved processed segment summary to 'data/processed/segmented_customer_summary.csv'.")
    
    return insights_df


def generate_segment_visualizations(df_metrics, pivot):
    """Save segment analysis visualizations into output directory."""
    os.makedirs('output', exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 1. Revenue Share vs Churn Rate Bar Comparison
    color_churn = '#d95f02'
    color_rev = '#1b9e77'
    
    x = np.arange(len(df_metrics.index))
    width = 0.35
    
    axes[0].bar(x - width/2, df_metrics['revenue_contribution'], width, label='Revenue Share (%)', color=color_rev)
    axes[0].bar(x + width/2, df_metrics['churn_rate'] * 100, width, label='Churn Rate (%)', color=color_churn)
    
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(df_metrics.index)
    axes[0].set_title('Segment Paradox: Revenue Contribution vs Churn Rate')
    axes[0].set_ylabel('Percentage (%)')
    axes[0].legend()
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)
    
    # 2. Product x Segment Heatmap
    sns.heatmap(pivot / 1000, annot=True, fmt='.1f', cmap='YlGnBu', ax=axes[1], cbar_kws={'label': 'Revenue ($K)'})
    axes[1].set_title('Product Revenue Matrix by Segment ($ In Thousands)')
    axes[1].set_xlabel('Product Line')
    axes[1].set_ylabel('Customer Segment')
    
    plt.tight_layout()
    plt.savefig('output/segment_revenue_churn_analysis.png')
    plt.close()
    
    print("Saved visual charts to 'output/segment_revenue_churn_analysis.png'.")


def run_pipeline():
    """Execute complete segment aggregation & insights pipeline."""
    print("=========================================================")
    print("    GROUPBY AGGREGATION & SEGMENT INSIGHTS DEMO          ")
    print("=========================================================")
    
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # 1. Generate synthetic dataset
    raw_df = create_synthetic_segment_dataset(num_records=1000)
    raw_df.to_csv('data/raw/customer_segment_data.csv', index=False)
    print(f"\nGenerated synthetic segment dataset 'data/raw/customer_segment_data.csv' ({len(raw_df)} records).")
    
    # 2. Task 1: Single-Level GroupBy
    segment_metrics = run_single_level_groupby(raw_df)
    
    # 3. Task 2: Multi-Level GroupBy
    product_segment, product_segment_pivot = run_multi_level_groupby(raw_df)
    
    # 4. Task 3: Pivot Table
    pivot = generate_two_dimensional_pivot_table(raw_df)
    
    # 5. Task 4: Rank & Analyze
    ranked_metrics = rank_and_analyze_performers(segment_metrics)
    
    # 6. Task 5: Surface Insights & Save Reports
    insights_df = surface_actionable_insights(ranked_metrics)
    
    # Visualizations
    generate_segment_visualizations(ranked_metrics, pivot)
    
    print("\n=========================================================")
    print("  CONGRATULATIONS! ALL 20 DATA PIPELINE LESSONS COMPLETE!")
    print("=========================================================")


if __name__ == '__main__':
    run_pipeline()
 