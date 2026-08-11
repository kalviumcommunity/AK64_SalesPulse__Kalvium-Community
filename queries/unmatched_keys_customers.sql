-- queries/unmatched_keys_customers.sql
-- Task 2: Customers with NO orders
SELECT 
    c.customer_id, 
    c.customer_type, 
    c.signup_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
ORDER BY c.signup_date;
