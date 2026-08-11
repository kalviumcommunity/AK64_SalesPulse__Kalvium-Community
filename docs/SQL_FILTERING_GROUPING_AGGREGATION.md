# SalesPulse SQL Filtering, Grouping & Aggregation

## Core Concept: SQL Query Execution Order

```
FROM -> JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```

This order determines which clauses can reference aggregated values and which cannot.

## WHERE vs HAVING Decision Guide

| Question | Clause | Reason |
|---|---|---|
| Is this a data quality check? | WHERE | Runs before aggregation — removes bad rows |
| Does this reference SUM/COUNT/AVG? | HAVING | Runs after aggregation — filters groups |
| Am I filtering raw row values? | WHERE | No aggregation needed |
| Am I filtering a grouped metric? | HAVING | Requires GROUP BY to exist first |

## Query Files

| File | Task | Key Technique |
|---|---|---|
| `queries/where_filtering.sql` | Task 1 | WHERE with 3 conditions: date, amount, status |
| `queries/group_by_aggregation.sql` | Task 2 | GROUP BY 2 dimensions + 5 aggregate functions |
| `queries/having_filtering.sql` | Task 3 | HAVING SUM + COUNT thresholds after grouping |
| `queries/where_having_combined.sql` | Task 4 | WHERE data gate + HAVING business gate |
| `queries/order_by_ranking.sql` | Task 5 | RANK() window function + ORDER BY + LIMIT 20 |

## Performance Note

WHERE filters run before GROUP BY and are significantly faster than HAVING because:
- They reduce the row set that GROUP BY must process
- Indexes can be used on WHERE columns
- HAVING cannot use indexes — it operates on computed aggregates

Always push conditions into WHERE when they reference raw column values.

## RANK() Window Function

```sql
RANK() OVER (ORDER BY SUM(t.amount) DESC) AS revenue_rank
```

- Applied after GROUP BY, before ORDER BY
- Ties receive the same rank; next rank skips
- Does NOT reduce row count unlike HAVING
