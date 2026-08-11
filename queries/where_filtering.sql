-- queries/where_filtering.sql
-- Task 1: WHERE Filtering - filter rows BEFORE grouping
-- Purpose: Apply data quality rules before any aggregation takes place.
--
-- Rule 1: transaction_date >= '2025-01-01'  -> limit to current fiscal year only
-- Rule 2: amount > 0                        -> exclude refunds, credits, and $0 test rows
-- Rule 3: transaction_status = 'completed'  -> include only settled, valid transactions
--
-- WHY: These conditions check data quality.
-- If a transaction has amount <= 0 or is 'pending'/'failed', it is NOT valid revenue.
-- WHERE excludes these rows entirely before any GROUP BY runs.

SELECT
    t.customer_id,
    ROUND(SUM(t.amount), 2)     AS annual_revenue,
    COUNT(*)                    AS transaction_count,
    ROUND(AVG(t.amount), 2)     AS avg_transaction_value,
    MIN(t.transaction_date)     AS first_transaction,
    MAX(t.transaction_date)     AS last_transaction
FROM transactions t
WHERE t.transaction_date >= '2025-01-01'      -- Data quality: fiscal year scope
  AND t.amount > 0                            -- Data quality: remove refunds/zero rows
  AND t.transaction_status = 'completed'      -- Data quality: valid settled records only
GROUP BY t.customer_id
ORDER BY annual_revenue DESC;
