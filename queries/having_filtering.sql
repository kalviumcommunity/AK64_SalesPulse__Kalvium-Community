-- queries/having_filtering.sql
-- Task 3: HAVING - filter GROUPS after aggregation
-- Purpose: Find high-value, high-frequency customers only.
--
-- HAVING vs WHERE:
--   WHERE filters individual rows BEFORE any grouping.
--   HAVING filters the resulting GROUPS after aggregation is computed.
--
-- Business question answered here:
--   "Which customers have both significant total spend (>$5,000 annual)
--    AND meaningful engagement (5+ purchases)?"
--
-- You cannot answer this with WHERE because SUM(amount) and COUNT(*)
-- don't exist yet when WHERE runs — they are created by GROUP BY.

SELECT
    t.customer_id,
    COUNT(*)                        AS transaction_count,
    ROUND(SUM(t.amount), 2)         AS annual_revenue,
    ROUND(AVG(t.amount), 2)         AS avg_order_value,
    MIN(t.transaction_date)         AS first_purchase,
    MAX(t.transaction_date)         AS last_purchase
FROM transactions t
WHERE t.transaction_date >= '2025-01-01'     -- WHERE: valid date range (row filter)
  AND t.amount > 0                           -- WHERE: valid amounts (row filter)
  AND t.transaction_status = 'completed'     -- WHERE: completed only (row filter)
GROUP BY t.customer_id
HAVING SUM(t.amount) > 5000                 -- HAVING: annual spend threshold (group filter)
  AND COUNT(*) >= 5                         -- HAVING: engagement minimum (group filter)
ORDER BY annual_revenue DESC;
