
================================================================================
SALESPULSE JOIN STRATEGY & LINEAGE DOCUMENTATION
================================================================================

TABLE SCHEMAS & CARDINALITY:
  1. customers   : 1,000 rows (PK: customer_id)
  2. orders      : 5,000 rows (PK: order_id, FK: customer_id)
  3. order_items : ~8,000 rows (PK: item_id, FK: order_id, FK: product_id)
  4. products    : 50 rows (PK: product_id)

DECISION 1: customers LEFT JOIN orders
  - Purpose       : Retain complete customer directory including inactive accounts.
  - Row Count     : 1,000 customers -> 5054 joined rows (1-to-many relationship).
  - Unmatched Keys: 104 customers with 0 orders (10.4%).
  - Business Use  : Customer Lifetime Value (LTV), cohort retention, inactive churn analysis.

DECISION 2: orders LEFT JOIN order_items
  - Purpose       : Extract line-item detail per order for product-level metrics.
  - Row Count     : 5,000 orders -> ~8,000 line item rows.
  - Multiplication: Average 1.6 line items per order.
  - Business Use  : Product sales volume, basket size analysis, revenue by product.

DECISION 3: Full 4-Table Join (customers + orders + order_items + products)
  - Purpose       : Unified operational reporting for Enterprise segment performance.
  - Row Count     : Filtered to Enterprise segment.
  - Risk & Remedy : Avoid summing raw join outputs directly without aggregation.
  - Validation    : Asserted line item total sum matches raw order_items table ($ total verified).

UNMATCHED KEY AUDIT:
  - Inactive Customers (0 orders) : 104 records (Retained in LEFT JOIN).
  - Orphaned Orders (no customer): 50 records (Retained in FULL OUTER JOIN; excluded in INNER/LEFT).

CONCLUSION:
  - Join lineage verified. All row transformations match theoretical expectations.
================================================================================
