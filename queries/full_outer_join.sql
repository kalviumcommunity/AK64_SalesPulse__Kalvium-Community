-- queries/full_outer_join.sql
-- Task 3: FULL OUTER JOIN - All records from both tables (with SQLite-compatible emulation fallback)
SELECT 
    c.customer_id, 
    c.customer_type, 
    o.order_id, 
    o.order_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
UNION ALL
SELECT 
    NULL AS customer_id, 
    NULL AS customer_type, 
    o.order_id, 
    o.order_amount
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
