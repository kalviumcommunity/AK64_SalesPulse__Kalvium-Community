"""Funnel Analysis & Drop-Off Detection pipeline.

This script reproduces the assignment funnel using the provided stage counts,
computes drop-off rates, estimates business impact, and exports a chart plus
text report into the output directory.
"""

from collections import OrderedDict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"


def build_funnel_stages() -> OrderedDict:
    """Return the ordered signup funnel used in the assignment."""

    return OrderedDict(
        [
            ("Sign Up", 10_000),
            ("Email Entered", 8_000),
            ("Password Created", 6_000),
            ("Email Verified", 5_000),
            ("Payment Added", 4_000),
            ("First Purchase", 2_000),
        ]
    )


def compute_funnel_metrics(stages: OrderedDict, revenue_per_customer: int = 100):
    stage_names = list(stages.keys())
    stage_values = list(stages.values())

    drop_rows = []
    for index in range(len(stage_values) - 1):
        users_before = stage_values[index]
        users_after = stage_values[index + 1]
        users_lost = users_before - users_after
        completion_rate = (users_after / users_before) * 100
        drop_rate = (users_lost / users_before) * 100

        drop_rows.append(
            {
                "from_stage": stage_names[index],
                "to_stage": stage_names[index + 1],
                "users_before": users_before,
                "users_after": users_after,
                "users_lost": users_lost,
                "completion_rate": round(completion_rate, 1),
                "drop_rate": round(drop_rate, 1),
                "revenue_impact": users_lost * revenue_per_customer,
            }
        )

    funnel_df = pd.DataFrame(drop_rows)
    impact_df = funnel_df.copy()
    impact_df["priority"] = impact_df["revenue_impact"].apply(
        lambda value: "HIGH" if value > 100_000 else "MEDIUM"
    )

    biggest_drop = (
        funnel_df.sort_values(
            by=["revenue_impact", "drop_rate", "users_lost"],
            ascending=[False, False, False],
        ).iloc[0]
    )
    return funnel_df, impact_df, biggest_drop


def save_funnel_chart(stages: OrderedDict, output_path: Path):
    """Save a bar chart for the funnel stage volumes."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899"]
    ax.bar(list(stages.keys()), list(stages.values()), color=colors)
    ax.set_ylabel("Users", fontsize=12)
    ax.set_xlabel("Stage", fontsize=12)
    ax.set_title("Signup Funnel: Volume by Stage", fontsize=14)
    ax.set_ylim(0, max(stages.values()) * 1.15)

    for stage, count in stages.items():
        ax.text(stage, count, f"{count:,}", ha="center", va="bottom", fontweight="bold")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close(fig)


def build_recommendation(biggest_drop: pd.Series, revenue_per_customer: int = 100) -> str:
    additional_conversions = int(biggest_drop["users_lost"] * 0.10)
    additional_revenue = additional_conversions * revenue_per_customer

    return f"""FUNNEL OPTIMIZATION PRIORITY

CRITICAL BOTTLENECK:
Stage: {biggest_drop['from_stage']} → {biggest_drop['to_stage']}
Users Lost: {biggest_drop['users_lost']:,.0f}
Completion Rate: {biggest_drop['completion_rate']:.1f}%
Drop Rate: {biggest_drop['drop_rate']:.1f}%
Revenue Impact: ${biggest_drop['revenue_impact']:,.0f}

ROOT CAUSE HYPOTHESES:
- The step may be too complex or too long.
- The step may be unclear, with weak guidance or messaging.
- The step may require too much trust too early in the journey.
- The step may suffer from technical friction or form errors.

RECOMMENDED ACTION:
1. A/B test a simplified version of the step.
2. Reduce the number of fields or required actions.
3. Add clearer copy, progress cues, and reassurance.
4. Track the drop rate before and after the change.

BUSINESS VALUE OF FIXING THE LEAK:
If completion improves by 10%, additional conversions = {additional_conversions:,.0f} and additional revenue = ${additional_revenue:,.0f}.

SUCCESS CRITERIA:
- Reduce drop rate on this step by at least 5 percentage points.
- Improve completion rate by at least 10% relative to baseline.
- Confirm the change with a statistically valid A/B test.
"""


def run_pipeline():
    stages = build_funnel_stages()
    funnel_df, impact_df, biggest_drop = compute_funnel_metrics(stages)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    chart_path = OUTPUT_DIR / "funnel_chart.png"
    report_path = OUTPUT_DIR / "funnel_analysis.txt"
    funnel_df_path = OUTPUT_DIR / "funnel_analysis.csv"

    save_funnel_chart(stages, chart_path)
    funnel_df.to_csv(funnel_df_path, index=False)

    report = [
        "Funnel Analysis & Drop-Off Detection",
        "====================================",
        "",
        "Stage volumes:",
        pd.Series(stages).to_string(),
        "",
        "Drop-off table:",
        funnel_df.to_string(index=False),
        "",
        "Business impact ranking:",
        impact_df.sort_values(
            by=["revenue_impact", "drop_rate", "users_lost"],
            ascending=[False, False, False],
        ).to_string(index=False),
        "",
        build_recommendation(biggest_drop),
    ]

    report_text = "\n".join(report)
    report_path.write_text(report_text, encoding="utf-8")

    print(report_text)
    print(f"\nSaved chart to {chart_path}")
    print(f"Saved report to {report_path}")
    print(f"Saved metrics to {funnel_df_path}")


if __name__ == "__main__":
    run_pipeline()