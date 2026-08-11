-- queries/where_having_combined.sql
-- Task 4: WHERE + HAVING Combined - data quality AND business thresholds together
-- Purpose: Demonstrate the two-stage filter pipeline in a single production query.
--
-- Stage 1 (WHERE) - Data quality gate:
--   transaction_date in scope     -> fiscal year data only
--   transaction_status=completed  -> real revenue, not pending/failed
--   amount > 0                    -> exclude refunds and test charges
--
-- Stage 2 (HAVING) - Business rule gate (applied to aggregated groups):
--   COUNT(DISTINCT customer_id) >= 10  -> segment must have meaningful size
--   SUM(amount) > 50000                -> segment must meet revenue materiality threshold
--
-- QUERY EXECUTION ORDER: FROM -> JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY

SELECT
    c.customer_type,
    COUNT(DISTINCT t.customer_id)            AS segment_customers,
    COUNT(*)                                 AS total_transactions,
    ROUND(SUM(t.amount), 2)                  AS segment_revenue,
    ROUND(AVG(t.amount), 2)                  AS avg_order_value,
    ROUND(SUM(t.amount) / COUNT(DISTINCT t.customer_id), 2) AS revenue_per_customer
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.transaction_date >= '2025-01-01'         -- WHERE: fiscal year scope
  AND t.transaction_status = 'completed'         -- WHERE: settled records only
  AND t.amount > 0                               -- WHERE: no refunds or zero charges
GROUP BY c.customer_type
HAVING COUNT(DISTINCT t.customer_id) >= 10       -- HAVING: minimum segment size
  AND SUM(t.amount) > 50000                      -- HAVING: revenue materiality threshold
ORDER BY segment_revenue DESC;
