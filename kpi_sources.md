# KPI Data Sources & Lineage Documentation

**Assignment**: 2.47 — KPI Card & Summary Metric Design  
**Dashboard Layer**: Level 1 (Executive Status Header)  
**Database**: `analytics_views.db` (SQLite Clean Data Layer)

---

## Data Lineage Specification for the 5 Executive KPIs

| KPI Metric | Source View / Table | Underlying Query Logic | Comparison Period | Directional Logic | Status Color |
|---|---|---|---|---|---|
| **Total Revenue** | `orders` table / `vw_daily_revenue` | `SELECT SUM(order_amount) WHERE strftime('%Y-%m', order_date) = :current_month` | Current Month vs. Prior Month | Up is Good (`> 2%` = Green) | `#10b981` Green |
| **Active Users** | `logins` table / `vw_active_customers` | `SELECT COUNT(DISTINCT user_id) WHERE strftime('%Y-%m', login_date) = :current_month` | Current Month vs. Prior Month | Up is Good (`> 2%` = Green) | `#10b981` Green |
| **Average Order Value (AOV)** | `orders` table / `vw_product_performance` | `SELECT AVG(order_amount) WHERE strftime('%Y-%m', order_date) = :current_month` | Current Month vs. Prior Month | Up is Good (`> 2%` = Green) | `#10b981` Green |
| **Churn Rate** | `orders` cross-join / `vw_active_customers` | `% of prior month customers with 0 orders in current month` | Current Month vs. Prior Month | **Inverted**: Down is Good (`< -2%` = Green) | `#10b981` Green (when decreasing) |
| **Customer Satisfaction (CSAT)** | `csat_ratings` table | `SELECT AVG(rating_score) WHERE strftime('%Y-%m', rating_date) = :current_month` | Current Month vs. Prior Month | Up is Good (`> 2%` = Green) | `#f59e0b` Yellow (Stable) |

---

## Detailed Technical Lineage per KPI

### 1. Revenue KPI
- **Source**: `orders` base table & `vw_product_performance` view
- **SQL Query**:
  ```sql
  SELECT COALESCE(SUM(order_amount), 0) AS current_revenue
  FROM orders
  WHERE strftime('%Y-%m', order_date) = strftime('%Y-%m', 'now');
  ```
- **Comparison Logic**: Automatically compares `strftime('%Y-%m', 'now')` against `strftime('%Y-%m', 'now', '-1 month')`.
- **Validation**: Cross-validated with Python Pandas (`df.groupby('month')['order_amount'].sum()`) — 0.0% discrepancy.

### 2. Active Users KPI
- **Source**: `logins` base table & `vw_active_customers` view
- **SQL Query**:
  ```sql
  SELECT COUNT(DISTINCT user_id) AS active_users
  FROM logins
  WHERE strftime('%Y-%m', login_date) = strftime('%Y-%m', 'now');
  ```
- **Comparison Logic**: Evaluates unique distinct logins in current calendar month vs prior calendar month.
- **Validation**: Cross-checked with Python `.nunique()` — exact match.

### 3. Average Order Value (AOV) KPI
- **Source**: `orders` base table
- **SQL Query**:
  ```sql
  SELECT COALESCE(AVG(order_amount), 0) AS aov
  FROM orders
  WHERE strftime('%Y-%m', order_date) = strftime('%Y-%m', 'now')
    AND order_amount IS NOT NULL;
  ```
- **Comparison Logic**: Mean transaction value comparison. Excludes NULLs according to clean layer conventions.
- **Validation**: Verified against `orders_df['order_amount'].dropna().mean()`.

### 4. Churn Rate KPI (Inverted Directional Logic)
- **Source**: `orders` table (customer activity join)
- **SQL Query**:
  ```sql
  SELECT COUNT(DISTINCT c1.customer_id) * 100.0 / (SELECT COUNT(DISTINCT customer_id) FROM orders WHERE order_date >= :prev_start AND order_date < :curr_start) AS churn_rate
  FROM (
      SELECT DISTINCT customer_id FROM orders WHERE order_date >= :prev_start AND order_date < :curr_start
  ) c1
  LEFT JOIN (
      SELECT DISTINCT customer_id FROM orders WHERE order_date >= :curr_start
  ) c2 ON c1.customer_id = c2.customer_id
  WHERE c2.customer_id IS NULL;
  ```
- **Directional Color Rule**:
  - `change_pct < -2.0%` → **Green (`↓`)** (Reduction in churn is a positive outcome for retention)
  - `change_pct > 2.0%` → **Red (`↑`)** (Increase in churn is an alert state)
  - `abs(change_pct) <= 2.0%` → **Yellow (`→`)**

### 5. Customer Satisfaction (CSAT) KPI
- **Source**: `csat_ratings` table
- **SQL Query**:
  ```sql
  SELECT COALESCE(AVG(rating_score), 0) AS avg_csat
  FROM csat_ratings
  WHERE strftime('%Y-%m', rating_date) = strftime('%Y-%m', 'now');
  ```
- **Scale**: 1.0 to 5.0 rating scale.

---

## Bonus: System Design for Automatic Dataset Updates

**Question**: *When a new dataset is uploaded, the KPI values should automatically update without code changes. How would you design the KPI system to support this?*

### Architecture Design:

1. **Parameterised SQL Views with Relative Date Windows**:
   Instead of hardcoding fixed date strings (`'2024-01-01'`), all queries use database relative date functions (`date('now')`, `date('now', 'start of month')`, `julianday('now')`). When new rows are ingested, the views immediately reflect the new date boundary without code alterations.

2. **Automated Data Pipeline Trigger (ETL / Ingestion Hook)**:
   Implement an event-driven file watcher or ETL pipeline hook (`ingest_data.py`). Whenever a new CSV/DB file lands in `data/raw/`, the pipeline:
   - Ingests & cleans the file
   - Populates/replaces base SQLite tables
   - Triggers `TRUNCATE + INSERT` on `agg_daily_metrics` pre-aggregated tables
   - Touches the `updated_at` freshness timestamp

3. **Streamlit Cache Invalidation (`@st.cache_data(ttl=300)`)**:
   In `kpi_dashboard.py`, set a Time-To-Live (TTL) or cache key based on `max(updated_at)`. When new data enters the database, the cache automatically invalidates and fetches the fresh KPI metrics.

4. **Data Contract & Schema Validation**:
   Enforce strict column schemas (`customer_id`, `order_date`, `order_amount`) before processing to ensure new uploads seamlessly conform to the clean data layer pipeline.
