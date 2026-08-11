"""
SalesPulse Alert Configuration Module
-------------------------------------
Assignment 2.56 - Task 1 & Task 3: Centralized Threshold Configuration

Defines business alert limits, evaluation directions, severity tiers, and 
actionable plain-language risk descriptions.
"""

ALERT_THRESHOLDS = {
    "churn_rate": {
        "metric": "High Churn Risk Rate (%)",
        "threshold": 7.0,
        "direction": "above",  # Trigger when value > threshold
        "severity": "critical",
        "message": "Churn rate exceeds safe operating limit. Investigate customer retention and support delays immediately."
    },
    "avg_order_value": {
        "metric": "Average Order Value ($)",
        "threshold": 2500.0,
        "direction": "below",  # Trigger when value < threshold
        "severity": "warning",
        "message": "Average order value has dropped below operational target. Check pricing, discount usage, and product mix."
    },
    "null_percentage": {
        "metric": "Data Quality (Null %)",
        "threshold": 5.0,
        "direction": "above",  # Trigger when value > threshold
        "severity": "warning",
        "message": "Null percentage exceeds acceptable quality limits. Inspect upstream data ingestion pipelines for missing fields."
    }
}


def check_alerts(current_metrics, thresholds=ALERT_THRESHOLDS):
    """
    Evaluates computed current metrics against configured threshold limits.

    Args:
        current_metrics (dict): Dict of {metric_key: numeric_value}
        thresholds (dict): Threshold configuration dictionary

    Returns:
        list: List of triggered alert dicts containing metric details, values, severity, and messages
    """
    triggered_alerts = []

    for key, config in thresholds.items():
        if key not in current_metrics or current_metrics[key] is None:
            continue

        value = float(current_metrics[key])
        threshold = float(config["threshold"])
        direction = config["direction"]

        breached = False
        if direction == "above" and value > threshold:
            breached = True
        elif direction == "below" and value < threshold:
            breached = True

        if breached:
            triggered_alerts.append({
                "key": key,
                "metric": config["metric"],
                "value": round(value, 1),
                "threshold": threshold,
                "direction": direction,
                "severity": config["severity"],
                "message": config["message"]
            })

    return triggered_alerts
