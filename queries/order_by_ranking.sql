-- queries/order_by_ranking.sql
-- Task 5: ORDER BY Ranking with RANK() window function
-- Purpose: Surface top-performing customer segments by revenue.
--
-- RANK() OVER (ORDER BY SUM(t.amount) DESC):
--   Window function applied AFTER GROUP BY.
--   Ranks each (customer_type, industry) group by its total revenue.
--   Ties receive the same rank; next rank skips (e.g., 1,2,2,4).
--   Does NOT require GROUP BY to include the RANK column.
--
-- Business question: "Which customer segment + industry combinations
--   drive the most revenue? Show top 20."

SELECT
    c.customer_type,
    c.industry,
    COUNT(DISTINCT t.customer_id)                              AS customers,
    COUNT(*)                                                   AS total_transactions,
    ROUND(SUM(t.amount), 2)                                    AS total_revenue,
    ROUND(AVG(t.amount), 2)                                    AS avg_order,
    ROUND(SUM(t.amount) / COUNT(DISTINCT t.customer_id), 2)    AS revenue_per_customer,
    RANK() OVER (ORDER BY SUM(t.amount) DESC)                  AS revenue_rank
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.transaction_date >= '2025-01-01'
  AND t.amount > 0
  AND t.transaction_status = 'completed'
GROUP BY c.customer_type, c.industry
HAVING COUNT(DISTINCT t.customer_id) >= 3
ORDER BY total_revenue DESC
LIMIT 20;
