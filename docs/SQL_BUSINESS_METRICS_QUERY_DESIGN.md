# SalesPulse SQL Business Metrics Query Design

## Overview
This document describes the SQL-first metric architecture for SalesPulse analytics.
Metrics are defined once in `.sql` files under `queries/` and loaded via `load_query()` in Python.
All teams execute the same files — achieving one truth for every KPI.

## Query Files

| File | Metric | Tables Used | Key Technique |
|---|---|---|---|
| `queries/monthly_active_users.sql` | Monthly Active Users by segment | `transactions`, `customers` | `CASE WHEN` conditional aggregation |
| `queries/revenue_by_segment.sql` | Revenue per customer segment per month | `transactions`, `customers` | `JOIN` + `GROUP BY` + 4+ aggregates |
| `queries/conversion_funnel.sql` | Daily signup → purchase conversion % | `users` | `CASE WHEN` conditional counting + `ROUND` |

## Python Usage Pattern

```python
def load_query(query_name, queries_dir='queries'):
    with open(f'{queries_dir}/{query_name}.sql', 'r') as f:
        return f.read()

mau = pd.read_sql(load_query('monthly_active_users'), engine)
revenue = pd.read_sql(load_query('revenue_by_segment'), engine)
funnel = pd.read_sql(load_query('conversion_funnel'), engine)
```

## SQLite Compatibility Notes
- `strftime('%Y-%m', date_col)` replaces PostgreSQL `DATE_TRUNC('month', ...)::DATE`
- `date('now', '-12 months')` replaces PostgreSQL `NOW() - INTERVAL '12 months'`
- `CASE WHEN ... END` replaces PostgreSQL `FILTER (WHERE ...)` for maximum portability

## Validation Checks
1. Zero null values in MAU and Revenue DataFrames
2. All `monthly_revenue` values > 0
3. `conversion_pct` in [0, 100] range
4. `order_count > 0` for every revenue row
5. `signups >= first_purchase` (funnel ordering logic)
