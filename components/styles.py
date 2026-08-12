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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Reset & Global ── */
    * { box-sizing: border-box; }
    html, body, .stApp {
        background-color: #F1F5F9 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.8rem !important;
        padding-right: 1.8rem !important;
        max-width: 100% !important;
    }
    footer { display: none !important; }
    #MainMenu { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }

    /* ── Hide Streamlit Default Page Navigation & Sidebar Controls ── */
    section[data-testid="stSidebar"] ul,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] nav,
    [data-testid="stSidebarNavItems"],
    [data-testid="stSidebarNavSeparator"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* ── Dark Navy Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        width: 232px !important;
        min-width: 232px !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
        padding: 0 !important;
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding: 0 !important;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
    section[data-testid="stSidebar"] * {
        color: #CBD5E1 !important;
    }

    /* ── Sidebar Buttons ── */
    section[data-testid="stSidebar"] button {
        background: transparent !important;
        border: none !important;
        color: #94A3B8 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 9px 14px !important;
        margin: 1px 8px !important;
        width: calc(100% - 16px) !important;
        text-align: left !important;
        border-radius: 7px !important;
        transition: all 0.15s ease !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    section[data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.07) !important;
        color: #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] button:disabled {
        background: rgba(59,130,246,0.18) !important;
        color: #93C5FD !important;
        border-left: 3px solid #3B82F6 !important;
        opacity: 1 !important;
        font-weight: 600 !important;
        cursor: default !important;
        padding-left: 11px !important;
    }
    section[data-testid="stSidebar"] button p {
        font-size: 13px !important;
        font-weight: inherit !important;
        margin: 0 !important;
    }

    /* ── Sidebar Logo Header ── */
    .sp-sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 18px 16px 14px 16px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 4px;
    }
    .sp-logo-mark {
        width: 32px; height: 32px;
        background: linear-gradient(135deg, #3B82F6, #1D4ED8);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(59,130,246,0.35);
        flex-shrink: 0;
    }
    .sp-logo-wordmark {
        font-size: 15px; font-weight: 700;
        color: white !important;
        letter-spacing: -0.3px;
        line-height: 1.2;
    }
    .sp-logo-sub {
        font-size: 9px; font-weight: 600;
        color: #475569 !important;
        text-transform: uppercase; letter-spacing: 1.2px;
        margin-top: 1px;
    }

    /* ── Sidebar Nav Section Label ── */
    .sp-nav-label {
        font-size: 9.5px; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1.2px;
        color: #334155 !important;
        padding: 12px 16px 5px 16px;
    }

    /* ── Sidebar Bottom User Chip ── */
    .sp-sidebar-bottom {
        margin-top: auto;
        padding: 12px 10px;
        border-top: 1px solid rgba(255,255,255,0.06);
    }
    .sp-user-chip {
        display: flex; align-items: center; gap: 9px;
        padding: 8px 6px;
        border-radius: 7px;
        background: rgba(255,255,255,0.04);
    }
    .sp-user-avatar {
        width: 28px; height: 28px;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 11px; font-weight: 700; color: white !important;
        flex-shrink: 0;
    }
    .sp-user-name { font-size: 12px; font-weight: 600; color: #CBD5E1 !important; }
    .sp-user-role { font-size: 10px; color: #475569 !important; text-transform: uppercase; letter-spacing: 0.5px; }
    .sp-status-dot {
        width: 7px; height: 7px; border-radius: 50%;
        background: #10B981; margin-left: auto; flex-shrink: 0;
        box-shadow: 0 0 6px rgba(16,185,129,0.5);
    }

    /* ── Streamlit Container as White Card ── */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 18px 20px !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
        margin-bottom: 14px !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        gap: 0.5rem !important;
    }

    .sp-card-title {
        font-size: 13.5px; font-weight: 700; color: #0F172A;
        margin-bottom: 12px; letter-spacing: -0.2px;
        display: flex; align-items: center; gap: 7px;
    }

    /* ── Page Top Bar ── */
    .sp-top-bar {
        display: flex; align-items: flex-start; justify-content: space-between;
        padding-bottom: 14px; margin-bottom: 16px;
        border-bottom: 1px solid #E2E8F0;
    }
    .sp-page-title {
        font-size: 20px; font-weight: 800; color: #0F172A;
        margin: 0; letter-spacing: -0.6px; line-height: 1.2;
    }
    .sp-page-sub {
        font-size: 12px; color: #94A3B8; margin-top: 3px; font-weight: 400;
    }

    /* ── KPI Accent Cards ── */
    .sp-kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 18px;
        border-left: 4px solid #3B82F6;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        margin-bottom: 14px;
        position: relative;
        overflow: hidden;
    }
    .sp-kpi-card::after {
        content: "";
        position: absolute; top: 0; right: 0;
        width: 55px; height: 100%;
        background: linear-gradient(135deg, transparent, rgba(59,130,246,0.03));
        pointer-events: none;
    }
    .sp-kpi-card.green  { border-left-color: #10B981; }
    .sp-kpi-card.green::after  { background: linear-gradient(135deg, transparent, rgba(16,185,129,0.03)); }
    .sp-kpi-card.amber  { border-left-color: #F59E0B; }
    .sp-kpi-card.amber::after  { background: linear-gradient(135deg, transparent, rgba(245,158,11,0.03)); }
    .sp-kpi-card.purple { border-left-color: #8B5CF6; }
    .sp-kpi-card.purple::after { background: linear-gradient(135deg, transparent, rgba(139,92,246,0.03)); }
    .sp-kpi-card.red    { border-left-color: #EF4444; }

    .sp-kpi-label {
        font-size: 10.5px; font-weight: 700; color: #64748B;
        text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 7px;
    }
    .sp-kpi-value {
        font-size: 24px; font-weight: 800; color: #0F172A;
        line-height: 1.1; margin-bottom: 5px; letter-spacing: -0.5px;
    }
    .sp-kpi-delta {
        font-size: 11.5px; font-weight: 600;
        display: inline-flex; align-items: center; gap: 3px;
    }
    .sp-delta-positive { color: #10B981; }
    .sp-delta-negative { color: #EF4444; }
    .sp-delta-neutral  { color: #94A3B8; }

    /* ── Status Tag Pills ── */
    .sp-tag {
        display: inline-block; padding: 2px 8px; border-radius: 5px;
        font-size: 10.5px; font-weight: 600; white-space: nowrap;
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
        width: 100%; border-collapse: collapse; font-size: 12.5px;
    }
    .sp-table thead tr {
        border-bottom: 2px solid #E2E8F0;
    }
    .sp-table thead th {
        padding: 8px 12px; text-align: left;
        font-size: 10.5px; font-weight: 700; color: #64748B;
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
        padding: 9px 12px; color: #1E293B; vertical-align: middle;
    }
    .sp-table .rank-cell {
        font-weight: 700; color: #3B82F6; font-size: 14px;
    }

    /* ── Insight / Feed Rows ── */
    .sp-feed-row {
        display: flex; align-items: flex-start; justify-content: space-between;
        padding: 11px 0; border-bottom: 1px solid #F1F5F9; gap: 12px;
    }
    .sp-feed-row:last-child { border-bottom: none; padding-bottom: 0; }
    .sp-feed-dot {
        width: 7px; height: 7px; border-radius: 50%;
        background: #3B82F6; margin-top: 5px; flex-shrink: 0;
    }
    .sp-feed-dot.red   { background: #EF4444; }
    .sp-feed-dot.amber { background: #F59E0B; }
    .sp-feed-dot.green { background: #10B981; }
    .sp-feed-title { font-size: 12.5px; font-weight: 600; color: #0F172A; }
    .sp-feed-desc  { font-size: 11.5px; color: #64748B; margin-top: 2px; line-height: 1.4; }

    /* ── Coaching Priority Cards ── */
    .sp-coach-card {
        border-radius: 7px; padding: 10px 12px; margin-bottom: 7px;
        border-left: 3px solid #3B82F6;
        background: #EFF6FF;
    }
    .sp-coach-card.high   { border-left-color: #EF4444; background: #FEF2F2; }
    .sp-coach-card.medium { border-left-color: #F59E0B; background: #FFFBEB; }
    .sp-coach-card.low    { border-left-color: #10B981; background: #F0FDF4; }
    .sp-coach-issue  { font-size: 11.5px; font-weight: 700; color: #1E293B; margin-bottom: 3px; }
    .sp-coach-action { font-size: 11px;   color: #475569; line-height: 1.4; }

    /* ── Win/Loss Reason Cards ── */
    .sp-reason-card {
        display: flex; align-items: center; justify-content: space-between;
        padding: 10px 12px; border-radius: 7px; margin-bottom: 7px;
        background: #F8FAFC; border: 1px solid #E2E8F0;
    }
    .sp-reason-card.win     { background: #F0FDF4; border-color: #BBF7D0; }
    .sp-reason-card.loss    { background: #FEF2F2; border-color: #FECACA; }
    .sp-reason-card.neutral { background: #FFFBEB; border-color: #FDE68A; }
    .sp-reason-rank { font-size: 10px; font-weight: 700; color: #94A3B8; margin-right: 8px; }
    .sp-reason-text { font-size: 12.5px; font-weight: 600; color: #1E293B; flex: 1; }
    .sp-reason-pct  { font-size: 12.5px; font-weight: 700; }
    .sp-reason-pct.win  { color: #16A34A; }
    .sp-reason-pct.loss { color: #DC2626; }

    /* ── Detail Panel (Team Performance) ── */
    .sp-detail-panel {
        background: #FFFFFF;
        border-radius: 10px;
        height: 100%;
    }
    .sp-rep-avatar {
        width: 44px; height: 44px; border-radius: 10px;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        display: flex; align-items: center; justify-content: center;
        font-size: 16px; font-weight: 700; color: white !important; flex-shrink: 0;
    }
    .sp-stat-row {
        display: flex; justify-content: space-between;
        align-items: center; padding: 7px 0;
        border-bottom: 1px solid #F1F5F9; font-size: 12.5px;
    }
    .sp-stat-row:last-child { border-bottom: none; }
    .sp-stat-label { color: #64748B; font-weight: 500; }
    .sp-stat-value { color: #0F172A; font-weight: 700; }

    /* ── Attainment Bar ── */
    .sp-bar-track {
        width: 100%; height: 5px; background: #E2E8F0;
        border-radius: 3px; overflow: hidden; margin-top: 4px;
    }
    .sp-bar-fill {
        height: 100%; border-radius: 3px;
        background: linear-gradient(90deg, #3B82F6, #10B981);
        transition: width 0.4s ease;
    }
    .sp-bar-fill.over { background: linear-gradient(90deg, #10B981, #059669); }
    .sp-bar-fill.low  { background: linear-gradient(90deg, #F59E0B, #EF4444); }

    /* ── Streamlit widget overrides ── */
    div[data-baseweb="select"] > div {
        border-radius: 7px !important; border-color: #CBD5E1 !important;
        background: white !important; font-size: 13px !important;
    }
    .stDateInput input {
        border-radius: 7px !important; border-color: #CBD5E1 !important;
        font-size: 13px !important;
    }
    .stButton > button {
        border-radius: 7px !important; font-weight: 600 !important;
        font-size: 13px !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        color: white !important; border: none !important;
        box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
    }
    .stRadio label { font-size: 13px !important; }
    .stSelectbox label, .stDateInput label { font-size: 12px !important; }

    /* ── Separator ── */
    .sp-hr { border: 0; border-top: 1px solid #E2E8F0; margin: 12px 0; }

    /* ── Streamlit column gap tightening ── */
    div[data-testid="column"] { padding: 0 4px !important; }
    div[data-testid="column"]:first-child { padding-left: 0 !important; }
    div[data-testid="column"]:last-child  { padding-right: 0 !important; }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
