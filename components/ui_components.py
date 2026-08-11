"""
SalesPulse UI Components Engine
-------------------------------
Shared render functions: metric_card(), status_tag(), data_table(),
insight_feed_row(), coaching_card(), reason_card().
"""

import streamlit as st
import pandas as pd


def status_tag(text, tag_type="neutral"):
    """Renders an inline colored pill badge."""
    return f'<span class="sp-tag sp-tag-{tag_type}">{text}</span>'


def metric_card(label, value, delta=None, delta_type="positive", accent="blue"):
    """Accent left-border KPI card with label, big value, delta trend."""
    delta_html = ""
    if delta:
        cls = f"sp-delta-{delta_type}"
        arrow = "↑" if delta_type == "positive" else ("↓" if delta_type == "negative" else "•")
        delta_html = f'<div class="sp-kpi-delta {cls}">{arrow} {delta}</div>'

    color_cls = {"blue": "", "green": "green", "amber": "amber",
                 "purple": "purple", "red": "red"}.get(accent, "")

    st.markdown(f"""
    <div class="sp-kpi-card {color_cls}">
        <div class="sp-kpi-label">{label}</div>
        <div class="sp-kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def attainment_bar(pct_float, label=""):
    """Renders a small progress bar for % attainment."""
    pct = min(pct_float, 100)
    cls = "over" if pct_float >= 100 else ("low" if pct_float < 70 else "")
    return f"""
    <div style="font-size:12px; font-weight:600; color:#0F172A;">{label}</div>
    <div class="sp-bar-track">
        <div class="sp-bar-fill {cls}" style="width:{pct}%"></div>
    </div>
    """


def insight_feed_row(title, description, category=None, tag=None, tag_type="info", dot_color="blue"):
    """Renders a recommendation/event list row with colored dot and optional tag."""
    tag_html = status_tag(tag, tag_type) if tag else ""
    cat_html = f'<span style="font-size:10px;font-weight:700;text-transform:uppercase;color:#94A3B8;margin-right:4px;">[{category}]</span>' if category else ""
    st.markdown(f"""
    <div class="sp-feed-row">
        <div style="display:flex;align-items:flex-start;gap:10px;flex:1;">
            <div class="sp-feed-dot {dot_color}" style="margin-top:5px;"></div>
            <div>
                <div class="sp-feed-title">{cat_html}{title}</div>
                <div class="sp-feed-desc">{description}</div>
            </div>
        </div>
        <div style="flex-shrink:0;margin-left:12px;">{tag_html}</div>
    </div>
    """, unsafe_allow_html=True)


def coaching_card(issue, action, priority="medium"):
    """Renders a coaching recommendation card with priority color."""
    priority_label = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}.get(priority, "Medium")
    st.markdown(f"""
    <div class="sp-coach-card {priority}">
        <div class="sp-coach-issue">{priority_label} — {issue}</div>
        <div class="sp-coach-action">💡 {action}</div>
    </div>
    """, unsafe_allow_html=True)


def reason_card(rank, driver, impact_pct, card_type="win"):
    """Renders a win/loss reason card with rank, text, and impact %."""
    pct_cls = "win" if card_type == "win" else "loss"
    prefix = "+" if card_type == "win" else "-"
    st.markdown(f"""
    <div class="sp-reason-card {card_type}">
        <span class="sp-reason-rank">#{rank}</span>
        <span class="sp-reason-text">{driver}</span>
        <span class="sp-reason-pct {pct_cls}">{prefix}{impact_pct}%</span>
    </div>
    """, unsafe_allow_html=True)


def data_table(df, tag_column=None, tag_type_column=None):
    """
    Renders a styled HTML table with zebra rows, compact density, and embedded tags.
    """
    if df is None or df.empty:
        st.markdown("""
        <div style="text-align:center;padding:28px;color:#94A3B8;font-size:13px;">
            No data available for the current filters.
        </div>
        """, unsafe_allow_html=True)
        return

    table_df = df.copy()

    if tag_column and tag_column in table_df.columns:
        def _fmt(row):
            val = row[tag_column]
            t = row[tag_type_column] if (tag_type_column and tag_type_column in row.index) else "neutral"
            return status_tag(str(val), t)
        table_df[tag_column] = table_df.apply(_fmt, axis=1)
        if tag_type_column and tag_type_column in table_df.columns:
            table_df = table_df.drop(columns=[tag_type_column])

    headers = "".join(
        f'<th>{col.replace("_", " ").title()}</th>'
        for col in table_df.columns
    )
    rows = "".join(
        f'<tr>{"".join(f"<td>{v}</td>" for v in row)}</tr>'
        for row in table_df.itertuples(index=False)
    )

    st.markdown(f"""
    <div class="sp-table-wrap">
        <table class="sp-table">
            <thead><tr>{headers}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
