-- queries/group_by_aggregation.sql
-- Task 2: GROUP BY on 2+ dimensions with 3+ aggregate functions
-- Purpose: Slice revenue across customer segment AND calendar month simultaneously.
--
-- WHERE fires FIRST (filters invalid rows), THEN GROUP BY runs on the remaining rows.
-- This means bad data is excluded before the aggregation math is done.
--
-- Aggregates used:
--   COUNT(DISTINCT t.customer_id) - unique active customers per cell
--   COUNT(*)                      - total transaction volume per cell
--   SUM(t.amount)                 - total revenue per cell
--   AVG(t.amount)                 - average ticket size per cell

SELECT
    c.customer_type,
    strftime('%Y-%m', t.transaction_date)          AS month,
    COUNT(DISTINCT t.customer_id)                  AS unique_customers,
    COUNT(*)                                       AS transaction_count,
    ROUND(SUM(t.amount), 2)                        AS monthly_revenue,
    ROUND(AVG(t.amount), 2)                        AS avg_transaction,
    ROUND(SUM(t.amount) / COUNT(DISTINCT t.customer_id), 2) AS revenue_per_customer
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.transaction_date >= '2025-01-01'           -- WHERE filters before GROUP BY
  AND t.amount > 0
  AND t.transaction_status = 'completed'
GROUP BY c.customer_type, strftime('%Y-%m', t.transaction_date)  -- 2 dimensions
ORDER BY month DESC, monthly_revenue DESC;
