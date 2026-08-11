-- queries/query1_optimized.sql
-- Task 1: Refactored Query 1 with explicit column selection
-- Business purpose: Analyze high-level customer transaction amounts by country & account type for 2024+.
-- Selected columns:
--   t.transaction_id   -> Unique primary key for transaction identification
--   t.transaction_date -> Date timestamp for temporal filtering and grouping
--   t.amount           -> Revenue metric for financial aggregation
--   c.customer_name    -> Entity identification for reporting
--   c.country          -> Geographic dimension for segment reporting
--   c.account_type     -> Customer classification tier

SELECT 
    t.transaction_id,
    t.transaction_date,
    t.amount,
    t.customer_id,
    c.customer_name,
    c.country,
    c.account_type
FROM transactions t
JOIN customers c ON t.customer_id = c.id
WHERE t.transaction_date >= '2024-01-01'
LIMIT 1000;
