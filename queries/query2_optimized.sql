-- queries/query2_optimized.sql
-- Task 2: Refactored Query 2 - Apply WHERE filters BEFORE JOINs using CTE
-- Optimization Strategy: Reduce transaction dataset first (amount > 100 AND date >= '2024-01-01')
-- so the database joins a tiny fraction of total rows.

WITH filtered_trans AS (
    SELECT transaction_id, customer_id, product_id, amount, transaction_date
    FROM transactions
    WHERE transaction_date >= '2024-01-01'
      AND amount > 100
)
SELECT 
    ft.transaction_id, 
    ft.amount, 
    c.customer_name, 
    p.product_name
FROM filtered_trans ft
JOIN customers c ON ft.customer_id = c.id
JOIN products p ON ft.product_id = p.id
WHERE c.country = 'USA'
LIMIT 5000;
