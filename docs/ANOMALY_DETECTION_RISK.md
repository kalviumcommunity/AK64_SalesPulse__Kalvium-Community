# SalesPulse Anomaly Detection & Risk Identification System

## Overview
This document specifies the technical architecture and operational procedures for the continuous KPI anomaly detection and risk monitoring engine in SalesPulse.

## 1. Detection Methodologies
- **Threshold-Based Alerts**: Static business min/max boundaries applied to real-time daily metrics (`daily_revenue`: $5k-$50k, `transaction_count`: 100-10,000, `signup_rate`: 10-500). Useful for fixed SLA contracts and hard business constraints.
- **Statistical Z-Score Monitoring**: Dynamic rolling mean and standard deviation computation ($Z = \frac{X - \mu}{\sigma}$). Flagged when $|Z| > 2.0$. Adaptive to seasonality and trend growth.

## 2. Severity Classification Matrix
| Severity Level | Z-Score Range | Response Action | Escalation SLA |
|---|---|---|---|
| **CRITICAL** | $|Z| > 3.0$ | Immediate pager incident & engineering audit | < 15 minutes |
| **HIGH** | $2.0 < |Z| \le 3.0$ | Automated Slack alert to data analyst team | < 1 hour |
| **MEDIUM** | $1.5 < |Z| \le 2.0$ | Flagged in daily digest report | < 24 hours |
| **LOW** | $|Z| \le 1.5$ | Normal operational variance | No action |

## 3. False Positive Mitigation Strategies
1. **Rolling Baseline Windows**: Use 30-day moving windows to automatically adjust to secular revenue growth.
2. **Multi-Metric Corroboration**: Trigger high-priority alerts only when revenue drops coincide with transaction count drop or error log spikes.
3. **Exclusion of Known Holidays**: Suppress non-critical alerts on planned company holidays and weekend cycles.

## 4. Audit Log Schema
The system persists anomaly records to `anomalies_log.csv` with fields:
- `timestamp`: Audit recording execution time
- `anomaly_date`: Target date of anomaly occurrence
- `metric`: KPI metric monitored
- `value`: Recorded actual value
- `expected_range`: Shaded expected $\pm 2\sigma$ band
- `z_score`: Standardized distance score
- `severity`: Classification (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`)
- `status`: Workflow status (`OPEN`, `INVESTIGATED`, `RESOLVED`)
