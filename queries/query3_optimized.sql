-- queries/query3_optimized.sql
-- Task 3: Refactored Query 3 using CTEs for readability, testability, and clear execution steps
-- Step 1: recent_transactions - Filter raw transactions to date scope
-- Step 2: customer_with_segment - Join filtered transactions with customer segment details
-- Step 3: segment_metrics - Compute aggregate metrics per segment
-- Final Step: Select ordered metrics

WITH recent_transactions AS (
    -- Step 1: Filter to recent data
    SELECT transaction_id, amount, customer_id
    FROM transactions
    WHERE transaction_date >= '2024-01-01'
),
customer_with_segment AS (
    -- Step 2: Join to customer data
    SELECT 
        rt.transaction_id,
        rt.amount,
        c.customer_segment
    FROM recent_transactions rt
    JOIN customers c ON rt.customer_id = c.id
),
segment_metrics AS (
    -- Step 3: Calculate segment-level metrics
    SELECT 
        customer_segment,
        COUNT(DISTINCT transaction_id) AS transaction_count,
        ROUND(AVG(amount), 2) AS avg_transaction_value,
        ROUND(SUM(amount), 2) AS total_revenue
    FROM customer_with_segment
    GROUP BY customer_segment
)
SELECT 
    customer_segment,
    avg_transaction_value,
    transaction_count,
    total_revenue
FROM segment_metrics
ORDER BY avg_transaction_value DESC;
