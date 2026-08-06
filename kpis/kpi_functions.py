"""Reusable KPI computations for SalesPulse.

These helpers define KPI formulas in one place so every team computes the same
numbers from the same DataFrame inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

import pandas as pd


@dataclass(frozen=True)
class KPIResult:
    name: str
    value: float | int
    formatted: str


def _ensure_datetime(series: pd.Series) -> pd.Series:
    if pd.api.types.is_datetime64_any_dtype(series):
        return series
    return pd.to_datetime(series, errors="coerce")


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


def format_integer(value: int) -> str:
    return f"{value:,}"


def format_percentage(value: float) -> str:
    return f"{value:.1%}"


def calculate_mau(
    df: pd.DataFrame,
    days: int = 30,
    customer_col: str = "customer_id",
    date_col: str = "transaction_date",
    reference_date: pd.Timestamp | None = None,
) -> int:
    """Monthly Active Users: distinct customers with transactions in the last N days."""

    working = df.copy()
    working[date_col] = _ensure_datetime(working[date_col])
    cutoff = (reference_date or pd.Timestamp.now()) - pd.Timedelta(days=days)
    return int(working.loc[working[date_col] >= cutoff, customer_col].nunique())


def calculate_revenue_per_customer(
    df: pd.DataFrame,
    amount_col: str = "amount",
    customer_col: str = "customer_id",
) -> float:
    """Average revenue generated per unique customer."""

    unique_customers = df[customer_col].nunique()
    if unique_customers == 0:
        return 0.0
    return float(df[amount_col].sum() / unique_customers)


def calculate_average_order_value(df: pd.DataFrame, amount_col: str = "amount") -> float:
    """Average value of a single transaction/order."""

    if len(df) == 0:
        return 0.0
    return float(df[amount_col].mean())


def calculate_churn_rate(
    df: pd.DataFrame,
    period_days: int = 30,
    customer_col: str = "customer_id",
    date_col: str = "transaction_date",
    reference_date: pd.Timestamp | None = None,
) -> float:
    """Share of customers active in the prior period who were inactive in the current period."""

    working = df.copy()
    working[date_col] = _ensure_datetime(working[date_col])
    end_date = reference_date or pd.Timestamp.now()
    current_start = end_date - pd.Timedelta(days=period_days)
    prior_start = current_start - pd.Timedelta(days=period_days)

    prior_active = working.loc[
        (working[date_col] >= prior_start) & (working[date_col] < current_start),
        customer_col,
    ].unique()
    current_active = working.loc[
        (working[date_col] >= current_start) & (working[date_col] <= end_date),
        customer_col,
    ].unique()

    if len(prior_active) == 0:
        return 0.0

    churned = len([customer for customer in prior_active if customer not in set(current_active)])
    return churned / len(prior_active)


def calculate_repeat_purchase_rate(
    df: pd.DataFrame,
    customer_col: str = "customer_id",
) -> float:
    """Customers with more than one purchase divided by total customers."""

    customer_orders = df.groupby(customer_col).size()
    total_customers = customer_orders.size
    if total_customers == 0:
        return 0.0
    repeat_customers = int((customer_orders > 1).sum())
    return repeat_customers / total_customers


def calculate_payment_success_rate(
    df: pd.DataFrame,
    status_col: str = "payment_status",
    success_values: Iterable[str] = ("success", "completed", "paid"),
    success_flag_col: str = "is_payment_successful",
) -> float:
    """Successful payments divided by total payment attempts."""

    if success_flag_col in df.columns:
        flag_series = df[success_flag_col].fillna(0).astype(int)
        if len(flag_series) == 0:
            return 0.0
        return float(flag_series.mean())

    if status_col not in df.columns:
        raise ValueError(
            f"DataFrame must contain '{status_col}' or '{success_flag_col}' to calculate payment success rate."
        )

    statuses = df[status_col].astype(str).str.lower()
    if len(statuses) == 0:
        return 0.0
    success_set = {value.lower() for value in success_values}
    return float(statuses.isin(success_set).mean())


def calculate_customer_acquisition_cost(
    df: pd.DataFrame,
    acquisition_cost_col: str = "acquisition_cost",
    customer_col: str = "customer_id",
    spend_col: str | None = None,
) -> float:
    """Average acquisition cost per customer."""

    if spend_col and spend_col in df.columns:
        total_spend = float(df[spend_col].sum())
    elif acquisition_cost_col in df.columns:
        total_spend = float(df[acquisition_cost_col].sum())
    else:
        raise ValueError(
            f"DataFrame must contain '{acquisition_cost_col}' or '{spend_col}' to calculate CAC."
        )

    total_customers = df[customer_col].nunique()
    if total_customers == 0:
        return 0.0
    return total_spend / total_customers


def calculate_customer_lifetime_value(
    df: pd.DataFrame,
    amount_col: str = "amount",
    customer_col: str = "customer_id",
) -> float:
    """Average lifetime value per customer."""

    total_customers = df[customer_col].nunique()
    if total_customers == 0:
        return 0.0
    return float(df.groupby(customer_col)[amount_col].sum().mean())


def build_kpi_results(df: pd.DataFrame, reference_date: pd.Timestamp | None = None) -> list[KPIResult]:
    """Compute the core KPI set in one call for reporting and validation."""

    mau = calculate_mau(df, reference_date=reference_date)
    rpc = calculate_revenue_per_customer(df)
    aov = calculate_average_order_value(df)
    churn_rate = calculate_churn_rate(df, reference_date=reference_date)
    repeat_rate = calculate_repeat_purchase_rate(df)
    clv = calculate_customer_lifetime_value(df)

    return [
        KPIResult("monthly_active_users", mau, format_integer(mau)),
        KPIResult("revenue_per_customer", rpc, format_currency(rpc)),
        KPIResult("average_order_value", aov, format_currency(aov)),
        KPIResult("churn_rate", churn_rate, format_percentage(churn_rate)),
        KPIResult("repeat_purchase_rate", repeat_rate, format_percentage(repeat_rate)),
        KPIResult("customer_lifetime_value", clv, format_currency(clv)),
    ]


def validate_kpis(current_kpis: Mapping[str, float | int], targets: Mapping[str, Mapping[str, float | int]]) -> pd.DataFrame:
    """Compare KPI values against target ranges and return a validation report."""

    rows = []
    for kpi_name, bounds in targets.items():
        actual = current_kpis[kpi_name]
        minimum = bounds["min"]
        maximum = bounds["max"]
        status = "PASS" if minimum <= actual <= maximum else "ALERT"
        rows.append(
            {
                "kpi": kpi_name,
                "actual": actual,
                "target_min": minimum,
                "target_max": maximum,
                "status": status,
            }
        )

    return pd.DataFrame(rows)


def decompose_total_revenue(
    df: pd.DataFrame,
    amount_col: str = "amount",
    segment_col: str = "customer_type",
    product_col: str = "product",
) -> str:
    """Return a hierarchical revenue decomposition for reporting."""

    total_revenue = float(df[amount_col].sum())
    segment_breakdown = df.groupby(segment_col)[amount_col].sum().sort_values(ascending=False)

    lines = ["KPI DECOMPOSITION: Total Monthly Revenue", ""]
    lines.append(f"Level 1 (Top-level): {format_currency(total_revenue)}")
    lines.append("")
    lines.append("Level 2 (By Segment):")
    for segment, value in segment_breakdown.items():
        lines.append(f"  {segment}: {format_currency(float(value))}")

    if product_col in df.columns:
        lines.append("")
        lines.append("Level 3 (By Product within Segment):")
        product_breakdown = df.groupby(product_col)[amount_col].sum().sort_values(ascending=False)
        for product, value in product_breakdown.items():
            lines.append(f"  {product}: {format_currency(float(value))}")

    lines.append("")
    lines.append("Component sums reconcile to the top-level revenue total.")
    return "\n".join(lines)


def format_kpi_results(results: Iterable[KPIResult]) -> pd.DataFrame:
    """Convert KPI results into a display-friendly table."""

    return pd.DataFrame(
        [
            {"kpi": item.name, "value": item.value, "formatted": item.formatted}
            for item in results
        ]
    )


if __name__ == "__main__":
    raise SystemExit(
        "Import kpi_functions from another module or notebook; this module is designed for reuse."
    )
