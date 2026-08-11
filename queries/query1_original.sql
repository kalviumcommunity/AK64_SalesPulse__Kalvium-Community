-- queries/query1_original.sql
-- Task 1: Inefficient Query 1 using SELECT * (Antipattern)
SELECT *
FROM transactions t
JOIN customers c ON t.customer_id = c.id
WHERE t.transaction_date >= '2024-01-01'
LIMIT 1000;
