"""
SalesPulse — Team Performance & AI Coaching
View 5: KPI row → leaderboard table left + coaching detail panel right.
"""

import streamlit as st
from components.styles import inject_custom_css
from components.header import render_top_bar
from components.ui_components import metric_card, data_table, coaching_card, attainment_bar, status_tag
from database_manager import fetch_team_performance
from ai_coaching import get_coaching_recommendations

st.set_page_config(page_title="Team Performance | SalesPulse AI", layout="wide")
inject_custom_css()
render_top_bar("Team Performance", "Sales rep leaderboard, quota attainment & AI-powered coaching recommendations")

start_date, end_date = st.session_state.get("date_range", (None, None))
segment = st.session_state.get("selected_segment", "All Segments")
df_reps, rep_details = fetch_team_performance(start_date, end_date, segment)

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1: metric_card("Team Quota Attainment", "94.2%",      "+3.8 pts",  "positive", "green")
with k2: metric_card("Top Rep Attainment",    "114.0%",     "Sarah Jenkins", "positive", "blue")
with k3: metric_card("Avg Sales Cycle",       "28.2 Days",  "-2.4 days", "positive", "amber")
with k4: metric_card("Team Activity Score",   "81.6 / 100", "+5.2 pts",  "positive", "purple")

# ── Layout: Leaderboard Left + Coaching Panel Right ──────────────────────────
col_table, col_detail = st.columns([0.63, 0.37], gap="medium")

with col_table:
    st.markdown('<div class="sp-card">', unsafe_allow_html=True)
    st.markdown('<div class="sp-card-title">👥 Sales Rep Leaderboard & Performance Telemetry</div>', unsafe_allow_html=True)

    selected_rep_name = st.radio(
        "Select rep to view coaching panel:",
        options=df_reps["name"].tolist(),
        horizontal=True,
        key="rep_selector"
    )
    selected_rep_id = int(df_reps[df_reps["name"] == selected_rep_name]["id"].iloc[0])

    # Custom leaderboard table with rank numbers + attainment bars
    st.markdown('<div class="sp-table-wrap"><table class="sp-table"><thead><tr>'
                '<th>#</th><th>Representative</th><th>Role</th>'
                '<th>Closed</th><th>Attainment</th><th>Deals</th>'
                '<th>Avg Cycle</th><th>Activity Score</th><th>Status</th>'
                '</tr></thead><tbody>', unsafe_allow_html=True)

    for i, row in df_reps.reset_index(drop=True).iterrows():
        rank = i + 1
        rank_color = "#F59E0B" if rank == 1 else ("#94A3B8" if rank == 2 else "#CD7F32" if rank == 3 else "#CBD5E1")
        rank_icon = "🥇" if rank == 1 else ("🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}")

        att_raw = str(row.get("attainment", "0%")).replace("%", "")
        try:
            att_float = float(att_raw)
        except ValueError:
            att_float = 0.0
        att_cls = "over" if att_float >= 100 else ("low" if att_float < 70 else "")
        att_bar_html = f'<div style="font-size:12px;font-weight:700;color:#0F172A;">{row.get("attainment","")}</div><div class="sp-bar-track"><div class="sp-bar-fill {att_cls}" style="width:{min(att_float,100)}%"></div></div>'

        tag_type = str(row.get("tag_type", "neutral"))
        status_html = status_tag(str(row.get("status", "")), tag_type)

        highlight = 'style="background:#EFF6FF !important;"' if row["name"] == selected_rep_name else ''

        st.markdown(f"""
        <tr {highlight}>
            <td><span style="font-size:15px;">{rank_icon}</span></td>
            <td><strong style="color:#0F172A;">{row['name']}</strong></td>
            <td><span style="font-size:11px;color:#64748B;">{row.get('role','')}</span></td>
            <td style="font-weight:700;color:#1E293B;">{row.get('closed','')}</td>
            <td style="min-width:120px;">{att_bar_html}</td>
            <td style="color:#1E293B;">{row.get('deals','')}</td>
            <td style="color:#1E293B;">{row.get('avg_cycle','')}</td>
            <td style="font-weight:700;color:#2563EB;">{row.get('activity_score','')}</td>
            <td>{status_html}</td>
        </tr>
        """, unsafe_allow_html=True)

    st.markdown('</tbody></table></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_detail:
    rep_info = rep_details.get(selected_rep_id, rep_details[1])
    ai_recs  = get_coaching_recommendations(selected_rep_id)

    st.markdown('<div class="sp-detail-panel">', unsafe_allow_html=True)

    # Rep Avatar + Header
    initials = "".join([n[0] for n in rep_info["name"].split()[:2]])
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:16px;">
        <div class="sp-rep-avatar">{initials}</div>
        <div>
            <div style="font-size:16px;font-weight:700;color:#0F172A;">{rep_info['name']}</div>
            <div style="font-size:12px;color:#64748B;">{rep_info['role']}</div>
        </div>
    </div>
    <hr class="sp-hr">
    """, unsafe_allow_html=True)

    # Key Stats
    stats = [
        ("Quota Attained",  rep_info.get("attainment", "—")),
        ("Closed Revenue",  rep_info.get("revenue", "—")),
        ("Win Rate",        rep_info.get("win_rate", "—")),
        ("Pipeline Held",   rep_info.get("pipeline_held", "—")),
    ]
    for label, val in stats:
        st.markdown(f"""
        <div class="sp-stat-row">
            <span class="sp-stat-label">{label}</span>
            <span class="sp-stat-value">{val}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="sp-hr">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;font-weight:700;color:#1E293B;margin-bottom:10px;">🤖 AI Coaching Recommendations</div>', unsafe_allow_html=True)

    for rec in ai_recs:
        priority = rec.get("priority", "medium")
        issue  = rec.get("issue",  rec.get("issue_description", "—"))
        action = rec.get("action", rec.get("suggested_action",  "—"))
        coaching_card(issue, action, priority)

    st.markdown('<hr class="sp-hr">', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:12px;color:#64748B;margin-bottom:8px;"><strong>Manager Action:</strong> {rep_info.get("recommended_action","—")}</div>', unsafe_allow_html=True)

    if st.button(f"⚡ Assign Action to {rep_info['name'].split()[0]}", type="primary",
                 key="btn_assign", use_container_width=True):
        st.toast(f"✅ Action assigned to {rep_info['name']} via Slack & Email!", icon="🚀")

    st.markdown('</div>', unsafe_allow_html=True)
