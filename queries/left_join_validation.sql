-- queries/left_join_validation.sql
-- Task 1: LEFT JOIN with Row Count Validation
-- Purpose: Get all customers with their aggregated order counts and total spending.
-- Note: Customers with no orders return order_count = 0 and total_spent = NULL (or 0).

SELECT 
    c.customer_id,
    c.customer_type,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(COALESCE(SUM(o.order_amount), 0), 2) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_type
ORDER BY total_spent DESC;
