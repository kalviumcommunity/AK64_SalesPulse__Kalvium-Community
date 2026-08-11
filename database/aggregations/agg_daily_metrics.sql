-- Table: agg_daily_metrics
-- Purpose: Pre-aggregated daily metrics summary for fast dashboard reads
-- Business metric: Daily revenue, order counts, average order value by product line
-- Refresh strategy: Full refresh daily (TRUNCATE + INSERT) - documented in refresh pipeline
-- Used by: Executive Dashboard, Operations Dashboard, Revenue Reporting
-- 
-- Columns:
--   aggregation_date  : Calendar date for this metric row
--   product_line      : Product category dimension for segmentation
--   total_revenue     : Sum of gross revenue for this date & product line
--   order_count       : Number of distinct orders
--   avg_order_value   : Average order amount
--   updated_at        : Timestamp when this row was computed - ALWAYS include for staleness detection

CREATE TABLE IF NOT EXISTS agg_daily_metrics (
    aggregation_date DATE NOT NULL,
    product_line VARCHAR(100) NOT NULL,
    total_revenue REAL NOT NULL DEFAULT 0,
    order_count INTEGER NOT NULL DEFAULT 0,
    avg_order_value REAL NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT (datetime('now'))
);

-- Populate agg_daily_metrics from base orders + products tables
INSERT INTO agg_daily_metrics
    (aggregation_date, product_line, total_revenue, order_count, avg_order_value, updated_at)
SELECT 
    date(o.order_date) AS aggregation_date,
    COALESCE(p.category, 'Uncategorized') AS product_line,
    ROUND(SUM(o.order_amount), 2) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(AVG(o.order_amount), 2) AS avg_order_value,
    datetime('now') AS updated_at
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY date(o.order_date), COALESCE(p.category, 'Uncategorized');
