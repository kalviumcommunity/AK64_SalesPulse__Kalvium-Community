-- queries/monthly_active_users.sql
-- Monthly Active Users (MAU): distinct customers with at least one transaction per month
-- Source Table: transactions JOIN customers
-- Compatible with: SQLite (strftime), PostgreSQL (DATE_TRUNC)
--
-- Metric Definition: One truth for MAU.
--   Active User = any customer_id appearing in transactions within the calendar month.
--   Segment breakdown added via CASE WHEN conditional aggregation.

SELECT
    strftime('%Y-%m', transaction_date) AS month,
    COUNT(DISTINCT t.customer_id)                                          AS active_users,
    COUNT(DISTINCT CASE WHEN c.customer_type = 'Enterprise'
                        THEN t.customer_id END)                            AS enterprise_users,
    COUNT(DISTINCT CASE WHEN c.customer_type = 'SMB'
                        THEN t.customer_id END)                            AS smb_users,
    COUNT(DISTINCT CASE WHEN c.customer_type = 'Startup'
                        THEN t.customer_id END)                            AS startup_users
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.transaction_date >= date('now', '-12 months')
GROUP BY strftime('%Y-%m', transaction_date)
ORDER BY month DESC;
