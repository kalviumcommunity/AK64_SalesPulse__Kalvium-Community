"""
Behavioural Analysis & User Segmentation Pipeline
--------------------------------------------------
Assignment 2.32 - Kalvium SalesPulse Segment Comparator

This script implements segment-level behavioural analysis:
1. Define Segments and Compute 4+ Metrics (GroupBy aggregation)
2. Summary Statistics Table with Rankings
3. Visual Comparison (Heatmap + Box Plots)
4. Top and Bottom Performer Analysis
5. Business-Facing Actionable Insights per Segment

Key Insight: Aggregate "average" metrics hide radically different
segment behaviours. Enterprise has 1% churn; SMB has 12% churn.
Segment strategy MUST be evidence-based and segment-specific.
"""

import os
import sys
import json
import numpy as np

# Ensure UTF-8 output on Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for file output
import matplotlib.pyplot as plt
import seaborn as sns


# ──────────────────────────────────────────────────────────────────────────────
# Synthetic Dataset Generator
# ──────────────────────────────────────────────────────────────────────────────

def create_segmented_customer_dataset(num_records: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Generate a realistic synthetic customer dataset with three segments:
      - Enterprise  (5% of base  | ~$150k LTV | ~1%  churn | premium support)
      - SMB         (40% of base | ~$8k  LTV  | ~12% churn | standard support)
      - Startup     (55% of base | ~$2k  LTV  | ~8%  churn | self-service)

    Columns produced:
        customer_id, customer_type, region, product_tier,
        lifetime_value, churn, support_tickets, retention_days,
        feature_adoption_score, nps_score
    """
    np.random.seed(seed)

    n_ent     = int(num_records * 0.05)
    n_smb     = int(num_records * 0.40)
    n_startup = num_records - n_ent - n_smb

    # ── Customer types ──────────────────────────────────────────────────────
    customer_type = ['Enterprise'] * n_ent + ['SMB'] * n_smb + ['Startup'] * n_startup

    # ── Lifetime Value (LTV) ────────────────────────────────────────────────
    ltv_ent     = np.random.uniform(120_000, 180_000, size=n_ent)
    ltv_smb     = np.random.uniform(5_000,   12_000,  size=n_smb)
    ltv_startup = np.random.uniform(1_000,    4_000,  size=n_startup)
    lifetime_value = np.concatenate([ltv_ent, ltv_smb, ltv_startup])

    # ── Churn (binary flag) ─────────────────────────────────────────────────
    churn = np.concatenate([
        (np.random.rand(n_ent)     < 0.01).astype(int),
        (np.random.rand(n_smb)     < 0.12).astype(int),
        (np.random.rand(n_startup) < 0.08).astype(int),
    ])

    # ── Support Tickets ─────────────────────────────────────────────────────
    support_tickets = np.concatenate([
        np.random.poisson(lam=1.5, size=n_ent),    # Enterprise: few tickets (dedicated CSM)
        np.random.poisson(lam=4.5, size=n_smb),    # SMB: high tickets (less guided)
        np.random.poisson(lam=3.0, size=n_startup), # Startup: moderate (self-service)
    ])

    # ── Retention Days ──────────────────────────────────────────────────────
    retention_days = np.concatenate([
        np.random.randint(700, 1200, size=n_ent),   # Enterprise: long contracts
        np.random.randint(90,   600, size=n_smb),   # SMB: medium tenure
        np.random.randint(30,   300, size=n_startup),# Startup: shorter tenure
    ])

    # ── Feature Adoption Score (0–100) ──────────────────────────────────────
    feature_adoption = np.concatenate([
        np.random.uniform(75, 100, size=n_ent),
        np.random.uniform(40,  80, size=n_smb),
        np.random.uniform(15,  55, size=n_startup),
    ])

    # ── NPS Score (−100 to +100) ────────────────────────────────────────────
    nps = np.concatenate([
        np.random.uniform(60,  100, size=n_ent),
        np.random.uniform(10,   60, size=n_smb),
        np.random.uniform(-20,  40, size=n_startup),
    ])

    # ── Region (secondary segment dimension) ────────────────────────────────
    regions_ent     = np.random.choice(['APAC', 'EMEA', 'AMER'], size=n_ent,     p=[0.2, 0.3, 0.5])
    regions_smb     = np.random.choice(['APAC', 'EMEA', 'AMER'], size=n_smb,     p=[0.3, 0.3, 0.4])
    regions_startup = np.random.choice(['APAC', 'EMEA', 'AMER'], size=n_startup, p=[0.4, 0.2, 0.4])
    region = np.concatenate([regions_ent, regions_smb, regions_startup])

    # ── Product Tier ────────────────────────────────────────────────────────
    tier_ent     = np.random.choice(['Platinum', 'Gold'],          size=n_ent,     p=[0.85, 0.15])
    tier_smb     = np.random.choice(['Gold',     'Silver'],        size=n_smb,     p=[0.55, 0.45])
    tier_startup = np.random.choice(['Silver',   'Free'],          size=n_startup, p=[0.40, 0.60])
    product_tier = np.concatenate([tier_ent, tier_smb, tier_startup])

    df = pd.DataFrame({
        'customer_id':            [f'CUST_{5000 + i}' for i in range(num_records)],
        'customer_type':          customer_type,
        'region':                 region,
        'product_tier':           product_tier,
        'lifetime_value':         np.round(lifetime_value, 2),
        'churn':                  churn,
        'support_tickets':        support_tickets,
        'retention_days':         retention_days,
        'feature_adoption_score': np.round(feature_adoption, 1),
        'nps_score':              np.round(nps, 1),
    })

    # Shuffle for realism
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


# ──────────────────────────────────────────────────────────────────────────────
# Task 1: Define Segments and Compute 4+ Metrics
# ──────────────────────────────────────────────────────────────────────────────

def task1_define_segments_compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Task 1: Group by customer_type (3 segments) and compute 5 metrics.

    Metrics:
      - avg_ltv            : Mean Lifetime Value per segment
      - churn_rate         : Mean churn probability
      - avg_tickets        : Mean support tickets filed
      - avg_retention      : Mean retention days
      - avg_adoption       : Mean feature adoption score (0–100)
      - count              : Number of customers (segment size)

    Returns:
        segment_metrics (pd.DataFrame) — raw numeric metrics indexed by segment
    """
    print("\n" + "=" * 60)
    print("  TASK 1: DEFINE SEGMENTS & COMPUTE METRICS")
    print("=" * 60)

    segment_metrics = df.groupby('customer_type').agg(
        avg_ltv       =('lifetime_value',         'mean'),
        churn_rate    =('churn',                  'mean'),
        avg_tickets   =('support_tickets',         'mean'),
        avg_retention =('retention_days',          'mean'),
        avg_adoption  =('feature_adoption_score',  'mean'),
        avg_nps       =('nps_score',               'mean'),
        count         =('customer_id',             'count'),
    ).round(4)

    print("\nRaw Segment Metrics (5+ computed metrics across 3 segments):\n")
    print(segment_metrics.to_string())

    # Segment size documentation
    print("\nSegment Sample Sizes:")
    for seg, row in segment_metrics.iterrows():
        pct = row['count'] / segment_metrics['count'].sum() * 100
        print(f"  {seg:12s}: {int(row['count'])} customers ({pct:.1f}% of base)")

    return segment_metrics


# ──────────────────────────────────────────────────────────────────────────────
# Task 2: Summary Statistics Table with Rankings
# ──────────────────────────────────────────────────────────────────────────────

def task2_summary_statistics_table(segment_metrics: pd.DataFrame) -> pd.DataFrame:
    """
    Task 2: Format metrics for readability and rank segments on 2+ dimensions.

    Rankings:
      - ltv_rank    : 1 = highest lifetime value
      - churn_rank  : 1 = lowest churn (best retention)
      - adoption_rank: 1 = highest feature adoption

    Returns:
        segment_summary (pd.DataFrame) — formatted table with ranks
    """
    print("\n" + "=" * 60)
    print("  TASK 2: SUMMARY STATISTICS TABLE WITH RANKINGS")
    print("=" * 60)

    summary = segment_metrics.copy()

    # Rankings
    summary['ltv_rank']      = summary['avg_ltv'].rank(ascending=False).astype(int)
    summary['churn_rank']    = summary['churn_rate'].rank(ascending=True).astype(int)   # lower churn -> rank 1
    summary['adoption_rank'] = summary['avg_adoption'].rank(ascending=False).astype(int)

    # Human-readable formatted columns
    summary['ltv_fmt']       = summary['avg_ltv'].apply(lambda x: f'${x:>10,.0f}')
    summary['churn_fmt']     = summary['churn_rate'].apply(lambda x: f'{x:.1%}')
    summary['retention_fmt'] = summary['avg_retention'].apply(lambda x: f'{x:.0f} days')
    summary['tickets_fmt']   = summary['avg_tickets'].apply(lambda x: f'{x:.2f}')
    summary['adoption_fmt']  = summary['avg_adoption'].apply(lambda x: f'{x:.1f}/100')
    summary['nps_fmt']       = summary['avg_nps'].apply(lambda x: f'{x:+.1f}')

    display_cols = [
        'ltv_fmt', 'ltv_rank',
        'churn_fmt', 'churn_rank',
        'retention_fmt',
        'tickets_fmt',
        'adoption_fmt', 'adoption_rank',
        'nps_fmt',
        'count',
    ]

    print("\nFormatted Segment Comparison Table (ranked on LTV, Churn, Adoption):\n")
    print(
        summary[display_cols]
        .rename(columns={
            'ltv_fmt':       'Avg LTV',
            'ltv_rank':      'LTV Rank',
            'churn_fmt':     'Churn Rate',
            'churn_rank':    'Churn Rank',
            'retention_fmt': 'Avg Retention',
            'tickets_fmt':   'Avg Tickets',
            'adoption_fmt':  'Feature Adoption',
            'adoption_rank': 'Adoption Rank',
            'nps_fmt':       'NPS Score',
            'count':         'Customers',
        })
        .to_string()
    )

    return summary


# ──────────────────────────────────────────────────────────────────────────────
# Task 3: Visual Comparison (Heatmap + Box Plots)
# ──────────────────────────────────────────────────────────────────────────────

def task3_visual_comparison(df: pd.DataFrame,
                             segment_metrics: pd.DataFrame,
                             output_dir: str = 'output') -> None:
    """
    Task 3: Produce two visualisations.

    (a) Segment Comparison Heatmap
        - Normalised [0, 1] per metric so disparate scales are comparable.
        - Annotated with actual values; RdYlGn colormap (green = better).
        - Churn inverted so green = low churn.

    (b) Box Plots
        - Distribution of lifetime_value by customer_type.
        - Shows spread + outliers, not just the mean.
    """
    print("\n" + "=" * 60)
    print("  TASK 3: VISUAL COMPARISON (HEATMAP + BOX PLOTS)")
    print("=" * 60)

    os.makedirs(output_dir, exist_ok=True)

    # ── (a) Segment Comparison Heatmap ──────────────────────────────────────
    heat_data = segment_metrics[
        ['avg_ltv', 'churn_rate', 'avg_tickets', 'avg_retention', 'avg_adoption', 'avg_nps']
    ].copy()

    # Build annotation matrix with human-readable labels
    annot_data = heat_data.copy()
    annot_data['avg_ltv']        = annot_data['avg_ltv'].apply(lambda x: f'${x:,.0f}')
    annot_data['churn_rate']     = annot_data['churn_rate'].apply(lambda x: f'{x:.1%}')
    annot_data['avg_tickets']    = annot_data['avg_tickets'].apply(lambda x: f'{x:.2f}')
    annot_data['avg_retention']  = annot_data['avg_retention'].apply(lambda x: f'{x:.0f}d')
    annot_data['avg_adoption']   = annot_data['avg_adoption'].apply(lambda x: f'{x:.1f}')
    annot_data['avg_nps']        = annot_data['avg_nps'].apply(lambda x: f'{x:+.1f}')

    # Normalise [0, 1] for colour intensity
    norm_data = heat_data.copy()
    for col in norm_data.columns:
        col_range = norm_data[col].max() - norm_data[col].min()
        if col_range > 0:
            norm_data[col] = (norm_data[col] - norm_data[col].min()) / col_range
        else:
            norm_data[col] = 0.5

    # Invert churn and support_tickets — lower is better -> green
    norm_data['churn_rate']  = 1 - norm_data['churn_rate']
    norm_data['avg_tickets'] = 1 - norm_data['avg_tickets']

    nice_col_names = {
        'avg_ltv':       'Avg LTV ($)',
        'churn_rate':    'Churn Rate ↓',
        'avg_tickets':   'Support Tickets ↓',
        'avg_retention': 'Retention (days)',
        'avg_adoption':  'Feature Adoption',
        'avg_nps':       'NPS Score',
    }
    norm_data  = norm_data.rename(columns=nice_col_names)
    annot_data = annot_data.rename(columns=nice_col_names)

    fig, ax = plt.subplots(figsize=(12, 4))
    sns.heatmap(
        norm_data,
        annot=annot_data.values,
        fmt='',
        cmap='RdYlGn',
        linewidths=0.5,
        linecolor='white',
        ax=ax,
        cbar_kws={'label': '<- Worse    Better ->', 'shrink': 0.85},
        vmin=0, vmax=1,
    )
    ax.set_title(
        'Segment Comparison Heatmap  |  Green = Better Performance  |  ↓ = Lower is Better',
        fontsize=13, fontweight='bold', pad=14,
    )
    ax.set_xlabel('Metric', fontsize=11)
    ax.set_ylabel('Customer Segment', fontsize=11)
    ax.tick_params(axis='x', rotation=15)
    ax.tick_params(axis='y', rotation=0)
    plt.tight_layout()

    heatmap_path = os.path.join(output_dir, 'segment_heatmap.png')
    plt.savefig(heatmap_path, dpi=150)
    plt.close()
    print(f"\n  [OK] Saved heatmap -> '{heatmap_path}'")

    # ── (b) Box Plots — distribution within each segment ───────────────────
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    palette = {'Enterprise': '#1b9e77', 'SMB': '#d95f02', 'Startup': '#7570b3'}

    order = ['Enterprise', 'SMB', 'Startup']

    # Lifetime Value distribution
    sns.boxplot(
        data=df, x='customer_type', y='lifetime_value',
        order=order, palette=palette, ax=axes[0],
        flierprops=dict(marker='o', markersize=3, alpha=0.5),
    )
    axes[0].set_title('Lifetime Value Distribution', fontweight='bold')
    axes[0].set_xlabel('Customer Segment')
    axes[0].set_ylabel('Lifetime Value ($)')
    axes[0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, _: f'${x:,.0f}')
    )

    # Retention Days distribution
    sns.boxplot(
        data=df, x='customer_type', y='retention_days',
        order=order, palette=palette, ax=axes[1],
        flierprops=dict(marker='o', markersize=3, alpha=0.5),
    )
    axes[1].set_title('Retention Days Distribution', fontweight='bold')
    axes[1].set_xlabel('Customer Segment')
    axes[1].set_ylabel('Days Retained')

    # Feature Adoption Score distribution
    sns.boxplot(
        data=df, x='customer_type', y='feature_adoption_score',
        order=order, palette=palette, ax=axes[2],
        flierprops=dict(marker='o', markersize=3, alpha=0.5),
    )
    axes[2].set_title('Feature Adoption Score Distribution', fontweight='bold')
    axes[2].set_xlabel('Customer Segment')
    axes[2].set_ylabel('Adoption Score (0–100)')

    fig.suptitle(
        'Within-Segment Distributions — Box Plots (Spread & Outliers)',
        fontsize=14, fontweight='bold', y=1.02,
    )
    plt.tight_layout()

    boxplot_path = os.path.join(output_dir, 'segment_boxplots.png')
    plt.savefig(boxplot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved box plots -> '{boxplot_path}'")


# ──────────────────────────────────────────────────────────────────────────────
# Task 4: Top and Bottom Performer Analysis
# ──────────────────────────────────────────────────────────────────────────────

def task4_top_bottom_performer_analysis(segment_metrics: pd.DataFrame) -> dict:
    """
    Task 4: Identify the top/bottom performers across key metrics.

    Findings:
      - Highest LTV segment   (most valuable)
      - Lowest  LTV segment   (least valuable)
      - Highest churn segment (most at risk)
      - Lowest  churn segment (most loyal)
      - Best    retention     segment
      - Best    feature adoption segment

    Returns:
        insights_dict (dict) — structured key findings
    """
    print("\n" + "=" * 60)
    print("  TASK 4: TOP & BOTTOM PERFORMER ANALYSIS")
    print("=" * 60)

    top_ltv_seg     = segment_metrics['avg_ltv'].idxmax()
    bottom_ltv_seg  = segment_metrics['avg_ltv'].idxmin()
    high_churn_seg  = segment_metrics['churn_rate'].idxmax()
    low_churn_seg   = segment_metrics['churn_rate'].idxmin()
    best_retention  = segment_metrics['avg_retention'].idxmax()
    best_adoption   = segment_metrics['avg_adoption'].idxmax()
    best_nps        = segment_metrics['avg_nps'].idxmax()

    top_ltv_val    = segment_metrics.loc[top_ltv_seg,    'avg_ltv']
    bottom_ltv_val = segment_metrics.loc[bottom_ltv_seg, 'avg_ltv']
    high_churn_val = segment_metrics.loc[high_churn_seg, 'churn_rate']
    low_churn_val  = segment_metrics.loc[low_churn_seg,  'churn_rate']
    ret_val        = segment_metrics.loc[best_retention, 'avg_retention']
    adp_val        = segment_metrics.loc[best_adoption,  'avg_adoption']
    nps_val        = segment_metrics.loc[best_nps,       'avg_nps']

    insights = f"""
  HIGHEST VALUE SEGMENT  : {top_ltv_seg:<15} -> ${top_ltv_val:>10,.0f} avg LTV
  LOWEST VALUE SEGMENT   : {bottom_ltv_seg:<15} -> ${bottom_ltv_val:>10,.0f} avg LTV
  LTV DIFFERENCE         : {top_ltv_val / bottom_ltv_val:.0f}× — critical for budget allocation

  HIGHEST CHURN SEGMENT  : {high_churn_seg:<15} -> {high_churn_val:.1%} churn rate  <- intervention needed
  LOWEST CHURN SEGMENT   : {low_churn_seg:<15} -> {low_churn_val:.1%} churn rate  <- protect at all cost

  BEST RETENTION SEGMENT : {best_retention:<15} -> {ret_val:.0f} days avg retention
  BEST ADOPTION SEGMENT  : {best_adoption:<15} -> {adp_val:.1f}/100 feature adoption
  BEST NPS SEGMENT       : {best_nps:<15} -> {nps_val:+.1f} NPS score
"""
    print(insights)

    insights_dict = {
        'highest_value_segment':  {'segment': top_ltv_seg,    'avg_ltv': round(top_ltv_val, 2)},
        'lowest_value_segment':   {'segment': bottom_ltv_seg, 'avg_ltv': round(bottom_ltv_val, 2)},
        'highest_churn_segment':  {'segment': high_churn_seg, 'churn_rate': round(high_churn_val, 4)},
        'lowest_churn_segment':   {'segment': low_churn_seg,  'churn_rate': round(low_churn_val, 4)},
        'best_retention_segment': {'segment': best_retention, 'avg_retention_days': round(ret_val, 1)},
        'best_adoption_segment':  {'segment': best_adoption,  'avg_adoption_score': round(adp_val, 1)},
        'best_nps_segment':       {'segment': best_nps,       'avg_nps': round(nps_val, 1)},
    }

    return insights_dict


# ──────────────────────────────────────────────────────────────────────────────
# Task 5: Business-Facing Insights
# ──────────────────────────────────────────────────────────────────────────────

def task5_business_facing_insights(segment_metrics: pd.DataFrame,
                                   insights_dict: dict,
                                   output_dir: str = 'output') -> str:
    """
    Task 5: Write 2–3 sentence business insight + specific action recommendation
    for EACH of the 3 segments, grounded in the observed metrics.

    Outputs:
      - Prints structured strategy summary to console
      - Saves to output/segment_strategy_report.txt
    """
    print("\n" + "=" * 60)
    print("  TASK 5: BUSINESS-FACING SEGMENT INSIGHTS")
    print("=" * 60)

    ent  = segment_metrics.loc['Enterprise']
    smb  = segment_metrics.loc['SMB']
    strt = segment_metrics.loc['Startup']

    report = f"""
+==============================================================+
|        SEGMENT STRATEGY SUMMARY — SALESPULSE 2.32           |
+==============================================================+

--------------------------------------------------------------
ENTERPRISE  ({int(ent['count'])} customers | {ent['count']/segment_metrics['count'].sum():.0%} of base)
--------------------------------------------------------------
  Observed:  Avg LTV ${ent['avg_ltv']:,.0f} | Churn {ent['churn_rate']:.1%} |
             Retention {ent['avg_retention']:.0f} days | Adoption {ent['avg_adoption']:.1f}/100 | NPS {ent['avg_nps']:+.1f}

  Insight:   Enterprise is the revenue anchor — {ent['count']/segment_metrics['count'].sum():.0%} of the customer base
             generates disproportionate LTV at ${ent['avg_ltv']:,.0f} per customer. Their
             {ent['churn_rate']:.1%} churn rate is near-zero, but any single churned enterprise
             account represents the equivalent of ~{round(ent['avg_ltv']/smb['avg_ltv']):.0f} SMB customers lost.

  Action:    Assign dedicated Customer Success Managers (CSMs) and maintain SLA-backed
             premium support. Run quarterly Executive Business Reviews (EBRs) to surface
             expansion opportunities. Protect this segment — do not cut support budget here.

--------------------------------------------------------------
SMB  ({int(smb['count'])} customers | {smb['count']/segment_metrics['count'].sum():.0%} of base)
--------------------------------------------------------------
  Observed:  Avg LTV ${smb['avg_ltv']:,.0f} | Churn {smb['churn_rate']:.1%} |
             Retention {smb['avg_retention']:.0f} days | Adoption {smb['avg_adoption']:.1f}/100 | NPS {smb['avg_nps']:+.1f}

  Insight:   SMB customers represent {smb['count']/segment_metrics['count'].sum():.0%} of the base and carry a dangerously high
             {smb['churn_rate']:.1%} churn rate — 12× Enterprise. Their average {smb['avg_tickets']:.1f} support
             tickets per customer indicate friction in onboarding and product usage, directly
             driving churn. Low feature adoption ({smb['avg_adoption']:.1f}/100) confirms shallow product
             engagement before customers abandon.

  Action:    Launch automated onboarding email sequences triggered by low feature-adoption
             signals (<40/100). Introduce a cheaper tiered support plan (chat-first, no
             phone), and create SMB-specific playbooks that reduce time-to-value to <14 days.
             Target churn reduction from {smb['churn_rate']:.0%} to <8% in 2 quarters.

--------------------------------------------------------------
STARTUP  ({int(strt['count'])} customers | {strt['count']/segment_metrics['count'].sum():.0%} of base)
--------------------------------------------------------------
  Observed:  Avg LTV ${strt['avg_ltv']:,.0f} | Churn {strt['churn_rate']:.1%} |
             Retention {strt['avg_retention']:.0f} days | Adoption {strt['avg_adoption']:.1f}/100 | NPS {strt['avg_nps']:+.1f}

  Insight:   Startups are the largest cohort ({strt['count']/segment_metrics['count'].sum():.0%} of base) but carry the lowest
             LTV at ${strt['avg_ltv']:,.0f} — making individual-level human support economically
             unviable. With {strt['churn_rate']:.1%} churn and {strt['avg_adoption']:.1f}/100 feature adoption, the biggest
             lever is education: customers who discover value early are significantly more
             likely to expand into SMB/Enterprise contracts as they grow.

  Action:    Invest in self-service resources — interactive product tours, in-app tooltips,
             and a searchable knowledge base. Implement a usage-based upgrade nudge when
             Startup customers hit 80% of their plan limits. Treat this segment as a
             pipeline (future SMB/Enterprise), not just a revenue line.

--------------------------------------------------------------
CROSS-SEGMENT STRATEGIC PRIORITIES
--------------------------------------------------------------
  1. BUDGET ALLOCATION:  Concentrate 60% of Customer Success budget on Enterprise
     (highest LTV, lowest churn risk), 30% on SMB churn reduction (highest ROI on
     intervention), and 10% on Startup self-service infrastructure.

  2. PRODUCT PRIORITISATION: Build features requested by Enterprise first (NPS {ent['avg_nps']:+.1f}).
     Validate each SMB feature request against churn signal data before committing roadmap.
     Startup requests -> direct to community/upvote forum.

  3. REPORTING: Stop reporting aggregate "average churn" ({segment_metrics['churn_rate'].mean():.1%}).
     Report per-segment. Stakeholders making decisions on the aggregate miss the 12×
     churn gap between Enterprise and SMB entirely.
"""

    print(report)

    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, 'segment_strategy_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"  [OK] Saved strategy report -> '{report_path}'")

    return report


# ──────────────────────────────────────────────────────────────────────────────
# Secondary Visualisation: Distribution Comparison
# ──────────────────────────────────────────────────────────────────────────────

def generate_segment_distribution_comparison(df: pd.DataFrame,
                                              output_dir: str = 'output') -> None:
    """
    Additional visual: bar chart comparing revenue contribution vs churn burden.
    Starkly illustrates the 'Segment Paradox'.
    """
    os.makedirs(output_dir, exist_ok=True)

    seg_rev   = df.groupby('customer_type')['lifetime_value'].sum()
    seg_churn = df.groupby('customer_type')['churn'].mean() * 100
    seg_count = df.groupby('customer_type')['customer_id'].count()

    total_rev = seg_rev.sum()
    total_cust = seg_count.sum()

    rev_share   = (seg_rev / total_rev * 100).reindex(['Enterprise', 'SMB', 'Startup'])
    cust_share  = (seg_count / total_cust * 100).reindex(['Enterprise', 'SMB', 'Startup'])
    churn_rates = seg_churn.reindex(['Enterprise', 'SMB', 'Startup'])

    x = np.arange(3)
    width = 0.28
    colors = ['#1b9e77', '#d95f02', '#7570b3']
    labels = ['Enterprise', 'SMB', 'Startup']

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: Revenue share vs Customer share
    bars1 = axes[0].bar(x - width / 2, rev_share.values, width,
                        color=colors, label='Revenue Share', alpha=0.9)
    bars2 = axes[0].bar(x + width / 2, cust_share.values, width,
                        color=colors, label='Customer Share', alpha=0.5, hatch='//')

    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, fontsize=11)
    axes[0].set_ylabel('Share of Total (%)', fontsize=11)
    axes[0].set_title('Segment Paradox: Revenue vs Customer Size', fontweight='bold', fontsize=12)
    axes[0].legend(['Revenue Share (%)', 'Customer Share (%)'])
    axes[0].grid(axis='y', linestyle='--', alpha=0.6)
    for bar in bars1:
        h = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width() / 2, h + 0.5, f'{h:.1f}%',
                     ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Right: Churn rate by segment
    bar3 = axes[1].bar(x, churn_rates.values, color=colors, alpha=0.9, edgecolor='white', linewidth=1.5)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, fontsize=11)
    axes[1].set_ylabel('Churn Rate (%)', fontsize=11)
    axes[1].set_title('Churn Rate by Segment — Hidden by Aggregate Reporting', fontweight='bold', fontsize=12)
    axes[1].axhline(y=churn_rates.mean(), color='gray', linestyle='--', linewidth=1.5,
                    label=f'Aggregate "Average" = {churn_rates.mean():.1f}%')
    axes[1].legend(fontsize=10)
    axes[1].grid(axis='y', linestyle='--', alpha=0.6)
    for bar in bar3:
        h = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width() / 2, h + 0.1, f'{h:.1f}%',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

    fig.suptitle(
        'Behavioural Analysis: Why Aggregate Metrics Are Misleading',
        fontsize=14, fontweight='bold', y=1.02,
    )
    plt.tight_layout()
    out_path = os.path.join(output_dir, 'segment_distribution_comparison.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved distribution comparison -> '{out_path}'")


# ──────────────────────────────────────────────────────────────────────────────
# Audit Export
# ──────────────────────────────────────────────────────────────────────────────

def export_audit_artifacts(df: pd.DataFrame,
                            segment_metrics: pd.DataFrame,
                            summary: pd.DataFrame,
                            insights_dict: dict,
                            output_dir: str = 'output') -> None:
    """
    Export all processed data and audit artifacts to disk.

    Files:
      - data/raw/segment_customer_data.csv        (synthetic raw dataset)
      - data/processed/segment_metrics.csv        (per-segment aggregated metrics)
      - data/processed/segment_summary_ranked.csv (formatted summary + ranks)
      - output/segment_insights.csv               (key insights per segment)
      - output/segment_insights_summary.json      (structured key findings JSON)
    """
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    df.to_csv('data/raw/segment_customer_data.csv', index=False)
    segment_metrics.to_csv('data/processed/segment_metrics.csv')
    summary.to_csv('data/processed/segment_summary_ranked.csv')

    # Flat insights CSV (one row per segment)
    insights_rows = []
    for seg in segment_metrics.index:
        row = segment_metrics.loc[seg]
        insights_rows.append({
            'segment':         seg,
            'customer_count':  int(row['count']),
            'avg_ltv':         f"${row['avg_ltv']:,.0f}",
            'churn_rate':      f"{row['churn_rate']:.1%}",
            'avg_tickets':     round(row['avg_tickets'], 2),
            'avg_retention':   f"{row['avg_retention']:.0f} days",
            'avg_adoption':    f"{row['avg_adoption']:.1f}/100",
            'avg_nps':         f"{row['avg_nps']:+.1f}",
        })
    pd.DataFrame(insights_rows).to_csv(
        os.path.join(output_dir, 'segment_insights.csv'), index=False
    )

    with open(os.path.join(output_dir, 'segment_insights_summary.json'), 'w') as f:
        json.dump(insights_dict, f, indent=2)

    print("\n  [OK] Audit artifacts exported:")
    print("       data/raw/segment_customer_data.csv")
    print("       data/processed/segment_metrics.csv")
    print("       data/processed/segment_summary_ranked.csv")
    print("       output/segment_insights.csv")
    print("       output/segment_insights_summary.json")


# ──────────────────────────────────────────────────────────────────────────────
# Pipeline Orchestrator
# ──────────────────────────────────────────────────────────────────────────────

def run_pipeline() -> None:
    """Execute the complete Behavioural Analysis & User Segmentation pipeline."""

    print("\n" + "=" * 60)
    print("  BEHAVIOURAL ANALYSIS & USER SEGMENTATION (2.32)")
    print("  SalesPulse — Segment Comparator")
    print("=" * 60)

    # ── 0. Generate synthetic dataset ───────────────────────────────────────
    df = create_segmented_customer_dataset(num_records=1000, seed=42)
    print(f"\n  Dataset: {len(df)} customers, {df['customer_type'].nunique()} segments, "
          f"{df.shape[1]} features")

    # ── Task 1: Define Segments & Compute Metrics ────────────────────────────
    segment_metrics = task1_define_segments_compute_metrics(df)

    # ── Task 2: Summary Statistics Table with Rankings ───────────────────────
    summary = task2_summary_statistics_table(segment_metrics)

    # ── Task 3: Visual Comparison ────────────────────────────────────────────
    task3_visual_comparison(df, segment_metrics, output_dir='output')
    generate_segment_distribution_comparison(df, output_dir='output')

    # ── Task 4: Top & Bottom Performer Analysis ──────────────────────────────
    insights_dict = task4_top_bottom_performer_analysis(segment_metrics)

    # ── Task 5: Business-Facing Insights ────────────────────────────────────
    task5_business_facing_insights(segment_metrics, insights_dict, output_dir='output')

    # ── Export Audit Artifacts ───────────────────────────────────────────────
    export_audit_artifacts(df, segment_metrics, summary, insights_dict)

    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE — ALL 5 TASKS EXECUTED SUCCESSFULLY")
    print("=" * 60)
    print("\n  Output files:")
    print("    output/segment_heatmap.png")
    print("    output/segment_boxplots.png")
    print("    output/segment_distribution_comparison.png")
    print("    output/segment_strategy_report.txt")
    print("    output/segment_insights.csv")
    print("    output/segment_insights_summary.json\n")


if __name__ == '__main__':
    run_pipeline()
