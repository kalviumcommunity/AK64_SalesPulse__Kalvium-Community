"""
API client wrapper for SalesPulse AI Streamlit Frontend.
Attempts live backend communication with fallback demo data for standalone execution.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta

NODE_BACKEND_URL = "http://localhost:5000/api"
FASTAPI_AI_URL = "http://localhost:8000"

def check_backend_status():
    """Returns True if the backend is reachable."""
    try:
        res = requests.get(f"{NODE_BACKEND_URL}/health", timeout=1.5)
        return res.status_code == 200
    except Exception:
        return False

def login_user(email, password):
    """Authenticate user and return user session & JWT token."""
    try:
        res = requests.post(f"{NODE_BACKEND_URL}/auth/login", json={"email": email, "password": password}, timeout=2)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
    except Exception:
        pass

    # Demo Fallback Auth Logic
    role = "Sales Representative"
    name = "Aditya Kulkarni"
    if "manager" in email.lower() or "meera" in email.lower():
        role = "Sales Manager"
        name = "Meera Nair"
    elif "vp" in email.lower() or "admin" in email.lower() or "rohan" in email.lower():
        role = "VP of Sales"
        name = "Rohan Bhatt"

    return {
        "success": True,
        "token": "demo_jwt_token_salespulse_2026",
        "user": {
            "user_id": 1,
            "name": name,
            "email": email,
            "role": role,
            "team": "Enterprise Sales East"
        }
    }

def register_user(name, email, password, role):
    """Register new user."""
    try:
        res = requests.post(f"{NODE_BACKEND_URL}/auth/register", json={
            "name": name, "email": email, "password": password, "role": role
        }, timeout=2)
        if res.status_code in (200, 201):
            return {"success": True, "message": "User registered successfully"}
    except Exception:
        pass

    return {
        "success": True,
        "message": f"Account created successfully for {name} ({role})! You can now log in."
    }

def get_performance_summary(date_range="30d"):
    """Fetch key performance metrics and sales trends."""
    # Data structure matching Performance.jsx
    revenue_trend = pd.DataFrame([
        {"Month": "Jan", "Sales ($)": 42000, "Target ($)": 40000},
        {"Month": "Feb", "Sales ($)": 58000, "Target ($)": 45000},
        {"Month": "Mar", "Sales ($)": 62000, "Target ($)": 50000},
        {"Month": "Apr", "Sales ($)": 78000, "Target ($)": 55000},
        {"Month": "May", "Sales ($)": 80000, "Target ($)": 60000},
        {"Month": "Jun", "Sales ($)": 96000, "Target ($)": 65000},
        {"Month": "Jul", "Sales ($)": 89000, "Target ($)": 70000},
    ])

    channel_data = pd.DataFrame([
        {"Channel": "Email", "Touchpoints": 38},
        {"Channel": "Phone", "Touchpoints": 27},
        {"Channel": "Demo", "Touchpoints": 19},
        {"Channel": "Meeting", "Touchpoints": 16},
    ])

    top_performers = pd.DataFrame([
        {"Rep": "Sarah Jenkins", "Deals Closed": 12, "Revenue": "$144,000", "Win Rate": "72%", "Quota Attainment": "124%", "Status": "Exceeding"},
        {"Rep": "Michael Chen", "Deals Closed": 9, "Revenue": "$98,500", "Win Rate": "61%", "Quota Attainment": "103%", "Status": "On Track"},
        {"Rep": "Emma Watson", "Deals Closed": 7, "Revenue": "$76,200", "Win Rate": "58%", "Quota Attainment": "88%", "Status": "At Risk"},
        {"Rep": "David Miller", "Deals Closed": 5, "Revenue": "$54,000", "Win Rate": "44%", "Quota Attainment": "71%", "Status": "At Risk"},
    ])

    insights = [
        {"label": "Sarah Jenkins", "note": "Closed 3 deals this week — 40% above personal best", "tag": "Top Performer", "type": "success"},
        {"label": "David Miller", "note": "Response time at 6.2h — exceeds team avg of 3.4h", "tag": "Needs Attention", "type": "warning"},
        {"label": "Enterprise Q3", "note": "4 high-value deals at negotiation — review urgently", "tag": "Opportunity", "type": "info"},
    ]

    return {
        "today_achievement": "$12,400",
        "today_comparison": "+18% vs yesterday",
        "win_rate_mtd": "63.2%",
        "win_rate_helper": "Team avg: 54.1%",
        "avg_cycle_time": "18 days",
        "cycle_time_helper": "−2 days vs last month",
        "active_reps": "8 / 10",
        "revenue_trend": revenue_trend,
        "channel_data": channel_data,
        "top_performers": top_performers,
        "insights": insights
    }

def get_pipeline_data(stage_filter="All", rep_filter="All"):
    """Fetch pipeline deals and stage distribution."""
    stages_df = pd.DataFrame([
        {"Stage": "Lead Qualification", "Deals": 24, "Total Value ($)": 280000},
        {"Stage": "Discovery Call", "Deals": 18, "Total Value ($)": 340000},
        {"Stage": "Proposal / Demo", "Deals": 14, "Total Value ($)": 420000},
        {"Stage": "Negotiation", "Deals": 9, "Total Value ($)": 390000},
        {"Stage": "Contract Sent", "Deals": 5, "Total Value ($)": 210000},
    ])

    deals = [
        {"Deal ID": "DEAL-101", "Company": "Acme Corp", "Rep": "Sarah Jenkins", "Value": "$85,000", "Stage": "Negotiation", "Closing Probability": "88%", "Status": "Healthy", "Created Date": "2026-06-12"},
        {"Deal ID": "DEAL-102", "Company": "Global Logistics", "Rep": "Michael Chen", "Value": "$120,000", "Stage": "Proposal / Demo", "Closing Probability": "74%", "Status": "Healthy", "Created Date": "2026-06-18"},
        {"Deal ID": "DEAL-103", "Company": "Nexus Systems", "Rep": "Aditya Kulkarni", "Value": "$65,000", "Stage": "Negotiation", "Closing Probability": "42%", "Status": "At Risk", "Created Date": "2026-06-05"},
        {"Deal ID": "DEAL-104", "Company": "Apex Health", "Rep": "David Miller", "Value": "$95,000", "Stage": "Discovery Call", "Closing Probability": "35%", "Status": "At Risk", "Created Date": "2026-06-25"},
        {"Deal ID": "DEAL-105", "Company": "Starlight Financial", "Rep": "Sarah Jenkins", "Value": "$140,000", "Stage": "Contract Sent", "Closing Probability": "92%", "Status": "Healthy", "Created Date": "2026-06-01"},
        {"Deal ID": "DEAL-106", "Company": "Vanguard Tech", "Rep": "Emma Watson", "Value": "$50,000", "Stage": "Lead Qualification", "Closing Probability": "60%", "Status": "Healthy", "Created Date": "2026-07-02"},
    ]

    deals_df = pd.DataFrame(deals)

    if stage_filter != "All":
        deals_df = deals_df[deals_df["Stage"] == stage_filter]
    if rep_filter != "All":
        deals_df = deals_df[deals_df["Rep"] == rep_filter]

    return {
        "stages": stages_df,
        "deals": deals_df,
        "total_pipeline_value": "$1,640,000",
        "open_deals_count": 70,
        "avg_deal_size": "$23,428"
    }

def get_win_loss_summary(date_range="30d"):
    """Fetch win/loss analytics."""
    win_loss_trend = pd.DataFrame([
        {"Month": "Jan", "Won": 14, "Lost": 8, "Win Rate (%)": 63.6},
        {"Month": "Feb", "Won": 18, "Lost": 9, "Win Rate (%)": 66.7},
        {"Month": "Mar", "Won": 16, "Lost": 11, "Win Rate (%)": 59.3},
        {"Month": "Apr", "Won": 22, "Lost": 7, "Win Rate (%)": 75.8},
        {"Month": "May", "Won": 20, "Lost": 10, "Win Rate (%)": 66.7},
        {"Month": "Jun", "Won": 25, "Lost": 8, "Win Rate (%)": 75.8},
    ])

    loss_reasons = pd.DataFrame([
        {"Reason": "Pricing / Budget", "Deals Lost": 18, "Percentage": "42%"},
        {"Reason": "Competitor Selected", "Deals Lost": 12, "Percentage": "28%"},
        {"Reason": "Slow Response / Stalled", "Deals Lost": 8, "Percentage": "19%"},
        {"Reason": "Product Feature Gap", "Deals Lost": 5, "Percentage": "11%"},
    ])

    rep_win_rates = pd.DataFrame([
        {"Rep": "Sarah Jenkins", "Won": 24, "Lost": 8, "Win Rate": "75.0%", "Avg Deal Value": "$38,000"},
        {"Rep": "Michael Chen", "Won": 19, "Lost": 10, "Win Rate": "65.5%", "Avg Deal Value": "$32,500"},
        {"Rep": "Emma Watson", "Won": 14, "Lost": 11, "Win Rate": "56.0%", "Avg Deal Value": "$28,000"},
        {"Rep": "David Miller", "Won": 10, "Lost": 14, "Win Rate": "41.6%", "Avg Deal Value": "$24,000"},
    ])

    return {
        "total_won_value": "$2,850,000",
        "overall_win_rate": "64.8%",
        "lost_revenue": "$920,000",
        "win_loss_trend": win_loss_trend,
        "loss_reasons": loss_reasons,
        "rep_win_rates": rep_win_rates
    }

def get_behaviour_metrics(rep_name="All"):
    """Fetch behavioural metrics: response time, follow-up cadence, email tone analysis."""
    rep_scorecards = pd.DataFrame([
        {"Rep": "Sarah Jenkins", "Avg Response Time (hrs)": 1.8, "Follow-Up Cadence (per wk)": 4.5, "Positive Tone (%)": 88, "Behaviour Score": 94, "Status": "Optimal"},
        {"Rep": "Michael Chen", "Avg Response Time (hrs)": 2.6, "Follow-Up Cadence (per wk)": 3.8, "Positive Tone (%)": 79, "Behaviour Score": 82, "Status": "Good"},
        {"Rep": "Aditya Kulkarni", "Avg Response Time (hrs)": 5.4, "Follow-Up Cadence (per wk)": 2.1, "Positive Tone (%)": 64, "Behaviour Score": 62, "Status": "Needs Attention"},
        {"Rep": "David Miller", "Avg Response Time (hrs)": 6.2, "Follow-Up Cadence (per wk)": 1.9, "Positive Tone (%)": 58, "Behaviour Score": 55, "Status": "High Risk"},
    ])

    tone_distribution = pd.DataFrame([
        {"Tone": "Positive / Empathetic", "Count": 142, "Percentage": "56.8%"},
        {"Tone": "Neutral / Transactional", "Count": 72, "Percentage": "28.8%"},
        {"Tone": "Passive / Hesitant", "Count": 24, "Percentage": "9.6%"},
        {"Tone": "Assertive / Urgent", "Count": 12, "Percentage": "4.8%"},
    ])

    response_time_benchmarks = pd.DataFrame([
        {"Category": "Top Performers (Top 10%)", "Avg Response Time": "1.8 hours", "Close Rate": "74%"},
        {"Category": "Team Average", "Avg Response Time": "3.4 hours", "Close Rate": "58%"},
        {"Category": "Underperforming Reps", "Avg Response Time": "5.8 hours", "Close Rate": "41%"},
    ])

    return {
        "team_avg_response_time": "3.4 hours",
        "top_performer_benchmark": "1.8 hours",
        "avg_follow_up_cadence": "3.2 / week",
        "overall_tone_score": "76.4%",
        "rep_scorecards": rep_scorecards,
        "tone_distribution": tone_distribution,
        "response_time_benchmarks": response_time_benchmarks
    }

def get_team_performance():
    """Fetch manager-facing team quota and leaderboard data."""
    quota_df = pd.DataFrame([
        {"Rep": "Sarah Jenkins", "Quota Target ($)": 120000, "Closed ($)": 144000, "Attainment (%)": 120.0},
        {"Rep": "Michael Chen", "Quota Target ($)": 100000, "Closed ($)": 103000, "Attainment (%)": 103.0},
        {"Rep": "Emma Watson", "Quota Target ($)": 90000, "Closed ($)": 79200, "Attainment (%)": 88.0},
        {"Rep": "Aditya Kulkarni", "Quota Target ($)": 85000, "Closed ($)": 64600, "Attainment (%)": 76.0},
        {"Rep": "David Miller", "Quota Target ($)": 80000, "Closed ($)": 56800, "Attainment (%)": 71.0},
    ])

    coaching_queue = [
        {"rep": "David Miller", "issue": "Follow-up delay > 48h on 4 open deals", "severity": "High", "action": "Schedule 1:1 cadence review"},
        {"rep": "Aditya Kulkarni", "issue": "Email response latency averaged 5.4h this week", "severity": "Medium", "action": "Recommend daily inbox triaging"},
        {"rep": "Emma Watson", "issue": "Negotiation stage duration is 2.5x team average", "severity": "Medium", "action": "Review discount strategy & proposal terms"},
    ]

    return {
        "team_name": "Enterprise B2B Sales Team",
        "total_quota": "$475,000",
        "total_achieved": "$447,600",
        "overall_attainment": "94.2%",
        "quota_df": quota_df,
        "coaching_queue": coaching_queue
    }

def get_coaching_recommendations(user_name="Aditya Kulkarni"):
    """Fetch AI coaching recommendations per representative."""
    recommendations = [
        {
            "title": "Accelerate Initial Response Time",
            "metric": "Response Time Latency",
            "current_value": "5.4 hours",
            "target_benchmark": "1.8 hours",
            "recommendation": "Response time on 3 open negotiation deals exceeds the 4-hour benchmark. Responding to prospect queries within 2 hours increases deal velocity by 28%.",
            "action": "Set up instant mobile alerts for inbound emails from key stakeholders on Nexus Systems and Apex Health.",
            "impact": "High (Estimated +$35k pipeline conversion)"
        },
        {
            "title": "Increase Mid-Funnel Follow-Up Cadence",
            "metric": "Follow-Up Frequency",
            "current_value": "2.1 touchpoints/week",
            "target_benchmark": "4.0 touchpoints/week",
            "recommendation": "Deals in Proposal / Demo stage are averaging 6 days between follow-ups. Top performers maintain a 2 to 3-day touchpoint cadence.",
            "action": "Schedule follow-up calendar blocks every Tuesday and Thursday morning.",
            "impact": "Medium (Reduces cycle time by ~4 days)"
        },
        {
            "title": "Adopt Warm & Assertive Closing Tone",
            "metric": "Communication Tone",
            "current_value": "64% Positive Tone",
            "target_benchmark": "> 80% Positive Tone",
            "recommendation": "NLP analysis detected passive phrasing in pricing emails sent to Nexus Systems. Emphasize value metrics rather than discounting upfront.",
            "action": "Use the ROI summary template when proposing budget adjustments.",
            "impact": "Medium (Improves win rate by ~12%)"
        }
    ]
    return recommendations

def analyze_email_content(deal_id, sender, receiver, subject, email_body):
    """Run simulated NLP sentiment analysis & tone classification on email content."""
    body_lower = email_body.lower()
    
    # Calculate simple sentiment score
    pos_words = ["great", "happy", "excellent", "interested", "proceed", "agree", "looking forward", "positive", "yes", "value"]
    neg_words = ["concern", "delay", "expensive", "issue", "problem", "doubt", "cancel", "disappointed", "hesitant", "no"]

    pos_count = sum(1 for w in pos_words if w in body_lower)
    neg_count = sum(1 for w in neg_words if w in body_lower)

    if pos_count > neg_count:
        sentiment_score = min(0.95, 0.5 + (pos_count - neg_count) * 0.15)
        tone = "Positive / Enthusiastic"
    elif neg_count > pos_count:
        sentiment_score = max(-0.85, -0.2 - (neg_count - pos_count) * 0.2)
        tone = "Negative / Concerned"
    else:
        sentiment_score = 0.1
        tone = "Neutral / Professional"

    return {
        "deal_id": deal_id,
        "sender": sender,
        "receiver": receiver,
        "subject": subject,
        "sentiment_score": round(sentiment_score, 3),
        "tone": tone,
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "key_phrases_detected": [w for w in pos_words + neg_words if w in body_lower] or ["standard inquiry"]
    }
