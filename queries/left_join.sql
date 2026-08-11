-- queries/left_join.sql
-- Task 3: LEFT JOIN - All left records + matched right records
SELECT 
    c.customer_id, 
    c.customer_type, 
    o.order_id, 
    o.order_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
