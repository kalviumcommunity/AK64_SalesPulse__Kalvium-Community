# Dashboard Design Documentation

## Information Hierarchy Applied

The dashboard is designed according to the four-level Information Hierarchy to ensure optimal cognitive load management and rapid decision-making:

- **Level 1 (Status - Top Row)**: 5 KPI Summary Cards displaying real-time business health. Answers: *"Are we on track?"*
  1. **Revenue ($5.2M, +12.5%)**: Primary financial performance indicator. Answers: *"What is our top-line growth?"*
  2. **Active Customers (2,500, +5.2%)**: Scale of active buyer base. Answers: *"Is our user base growing?"*
  3. **Avg Order Value ($145, +3.1%)**: Monetization efficiency per transaction. Answers: *"Are customers buying larger packages?"*
  4. **Churn Rate (4.8%, -1.2%)**: Retention efficiency (inverse delta color). Answers: *"Are we retaining revenue and customers?"*
  5. **NPS Score (72, +4)**: Customer satisfaction sentiment. Answers: *"Are users satisfied with the product experience?"*

- **Level 2 (Trends - Middle Section)**: 3 Time Series Trend Charts with reference lines. Answers: *"Is performance improving or degrading over time?"*
  1. **Monthly Revenue Trend**: 12-month line chart with $5.0M green target line.
  2. **Customer Metrics Trend**: Dual line chart comparing Active Customers vs. Churned Customers.
  3. **Average Order Value (AOV) Trend**: 12-month trajectory with historical benchmark.

- **Level 3 (Segments - Lower Section)**: Horizontal Bar Charts breaking down performance by customer segment (Enterprise, Mid-Market, SMB, Starter). Answers: *"Which customer tiers drive revenue and require attention?"*

- **Level 4 (Detail - Bottom & Sidebar)**: Dynamic Data Explorer with interactive sidebar filters (Segment, Date Range), searchable data table, and CSV download button. Answers: *"What are the exact underlying transactional records?"*

---

## Design Principles Applied

1. **Progressive Disclosure**: High-level status KPIs are displayed immediately at the top. Complex segment breakdowns and detailed tabular records are placed further down or behind interactive filters.
2. **Spatial Organization**: Top-left position (highest visual priority) is reserved for Revenue KPI card and Revenue Trend chart. Primary dimension filters reside in the left sidebar.
3. **Consistent Metaphor**: Green (`#2ca02c` / `#10b981`) signifies positive metrics/targets; Red (`#d62728` / `#ef4444`) signifies risk/churn issues; Blue (`#1f77b4` / `#3b82f6`) represents baseline trends.
4. **Context Over Numbers**: Every numerical value includes a comparison context — period-over-period percentage delta, trend direction arrow, or explicit reference target lines.

---

## Color Palette

- **Primary**: `#1f77b4` (Deep Blue) — Main metric series and primary UI elements.
- **Secondary**: `#ff7f0e` (Orange) — Comparison lines and secondary trends.
- **Success / Target**: `#2ca02c` (Green) — Positive deltas, growth indicators, and target threshold lines.
- **Danger / Churn**: `#d62728` (Red) — Negative deltas, churn metrics, and warning thresholds.
- **Neutral Accent**: `#6366f1` (Indigo) & `#f59e0b` (Amber) — Segment breakdowns.

---

## Target Audience

- **Primary (VP of Sales)**: Daily active user. Needs rapid evaluation of monthly revenue against target, segment contributions, and top-tier enterprise accounts.
- **Secondary (CEO)**: Weekly user. Scans Level 1 KPI summary cards in 5 seconds to verify corporate strategy alignment.
- **Tertiary (Data Analysts)**: Heavy exploratory user. Leverages Level 4 filters, table views, and CSV export for deep-dive root cause investigation.

---

## Data Sources & SQL Abstractions

- **KPI Summary Values**: Computed from `vw_monthly_kpi_summary` SQL database view.
- **Trend Time Series**: Queried from `agg_daily_revenue` and `agg_monthly_customer_trends` aggregate tables.
- **Segment Performance**: Computed from `vw_customer_segment_revenue` SQL view using `GROUP BY customer_type`.
- **Detail Records**: Sourced from indexed `customers` JOIN `transactions` relational tables with dynamic parameter filtering.
