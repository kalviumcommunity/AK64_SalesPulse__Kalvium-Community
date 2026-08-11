# SalesPulse SQL Environment & Database Integration

## Overview
This document outlines the architecture, database integration patterns, and schema validation standards used to establish a single, reproducible source of truth for SalesPulse analytics data.

## 1. SQLite vs. PostgreSQL Architectural Comparison
| Dimension | SQLite | PostgreSQL |
|---|---|---|
| **Architecture** | File-based, zero setup | Client-server daemon architecture |
| **Concurrency** | Single-writer file lock | Multi-user MVCC concurrent writers |
| **Scale Limit** | Ideal for datasets < 1-2 GB | Scalable to terabytes / enterprise clusters |
| **Use Case in SalesPulse** | Local analytics, development & CI testing | Production reporting & data warehouse integration |

## 2. SQLAlchemy Abstraction Layer
Using `sqlalchemy.create_engine()` allows SalesPulse analytics scripts to remain engine-agnostic:
- Development: `create_engine('sqlite:///analytics.db')`
- Production: `create_engine('postgresql://user:password@localhost:5432/salespulse_db')`

## 3. Pandas Integration Patterns
- **Writing Data**: `df.to_sql(table_name, engine, if_exists='replace', index=False)`
- **Reading Data**: `pd.read_sql(sql_query, engine)`

## 4. Schema Validation & Audit Checklist
1. **Inspection**: Use `sqlalchemy.inspect(engine).get_columns(table_name)` to audit schema definitions.
2. **Type Checking**: Verify SQL data types (`INTEGER`, `TEXT`, `FLOAT`, `DATE`) match Pandas DataFrame dtypes.
3. **Nullability Checks**: Verify non-nullable primary keys and mandatory foreign key attributes.
4. **Repeatable Pipelines**: Encapsulate ingestion logic inside reusable helper functions to prevent data fragmentation across notebooks.
