# SalesPulse Business Visualisation Architecture

This directory contains high-resolution (300 DPI) visualisations built in compliance with modern business data communication principles (Assignment 2.45).

---

## Unified Palette System & Accessibility

Every chart strictly follows the SalesPulse design token palette:

- **Primary (`#1f77b4`)**: Core business metric, lead category (Analytics Suite)
- **Secondary (`#ff7f0e`)**: Secondary category comparison (CRM Enterprise)
- **Success (`#2ca02c`)**: Growth, target achievements, order distributions
- **Danger (`#d62728`)**: Anomalies, dips, target lines, outlier warnings
- **Purple (`#9467bd`)**: Emerging product modules (AI Insight Hub)

### Accessibility Considerations
- **Color Blindness**: All multi-line and scatter charts combine color with distinct marker shapes (`'o'`, `'s'`, `'^'`) and line styles so information is preserved in grayscale or under red-green color blindness.
- **Contrast**: Text labels use dark slate (`#1e293b`) or white on dark backgrounds to guarantee high contrast.

---

## Chart Catalog & Technical Breakdown

### Chart 1: Revenue by Product Line
- **File**: [`chart1_revenue_by_product.png`](chart1_revenue_by_product.png)
- **Type**: Horizontal Bar Chart (Comparison across discrete categories)
- **Business Question**: Which product line generates the most revenue in Q4?
- **Key Insight**: Analytics Suite dominates Q4 revenue at **$1.42M**, generating 2.9x more revenue than the lowest module.
- **Labels Added**: Title, X-axis (`Revenue ($ USD)` in $M format), Y-axis (`Product Line`), exact value labels on each bar.
- **Annotation**: Highlight box marking **Analytics Suite** as Market Leader.

### Chart 2: Monthly Revenue Trend
- **File**: [`chart2_revenue_trend.png`](chart2_revenue_trend.png)
- **Type**: Multi-series Line Chart (Trend over continuous time)
- **Business Question**: How has revenue performed across the top 3 product lines over the last 12 months?
- **Key Insight**: Steady annual growth across all 3 modules, with Analytics Suite reaching a peak of **$650K/mo** in December.
- **Labels Added**: Title, X-axis (`Month`), Y-axis (`Revenue ($ USD)` formatted as $K), Series Legend, Target line legend.
- **Annotation**: 
  - **August Seasonal Dip**: Highlighted summer slowdown on Analytics Suite line.
  - **Target Line**: Dashed horizontal reference line at **$500K/month target**.

### Chart 3: Order Value Distribution
- **File**: [`chart3_order_value_distribution.png`](chart3_order_value_distribution.png)
- **Type**: Histogram (Distribution of continuous values)
- **Business Question**: What is the typical order value range across customer transactions?
- **Key Insight**: Clear **bimodal distribution** separating self-serve SMB orders (~$180 peak) from high-touch Enterprise orders (~$550 peak).
- **Labels Added**: Title, X-axis (`Order Amount ($ USD)`), Y-axis (`Transaction Count`), bin border lines.
- **Annotation**: Dual callout boxes marking **Peak 1 (SMB Tier)** and **Peak 2 (Enterprise Tier)**.

### Chart 4: Quarterly Revenue Composition
- **File**: [`chart4_revenue_composition.png`](chart4_revenue_composition.png)
- **Type**: Stacked Bar Chart (Composition / Part-to-Whole over discrete quarters)
- **Business Question**: How is total quarterly revenue composed across product lines, and how is product mix shifting?
- **Key Insight**: Total quarterly revenue expanded from **$3.38M in Q1** to **$4.84M in Q4**, driven by rapid expansion of the AI Insight Hub.
- **Labels Added**: Title, X-axis (`Fiscal Quarter`), Y-axis (`Total Revenue ($ USD)` in $M), Product Legend, Bar top totals.
- **Annotation**: Highlight arrow on AI Insight Hub segment showing double-digit quarter-over-quarter expansion.

### Chart 5: Marketing Spend vs. Revenue Generated
- **File**: [`chart5_marketing_vs_revenue.png`](chart5_marketing_vs_revenue.png)
- **Type**: Scatter Plot with Linear Trendline (Correlation between two numerical variables)
- **Business Question**: Does marketing campaign expenditure correlate directly with generated revenue?
- **Key Insight**: Strong positive linear correlation (**r = 0.88**), indicating high return on marketing spend across 49 of 50 campaigns.
- **Labels Added**: Title, X-axis (`Marketing Spend ($ USD)` in $K), Y-axis (`Revenue Generated ($ USD)` in $K), Correlation text block, Trendline equation.
- **Annotation**: Marked single inefficient **Outlier Campaign** ($115K spend producing only $140K revenue).

---

## Multi-Chart Executive Overview
- **File**: [`dashboard_consistent_colors.png`](dashboard_consistent_colors.png)
- **Description**: 6-panel summary dashboard demonstrating color token consistency and layout hierarchy across all 5 chart types.
