"""
SalesPulse Design System & Custom CSS Injection
-----------------------------------------------
Dark navy sidebar, white card main area, accent KPI cards,
zebra-stripe tables, coaching priority cards, status pill tags.
"""

import streamlit as st


def inject_custom_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ── Reset & Global ── */
    .stApp {
        background-color: #F1F5F9 !important;
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.8rem !important;
        padding-right: 1.8rem !important;
        max-width: 100% !important;
    }

    /* ── Hide Streamlit toolbar & footer only ── */
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    footer { display: none !important; }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 99999 !important;
    }

    /* ── Dark Navy Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] {
        padding-top: 0.5rem !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] ul {
        padding: 0 8px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] a {
        background-color: #334155 !important;
        border-radius: 8px !important;
        margin: 4px 0 !important;
        padding: 10px 14px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] a:hover {
        background-color: #475569 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #2563EB !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* ── Sidebar Logo Header ── */
    .sp-sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 22px 20px 16px 20px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 8px;
    }
    .sp-logo-mark {
        width: 34px; height: 34px;
        background: linear-gradient(135deg, #3B82F6, #1D4ED8);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 18px;
        box-shadow: 0 4px 12px rgba(59,130,246,0.4);
        flex-shrink: 0;
    }
    .sp-logo-wordmark {
        font-size: 17px; font-weight: 700;
        color: white !important;
        letter-spacing: -0.3px;
    }
    .sp-logo-sub {
        font-size: 10px; font-weight: 600;
        color: #64748B !important;
        text-transform: uppercase; letter-spacing: 1px;
        margin-top: 1px;
    }

    /* ── Sidebar Nav Label ── */
    .sp-nav-label {
        font-size: 10px; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1.2px;
        color: #475569 !important;
        padding: 16px 20px 6px 20px;
    }

    /* ── Sidebar Nav Items ── */
    .sp-nav-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 16px;
        margin: 2px 10px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.15s ease;
        color: #94A3B8 !important;
        font-size: 13px;
        font-weight: 500;
        text-decoration: none;
    }
    .sp-nav-item:hover {
        background: rgba(255,255,255,0.07);
        color: #E2E8F0 !important;
    }
    .sp-nav-item.active {
        background: rgba(59,130,246,0.18);
        color: #93C5FD !important;
        font-weight: 600;
        border-left: 3px solid #3B82F6;
    }
    .sp-nav-icon { font-size: 15px; width: 20px; text-align: center; }

    /* ── Sidebar User Chip ── */
    .sp-sidebar-user {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        padding: 14px 16px;
        border-top: 1px solid rgba(255,255,255,0.07);
        background: rgba(0,0,0,0.15);
    }
    .sp-user-chip {
        display: flex; align-items: center; gap: 10px;
    }
    .sp-user-avatar {
        width: 32px; height: 32px;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 13px; font-weight: 700; color: white !important;
        flex-shrink: 0;
    }
    .sp-user-name { font-size: 12px; font-weight: 600; color: #E2E8F0 !important; }
    .sp-user-role { font-size: 10px; color: #64748B !important; text-transform: uppercase; }

    /* ── White Card Base ── */
    .sp-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px 22px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 16px;
    }
    .sp-card-title {
        font-size: 14px; font-weight: 700; color: #1E293B;
        margin-bottom: 16px; letter-spacing: -0.2px;
        display: flex; align-items: center; justify-content: space-between;
    }
    .sp-card-subtitle {
        font-size: 12px; color: #64748B; font-weight: 400; margin-left: 4px;
    }

    /* ── KPI Accent Cards ── */
    .sp-kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        border-left: 4px solid #3B82F6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 16px;
        position: relative;
        overflow: hidden;
    }
    .sp-kpi-card::after {
        content: "";
        position: absolute; top: 0; right: 0;
        width: 60px; height: 100%;
        background: linear-gradient(135deg, transparent, rgba(59,130,246,0.03));
    }
    .sp-kpi-card.green { border-left-color: #10B981; }
    .sp-kpi-card.green::after { background: linear-gradient(135deg, transparent, rgba(16,185,129,0.03)); }
    .sp-kpi-card.amber { border-left-color: #F59E0B; }
    .sp-kpi-card.amber::after { background: linear-gradient(135deg, transparent, rgba(245,158,11,0.03)); }
    .sp-kpi-card.purple { border-left-color: #8B5CF6; }
    .sp-kpi-card.red { border-left-color: #EF4444; }

    .sp-kpi-label {
        font-size: 11px; font-weight: 600; color: #64748B;
        text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 8px;
    }
    .sp-kpi-value {
        font-size: 26px; font-weight: 800; color: #0F172A;
        line-height: 1.1; margin-bottom: 6px; letter-spacing: -0.5px;
    }
    .sp-kpi-delta {
        font-size: 12px; font-weight: 600;
        display: inline-flex; align-items: center; gap: 3px;
    }
    .sp-delta-positive { color: #10B981; }
    .sp-delta-negative { color: #EF4444; }
    .sp-delta-neutral  { color: #94A3B8; }

    /* ── Top Bar ── */
    .sp-top-bar {
        display: flex; align-items: flex-start; justify-content: space-between;
        padding-bottom: 16px; margin-bottom: 20px;
        border-bottom: 1px solid #E2E8F0;
    }
    .sp-page-title {
        font-size: 22px; font-weight: 800; color: #0F172A;
        margin: 0; letter-spacing: -0.5px;
    }
    .sp-page-sub {
        font-size: 12px; color: #94A3B8; margin-top: 3px; font-weight: 400;
    }

    /* ── Status Tag Pills ── */
    .sp-tag {
        display: inline-block; padding: 3px 9px; border-radius: 6px;
        font-size: 11px; font-weight: 600; white-space: nowrap;
    }
    .sp-tag-success { background: #DCFCE7; color: #15803D; }
    .sp-tag-warning { background: #FEF3C7; color: #B45309; }
    .sp-tag-danger  { background: #FEE2E2; color: #B91C1C; }
    .sp-tag-info    { background: #DBEAFE; color: #1D4ED8; }
    .sp-tag-neutral { background: #F1F5F9; color: #475569; }
    .sp-tag-purple  { background: #F3E8FF; color: #7C3AED; }

    /* ── Data Tables ── */
    .sp-table-wrap { overflow-x: auto; width: 100%; }
    .sp-table {
        width: 100%; border-collapse: collapse; font-size: 13px;
    }
    .sp-table thead tr {
        border-bottom: 2px solid #E2E8F0;
    }
    .sp-table thead th {
        padding: 9px 14px; text-align: left;
        font-size: 11px; font-weight: 700; color: #64748B;
        text-transform: uppercase; letter-spacing: 0.5px;
        white-space: nowrap; background: #F8FAFC;
    }
    .sp-table tbody tr {
        border-bottom: 1px solid #F1F5F9;
        transition: background 0.1s;
    }
    .sp-table tbody tr:nth-child(even) { background: #FAFBFC; }
    .sp-table tbody tr:hover { background: #EFF6FF !important; }
    .sp-table tbody td {
        padding: 10px 14px; color: #1E293B; vertical-align: middle;
    }
    .sp-table .rank-cell {
        font-weight: 700; color: #3B82F6; font-size: 14px;
    }

    /* ── Insight / Feed Rows ── */
    .sp-feed-row {
        display: flex; align-items: flex-start; justify-content: space-between;
        padding: 12px 0; border-bottom: 1px solid #F1F5F9; gap: 12px;
    }
    .sp-feed-row:last-child { border-bottom: none; padding-bottom: 0; }
    .sp-feed-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: #3B82F6; margin-top: 5px; flex-shrink: 0;
    }
    .sp-feed-dot.red { background: #EF4444; }
    .sp-feed-dot.amber { background: #F59E0B; }
    .sp-feed-dot.green { background: #10B981; }
    .sp-feed-title { font-size: 13px; font-weight: 600; color: #1E293B; }
    .sp-feed-desc { font-size: 12px; color: #64748B; margin-top: 2px; line-height: 1.4; }

    /* ── Coaching Priority Cards ── */
    .sp-coach-card {
        border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;
        border-left: 4px solid #3B82F6;
        background: #EFF6FF;
    }
    .sp-coach-card.high { border-left-color: #EF4444; background: #FEF2F2; }
    .sp-coach-card.medium { border-left-color: #F59E0B; background: #FFFBEB; }
    .sp-coach-card.low { border-left-color: #10B981; background: #F0FDF4; }
    .sp-coach-issue {
        font-size: 12px; font-weight: 700; color: #1E293B; margin-bottom: 4px;
    }
    .sp-coach-action { font-size: 11px; color: #475569; line-height: 1.4; }

    /* ── Win/Loss Reason Cards ── */
    .sp-reason-card {
        display: flex; align-items: center; justify-content: space-between;
        padding: 12px 14px; border-radius: 8px; margin-bottom: 8px;
        background: #F8FAFC; border: 1px solid #E2E8F0;
    }
    .sp-reason-card.win { background: #F0FDF4; border-color: #BBF7D0; }
    .sp-reason-card.loss { background: #FEF2F2; border-color: #FECACA; }
    .sp-reason-card.neutral { background: #FFFBEB; border-color: #FDE68A; }
    .sp-reason-rank { font-size: 11px; font-weight: 700; color: #94A3B8; margin-right: 10px; }
    .sp-reason-text { font-size: 13px; font-weight: 600; color: #1E293B; flex: 1; }
    .sp-reason-pct { font-size: 13px; font-weight: 700; }
    .sp-reason-pct.win { color: #16A34A; }
    .sp-reason-pct.loss { color: #DC2626; }

    /* ── Detail Panel (Team Performance) ── */
    .sp-detail-panel {
        background: #FFFFFF; border: 1px solid #E2E8F0;
        border-radius: 12px; padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        height: 100%;
    }
    .sp-rep-avatar {
        width: 48px; height: 48px; border-radius: 12px;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; flex-shrink: 0;
    }
    .sp-stat-row {
        display: flex; justify-content: space-between;
        align-items: center; padding: 8px 0;
        border-bottom: 1px solid #F1F5F9; font-size: 13px;
    }
    .sp-stat-row:last-child { border-bottom: none; }
    .sp-stat-label { color: #64748B; font-weight: 500; }
    .sp-stat-value { color: #0F172A; font-weight: 700; }

    /* ── Attainment Bar ── */
    .sp-bar-track {
        width: 100%; height: 6px; background: #E2E8F0;
        border-radius: 3px; overflow: hidden; margin-top: 4px;
    }
    .sp-bar-fill {
        height: 100%; border-radius: 3px;
        background: linear-gradient(90deg, #3B82F6, #10B981);
        transition: width 0.4s ease;
    }
    .sp-bar-fill.over { background: linear-gradient(90deg, #10B981, #059669); }
    .sp-bar-fill.low { background: linear-gradient(90deg, #F59E0B, #EF4444); }

    /* ── Streamlit widget overrides ── */
    div[data-baseweb="select"] > div {
        border-radius: 8px !important; border-color: #CBD5E1 !important;
        background: white !important; font-size: 13px !important;
    }
    .stDateInput input {
        border-radius: 8px !important; border-color: #CBD5E1 !important;
        font-size: 13px !important;
    }
    .stButton>button {
        border-radius: 8px !important; font-weight: 600 !important;
        font-size: 13px !important;
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        color: white !important; border: none !important;
        box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
    }
    .stRadio label { font-size: 13px !important; }
    .stSelectbox label, .stDateInput label { font-size: 12px !important; }

    /* ── Separator ── */
    .sp-hr { border: 0; border-top: 1px solid #E2E8F0; margin: 14px 0; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
