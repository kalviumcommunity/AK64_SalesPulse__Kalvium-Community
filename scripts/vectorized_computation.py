"""
NumPy Vectorised Computation Workflow
-------------------------------------
Assignment 17 - Kalvium SalesPulse Performance Optimization Pipeline

This script demonstrates replacing slow Python loop-based calculations with fast
vectorized NumPy array operations on 100,000+ customer records.

Tasks Covered:
1. Replace Loop with NumPy Min-Max Normalization
2. Vectorized Z-Score Normalization
3. Bulk Ranking & Scoring using np.argsort
4. Precise Time Performance Benchmarking (Loop vs NumPy Speedup)
5. Seamless Integration of NumPy Results back to Pandas DataFrames
"""

import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def create_large_synthetic_dataset(num_records=100000, seed=42):
    """
    Generate synthetic dataset containing 100,000+ revenue records for performance testing.
    """
    np.random.seed(seed)
    
    customer_ids = [f"CUST_{i:06d}" for i in range(1, num_records + 1)]
    revenue = np.round(np.random.lognormal(mean=5.0, sigma=1.0, size=num_records), 2)
    quantity = np.random.randint(1, 50, size=num_records)
    
    df = pd.DataFrame({
        'customer_id': customer_ids,
        'revenue': revenue,
        'quantity': quantity
    })
    
    return df


# Task 1: Replace Loop with NumPy Vectorization (Min-Max Normalization)
def demonstrate_min_max_normalization(df):
    """
    Compare Min-Max Normalization: Python Loop vs NumPy Vectorization.
    
    Formula:
        X_norm = (X - X_min) / (X_max - X_min)
        Result bounds: [0, 1]
    """
    print("\n--- TASK 1: MIN-MAX NORMALIZATION (LOOP VS NUMPY) ---")
    
    # 1. Slow Python Loop
    start_loop = time.perf_counter()
    min_val = df['revenue'].min()
    max_val = df['revenue'].max()
    denom = max_val - min_val
    
    normalized_loop = []
    for val in df['revenue']:
        normalized_loop.append((val - min_val) / denom)
    loop_dur = time.perf_counter() - start_loop
    
    # 2. Fast NumPy Vectorized
    start_np = time.perf_counter()
    revenue_array = df['revenue'].values
    normalized_np = (revenue_array - revenue_array.min()) / (revenue_array.max() - revenue_array.min())
    np_dur = time.perf_counter() - start_np
    
    # Assign to DataFrame
    df_res = df.copy()
    df_res['revenue_normalized'] = normalized_np
    
    print(f"Min-Max Normalization on {len(df):,} rows:")
    print(f"  - Python Loop Time:  {loop_dur:.4f} seconds")
    print(f"  - NumPy Vector Time: {np_dur:.4f} seconds")
    print(f"  - Performance Speedup: {loop_dur / np_dur:.0f}x faster!")
    print(f"Normalized Min: {df_res['revenue_normalized'].min():.4f}, Max: {df_res['revenue_normalized'].max():.4f}")
    
    return df_res, normalized_np, loop_dur, np_dur


# Task 2: Z-Score Normalization
def demonstrate_zscore_normalization(df):
    """
    Perform Z-Score normalization directly using NumPy array arithmetic.
    
    Formula:
        Z = (X - mean) / std
    """
    print("\n--- TASK 2: VECTORIZED Z-SCORE NORMALIZATION ---")
    df_res = df.copy()
    
    start_time = time.time()
    revenue_array = df_res['revenue'].values
    z_scores = (revenue_array - revenue_array.mean()) / revenue_array.std()
    dur = time.time() - start_time
    
    df_res['revenue_zscore'] = z_scores
    
    print(f"Vectorized Z-Score calculation completed in {dur:.5f} seconds.")
    print(f"Z-Score Mean: {z_scores.mean():.6f} (approx 0), Std: {z_scores.std():.6f} (approx 1)")
    print(df_res[['customer_id', 'revenue', 'revenue_zscore']].head())
    
    return df_res, z_scores


# Task 3: Bulk Ranking & Scoring
def demonstrate_bulk_ranking(df):
    """
    Compute customer revenue rankings in descending order using np.argsort.
    """
    print("\n--- TASK 3: BULK RANKING & SCORING WITH NUMPY ---")
    df_res = df.copy()
    
    start_time = time.time()
    revenue_array = df_res['revenue'].values
    
    # np.argsort(-array) gives indices that would sort the array in descending order
    rankings = np.argsort(-revenue_array)
    rank_positions = np.empty_like(rankings)
    rank_positions[rankings] = np.arange(1, len(rankings) + 1)
    dur = time.time() - start_time
    
    df_res['revenue_rank'] = rank_positions
    
    print(f"Bulk ranking of {len(df):,} records completed in {dur:.5f} seconds.")
    print(f"Top 5 highest revenue customers:")
    print(df_res.sort_values(by='revenue_rank').head(5)[['customer_id', 'revenue', 'revenue_rank']])
    
    return df_res, rank_positions


