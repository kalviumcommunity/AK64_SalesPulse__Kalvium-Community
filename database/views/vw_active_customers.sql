-- View: vw_active_customers
-- Purpose: Identify customers with recent order activity (last 30 days rolling window)
-- Business metric: Active customers, 30-day revenue, order frequency, recency (days since last order)
-- Updated: Automatically with each query (view recalculates fresh against base tables)
-- Used by: Customer Retention Dashboard, Sales Operations, Account Managers
-- 
-- Columns:
--   customer_id      : Unique customer primary key
--   customer_name    : Display name of the customer
--   segment          : Customer tier classification (Enterprise, Mid-Market, SMB, Starter)
--   order_count_30d  : Number of orders completed in the last 30 days
--   revenue_30d      : Total spending in the last 30 days
--   last_order_date  : Timestamp of the most recent completed order
--   days_since_order : Days elapsed between current date and last order date

CREATE VIEW IF NOT EXISTS vw_active_customers AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    COUNT(DISTINCT o.order_id) AS order_count_30d,
    ROUND(COALESCE(SUM(o.order_amount), 0), 2) AS revenue_30d,
    MAX(o.order_date) AS last_order_date,
    CAST(julianday('now') - julianday(MAX(o.order_date)) AS INTEGER) AS days_since_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
    AND o.order_date >= date('now', '-30 days')
WHERE c.deleted_at IS NULL
GROUP BY c.customer_id, c.customer_name, c.segment;
