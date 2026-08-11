-- queries/query3_original.sql
-- Task 3: Inefficient Query 3 - 3-level nested subqueries (hard to read and optimize)
SELECT customer_segment, revenue_per_transaction AS avg_transaction_value
FROM (
    SELECT 
        c.customer_segment,
        ROUND(AVG(t.amount), 2) AS revenue_per_transaction,
        COUNT(DISTINCT t.transaction_id) AS transaction_count
    FROM (
        SELECT t.transaction_id, t.amount, t.customer_id
        FROM transactions t
        WHERE t.transaction_date >= '2024-01-01'
    ) t
    JOIN customers c ON t.customer_id = c.id
    GROUP BY c.customer_segment
) grouped
ORDER BY avg_transaction_value DESC;
