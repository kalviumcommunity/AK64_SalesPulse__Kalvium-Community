"""
Correlation & Relationship Analysis Pipeline
--------------------------------------------
Assignment 19 - Kalvium SalesPulse Relationship Analytics Pipeline

This script implements correlation discovery, relationship visualization, feature selection,
and causal reasoning for customer churn modeling.

Tasks Covered:
1. Pearson and Spearman Correlation Matrices & Comparison
2. Seaborn Correlation Heatmap Visualization
3. Identify Strongly Correlated Feature Pairs (|r| > 0.7)
4. Business Interpretation & Correlation vs Causation Analysis
5. Feature Selection via Multicollinearity Reduction
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def create_synthetic_churn_correlation_dataset(num_records=500, seed=42):
    """
    Generate synthetic customer churn dataset with known structural correlations:
      - engagement & transactions_per_month: Highly collinear (r ≈ 0.92)
      - support_tickets & churn: Strong positive correlation (r ≈ 0.78)
      - days_since_last_purchase & churn: Positive correlation (r ≈ 0.65)
      - total_spent & churn: Negative correlation (r ≈ -0.55)
    """
    np.random.seed(seed)
    
    transactions_per_month = np.random.uniform(0.5, 20.0, size=num_records)
    # Collinear feature: engagement is strongly proportional to transactions_per_month
    engagement = transactions_per_month * 4.5 + np.random.normal(loc=0, scale=3.0, size=num_records)
    
    # Customer friction / pain score (unobserved confounding variable)
    customer_pain = np.random.exponential(scale=2.0, size=num_records)
    
    support_tickets = np.round(customer_pain * 2.5 + np.random.poisson(lam=1, size=num_records)).astype(int)
    days_since_last_purchase = np.round(customer_pain * 8.0 + np.random.uniform(1, 15, size=num_records)).astype(int)
    total_spent = np.round(np.random.uniform(100, 5000, size=num_records) - customer_pain * 400, 2)
    total_spent = np.clip(total_spent, 20.0, 10000.0)
    
    # Churn probability driven by customer pain and inactivity
    churn_prob = 1 / (1 + np.exp(-(customer_pain - 2.0)))
    churn = (np.random.rand(num_records) < churn_prob).astype(int)
    
    df = pd.DataFrame({
        'customer_id': [f"CUST_{3000 + i}" for i in range(num_records)],
        'transactions_per_month': np.round(transactions_per_month, 2),
        'engagement': np.round(engagement, 2),
        'support_tickets': support_tickets,
        'days_since_last_purchase': days_since_last_purchase,
        'total_spent': total_spent,
        'churn': churn
    })
    
    return df


# Task 1: Compute Pearson and Spearman Correlation
def compute_pearson_spearman_correlations(df):
    """
    Calculate Pearson (linear) and Spearman (rank-monotonic) correlation matrices.
    """
    print("\n--- TASK 1: COMPUTE PEARSON & SPEARMAN CORRELATION ---")
    
    numeric_df = df.select_dtypes(include=[np.number])
    
    pearson_corr = numeric_df.corr(method='pearson')
    spearman_corr = numeric_df.corr(method='spearman')
    
    comparison = pd.DataFrame({
        'pearson_churn': pearson_corr['churn'],
        'spearman_churn': spearman_corr['churn'],
        'abs_difference': (pearson_corr['churn'] - spearman_corr['churn']).abs()
    }).round(3)
    
    print("Comparison of Feature Correlations with Target ('churn'):")
    print(comparison)
    
    return pearson_corr, spearman_corr, comparison


# Task 2: Visualize Correlation Heatmap
def visualize_correlation_heatmap(pearson_corr, output_path='output/correlation_heatmap.png'):
    """
    Generate and save a Seaborn correlation matrix heatmap.
    """
    print("\n--- TASK 2: VISUALIZE CORRELATION HEATMAP ---")
    os.makedirs('output', exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        pearson_corr, 
        annot=True, 
        fmt='.2f', 
        cmap='coolwarm', 
        center=0, 
        linewidths=0.5, 
        ax=ax
    )
    ax.set_title('Customer Churn Feature Correlation Matrix (Pearson)', fontsize=14, pad=12)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    print(f"Saved correlation heatmap visualization to '{output_path}'.")


# Task 3: Identify Strongly Correlated Pairs
def identify_strongly_correlated_pairs(pearson_corr, threshold=0.7):
    """
    Locate pairs of features with absolute correlation coefficient |r| > threshold.
    """
    print(f"\n--- TASK 3: IDENTIFY STRONGLY CORRELATED PAIRS (|r| > {threshold}) ---")
    
    corr_flat = pearson_corr.unstack()
    
    # Exclude self-correlations (r = 1.0) and duplicates
    strong_corrs = corr_flat[corr_flat.abs() > threshold].sort_values(ascending=False)
    strong_pairs = strong_corrs[strong_corrs != 1.0]
    
    # Remove duplicate reverse pairs (A-B and B-A)
    unique_pairs = {}
    for (var1, var2), val in strong_pairs.items():
        pair_key = tuple(sorted([var1, var2]))
        if pair_key not in unique_pairs:
            unique_pairs[pair_key] = val
            
    print(f"Discovered {len(unique_pairs)} Strongly Correlated Feature Pair(s):")
    for (v1, v2), val in unique_pairs.items():
        print(f"  - {v1} <--> {v2}: r = {val:+.3f}")
        
    return unique_pairs


# Task 4: Business Interpretation & Causation Walkthrough
def perform_causal_business_analysis(pearson_corr):
    """
    Synthesize business interpretation and address Correlation vs Causation paradoxes.
    """
    print("\n--- TASK 4: BUSINESS INTERPRETATION & CAUSATION ANALYSIS ---")
    
    r_tickets_churn = float(pearson_corr.loc['support_tickets', 'churn'])
    
    analysis = {
        'support_tickets <-> churn': {
            'correlation_r': round(r_tickets_churn, 3),
            'possible_causal_directions': [
                'Direction 1 (Direct Causal): support_tickets -> churn (Customers get frustrated by support process and leave)',
                'Direction 2 (Reverse Causal): churn -> support_tickets (Customers about to leave open tickets to request refunds)',
                'Direction 3 (Confounding Variable): customer_pain -> BOTH (Product defects cause both high tickets AND churn)'
            ],
            'data_driven_insight': (
                "Likely Direction 3: Underlying customer friction/product bugs act as a confounding variable. "
                "Support tickets are a SYMPTOM of friction, not the root cause of churn."
            ),
            'actionable_business_decision': (
                "Do NOT attempt to reduce churn by limiting support ticket access. "
                "Instead, resolve root-cause product friction and train support teams to proactively resolve ticket issues."
            )
        }
    }
    
    json_output = json.dumps(analysis, indent=2)
    print(json_output)
    
    os.makedirs('output', exist_ok=True)
    with open('output/causal_relationship_analysis.json', 'w') as f:
        f.write(json_output)
        
    print("\nSaved causal relationship analysis to 'output/causal_relationship_analysis.json'.")
    return analysis


# Task 5: Feature Selection Based on Correlation
def execute_correlation_feature_selection(df, pearson_corr):
    """
    Drop redundant collinear features (|r| > 0.70) to prevent model multicollinearity.
    """
    print("\n--- TASK 5: FEATURE SELECTION BASED ON CORRELATION ---")
    
    # Full candidate feature matrix
    df_features = df[['engagement', 'transactions_per_month', 'support_tickets', 'days_since_last_purchase', 'total_spent', 'churn']]
    print(f"Original Feature Matrix Shape: {df_features.shape}")
    
    r_collinear = pearson_corr.loc['transactions_per_month', 'engagement']
    print(f"Collinearity Check: 'transactions_per_month' <-> 'engagement' r = {r_collinear:.3f}")
    
    # Drop 'engagement' because 'transactions_per_month' is more interpretable and directly normalized
    df_selected = df_features.drop(columns=['engagement'])
    print("Action Taken: Dropped redundant column 'engagement' to eliminate multicollinearity.")
    
    print(f"Selected Feature Matrix Shape: {df_selected.shape}")
    print("\nSelected Features Correlation Matrix with Target:")
    print(df_selected.corr()['churn'].round(3))
    
    os.makedirs('data/processed', exist_ok=True)
    df_selected.to_csv('data/processed/selected_features_churn.csv', index=False)
    print("\nSaved selected features dataset to 'data/processed/selected_features_churn.csv'.")
    
    return df_selected


def run_pipeline():
    """Execute full correlation and relationship analysis pipeline."""
    print("=========================================================")
    print("     CORRELATION & RELATIONSHIP ANALYSIS DEMO            ")
    print("=========================================================")
    
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # 1. Create synthetic dataset
    raw_df = create_synthetic_churn_correlation_dataset()
    raw_df.to_csv('data/raw/customer_churn_correlation.csv', index=False)
    print(f"\nGenerated synthetic churn dataset 'data/raw/customer_churn_correlation.csv' ({len(raw_df)} records).")
    
    # 2. Task 1: Pearson & Spearman
    pearson_corr, spearman_corr, comparison = compute_pearson_spearman_correlations(raw_df)
    
    # 3. Task 2: Visualize Heatmap
    visualize_correlation_heatmap(pearson_corr)
    
    # 4. Task 3: Identify Strong Pairs
    strong_pairs = identify_strongly_correlated_pairs(pearson_corr, threshold=0.7)
    
    # 5. Task 4: Causal Business Interpretation
    causal_analysis = perform_causal_business_analysis(pearson_corr)
    
    # 6. Task 5: Feature Selection
    df_selected = execute_correlation_feature_selection(raw_df, pearson_corr)
    
    print("\nPipeline Execution Completed Successfully.")


if __name__ == '__main__':
    run_pipeline()
