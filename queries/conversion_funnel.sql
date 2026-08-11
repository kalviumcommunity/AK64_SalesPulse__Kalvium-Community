-- queries/conversion_funnel.sql
-- Daily Conversion Funnel: Signup -> Email Verified -> First Purchase
-- Source Table: users
-- Compatible with: SQLite, PostgreSQL
--
-- Metric Definition: One truth for daily conversion rate.
--   conversion_pct = (first_purchase count / total signups) * 100
--   Conditional counting via CASE WHEN (portable across SQLite & PG).

SELECT
    date(u.created_at)                                         AS signup_date,
    COUNT(*)                                                   AS signups,
    COUNT(CASE WHEN u.email_verified_at IS NOT NULL THEN 1 END) AS email_verified,
    COUNT(CASE WHEN u.first_purchase_at IS NOT NULL THEN 1 END) AS first_purchase,
    ROUND(
        100.0
        * COUNT(CASE WHEN u.first_purchase_at IS NOT NULL THEN 1 END)
        / COUNT(*),
        1
    )                                                          AS conversion_pct
FROM users u
WHERE u.created_at >= date('now', '-90 days')
GROUP BY date(u.created_at)
ORDER BY signup_date DESC;
