# Clean Data Layer Naming Conventions

## Overview
This document defines the naming conventions for all SQL objects in the SalesPulse data layer.
Following these conventions prevents metric drift, ensures discoverability, and enables any team member to navigate the data layer without documentation.

---

## Views

- **Prefix**: `vw_`
- **Pattern**: `vw_[business_entity]_[metric]`
- **Location**: `database/views/`
- **Refresh**: Automatic — recalculated fresh every time queried (stored logic, not stored data)

| View Name | Business Entity | Metric | Business Question |
|---|---|---|---|
| `vw_active_customers` | Customer | 30-day activity & revenue | "Who has ordered recently and how much?" |
| `vw_product_performance` | Product | 90-day revenue & buyer breadth | "Which products drive the most revenue?" |

### Rules for Views
- Prefix **must** be `vw_` — tells any reader this is computed logic, not a raw table
- One view per business concept — never pack all metrics into a single view
- Include a business-readable comment block at the top of every `.sql` file
- Apply WHERE filters to scope the metric (e.g., 30-day rolling window)
- JOIN at a minimum 2 tables; views on single tables are typically unnecessary

---

## Pre-Aggregated Tables

- **Prefix**: `agg_`
- **Pattern**: `agg_[grain]_[subject]`
- **Location**: `database/aggregations/`
- **Refresh**: Scheduled (daily Full Refresh = TRUNCATE + INSERT for daily grain tables)

| Table Name | Grain | Subject | Refresh Schedule |
|---|---|---|---|
| `agg_daily_metrics` | Daily | Revenue & Order Volume per Product Line | Daily full refresh |

### Rules for Aggregated Tables
- Prefix **must** be `agg_` — signals pre-computed data that needs scheduled refresh
- **Always include** `updated_at TIMESTAMP` — dashboards must know data freshness
- **Always include** `order_count` or a row validation field — confirms aggregation was populated
- Never expose raw tables directly to dashboards — only `vw_*` views or `agg_*` tables

---

## General Column Conventions

| Column Type | Convention | Example |
|---|---|---|
| Aggregation date | `aggregation_date` | `aggregation_date DATE` |
| Freshness marker | `updated_at` | `updated_at TIMESTAMP DEFAULT datetime('now')` |
| Revenue | `total_revenue` / `revenue_Xd` | `revenue_30d REAL` |
| Count | `*_count` suffix | `order_count INTEGER` |
| Average | `avg_*` prefix | `avg_order_value REAL` |
| Distinct count | `unique_*` prefix | `unique_buyers INTEGER` |

---

## Benefits of This Convention

1. **Discoverability**: Any analyst knows `vw_` = view, `agg_` = pre-aggregated immediately
2. **No Metric Drift**: Revenue defined once in `vw_active_customers` — not recomputed per dashboard
3. **Staleness Detection**: `updated_at` on all `agg_*` tables allows dashboards to show data age warnings
4. **Maintainability**: One-view-per-concept means changing a definition touches one `.sql` file only
5. **Team Alignment**: New engineers navigate the data layer from naming patterns alone

---

## Folder Structure

```
database/
├── views/
│   ├── vw_active_customers.sql        # Active customer 30-day rolling metrics
│   └── vw_product_performance.sql     # Product revenue & buyer metrics (90 days)
└── aggregations/
    └── agg_daily_metrics.sql          # Daily revenue + order count by product line
```
