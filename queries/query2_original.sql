-- queries/query2_original.sql
-- Task 2: Inefficient Query 2 - Joins 3 full tables BEFORE applying WHERE filters
SELECT 
    t.transaction_id, 
    t.amount, 
    c.customer_name, 
    p.product_name
FROM transactions t
JOIN customers c ON t.customer_id = c.id
JOIN products p ON t.product_id = p.id
WHERE t.transaction_date >= '2024-01-01'
  AND t.amount > 100
  AND c.country = 'USA'
LIMIT 5000;