# Task 4: Time Performance Comparison
def run_benchmark_comparison(df):
    """
    Benchmark element-wise calculation (e.g. 10% price markup + tax) Loop vs NumPy.
    """
    print("\n--- TASK 4: DETAILED TIME PERFORMANCE COMPARISON ---")
    
    # 1. Time loop version
    start = time.perf_counter()
    result_loop = []
    for val in df['revenue']:
        result_loop.append(val * 1.10)
    loop_time = time.perf_counter() - start

    # 2. Time NumPy version
    start = time.perf_counter()
    result_np = df['revenue'].values * 1.10
    np_time = time.perf_counter() - start

    speedup = loop_time / np_time if np_time > 0 else 1.0
    
    print(f"Operation: Price 10% Inflation Calculation across {len(df):,} records")
    print(f"  - Python Loop Execution Time:  {loop_time:.6f}s")
    print(f"  - NumPy Vectorized Execution:  {np_time:.6f}s")
    print(f"  - Vectorization Speedup:       {speedup:.0f}x Faster")
    
    return loop_time, np_time, speedup


# Task 5: Integrate Back to DataFrame
def integrate_all_features_and_verify(df, normalized_np, z_scores, rankings):
    """
    Integrate NumPy results back to DataFrame and verify shapes and dtypes.
    """
    print("\n--- TASK 5: INTEGRATE BACK TO DATAFRAME & VERIFY ---")
    df_final = df.copy()
    
    df_final['revenue_normalized'] = normalized_np
    df_final['revenue_zscore'] = z_scores
    df_final['revenue_rank'] = rankings
    
    print(f"Final DataFrame Shape: {df_final.shape}")
    print("\nDataFrame Column Data Types (dtypes):")
    print(df_final.dtypes)
    
    print("\nFinal DataFrame Sample Rows:")
    print(df_final.head(10))
    
    return df_final


def generate_benchmark_plot(loop_time, np_time, speedup):
    """Save visualization chart comparing execution times."""
    os.makedirs('output', exist_ok=True)
    
    plt.figure(figsize=(8, 5))
    categories = ['Python Loop', 'NumPy Vectorized']
    times = [loop_time, np_time]
    colors = ['#d95f02', '#1b9e77']
    
    bars = plt.bar(categories, times, color=colors, width=0.5)
    plt.ylabel('Execution Time (Seconds)')
    plt.title(f'Performance Comparison (100,000 Rows)\nSpeedup: {speedup:.0f}x Faster')
    plt.yscale('log')  # Log scale to make tiny milliseconds visible next to seconds
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                 f'{height:.4f}s', ha='center', va='bottom', fontweight='bold')
                 
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('output/vectorization_speedup_benchmark.png')
    plt.close()
    
    print("\nSaved benchmark plot to 'output/vectorization_speedup_benchmark.png'.")


def run_pipeline():
    """Execute full NumPy vectorization workflow demonstration."""
    print("=========================================================")
    print("      NUMPY VECTORISED COMPUTATION WORKFLOW DEMO         ")
    print("=========================================================")
    
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # 1. Create synthetic dataset (100k rows)
    raw_df = create_large_synthetic_dataset(num_records=100000)
    raw_df.to_csv('data/raw/vectorized_raw_data.csv', index=False)
    print(f"\nGenerated 100,000 row dataset ('data/raw/vectorized_raw_data.csv').")
    
    # 2. Task 1: Min-Max Normalization
    df_t1, norm_np, loop_t, np_t = demonstrate_min_max_normalization(raw_df)
    
    # 3. Task 2: Z-Score Normalization
    df_t2, z_scores = demonstrate_zscore_normalization(raw_df)
    
    # 4. Task 3: Bulk Ranking
    df_t3, rankings = demonstrate_bulk_ranking(raw_df)
    
    # 5. Task 4: Detailed Benchmark
    loop_b, np_b, speedup = run_benchmark_comparison(raw_df)
    
    # 6. Task 5: Integration & Verification
    final_df = integrate_all_features_and_verify(raw_df, norm_np, z_scores, rankings)
    
    # Visualizations & saving
    generate_benchmark_plot(loop_b, np_b, speedup)
    final_df.to_csv('data/processed/vectorized_revenue_data.csv', index=False)
    
    print("\nSaved processed clean dataset to 'data/processed/vectorized_revenue_data.csv'.")
    print("Pipeline Execution Completed Successfully.")


if __name__ == '__main__':
    run_pipeline()
