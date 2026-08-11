"""
SalesPulse PRD Database Manager
-------------------------------
Implements the exact 5 core PRD relational tables from Appendix B:
  1. Users (user_id, name, email, password_hash, role)
  2. Customers (customer_id, company_name, contact_person, email, phone_number)
  3. Deals (deal_id, customer_id, salesperson_id, deal_value, current_stage, status, created_date, closed_date)
  4. Activities (activity_id, deal_id, activity_type, activity_date, notes)
  5. Emails (email_id, deal_id, sender, receiver, subject, email_body, sentiment_score, tone, sent_timestamp)
  6. CoachingRecommendations (rec_id, salesperson_id, metric_key, issue_description, suggested_action, priority, created_at)
"""

import sqlite3
import os
import hashlib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "salespulse_prd.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_db():
    """Create all PRD tables if they don't exist and seed initial demo data."""
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('rep', 'manager', 'admin'))
    );
    """)
    
    # 2. Customers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        contact_person TEXT NOT NULL,
        email TEXT NOT NULL,
        phone_number TEXT
    );
    """)
    
    # 3. Deals Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deals (
        deal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        salesperson_id INTEGER NOT NULL,
        deal_value REAL NOT NULL,
        current_stage TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('open', 'won', 'lost')),
        created_date TEXT NOT NULL,
        closed_date TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (salesperson_id) REFERENCES users(user_id)
    );
    """)
    
    # 4. Activities Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        deal_id INTEGER NOT NULL,
        activity_type TEXT NOT NULL CHECK(activity_type IN ('call', 'email', 'meeting', 'note')),
        activity_date TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (deal_id) REFERENCES deals(deal_id)
    );
    """)
    
    # 5. Emails Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        email_id INTEGER PRIMARY KEY AUTOINCREMENT,
        deal_id INTEGER NOT NULL,
        sender TEXT NOT NULL,
        receiver TEXT NOT NULL,
        subject TEXT NOT NULL,
        email_body TEXT NOT NULL,
        sentiment_score REAL NOT NULL,
        tone TEXT NOT NULL CHECK(tone IN ('positive', 'assertive', 'passive', 'negative')),
        sent_timestamp TEXT NOT NULL,
        FOREIGN KEY (deal_id) REFERENCES deals(deal_id)
    );
    """)
    
    # 6. Coaching Recommendations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coaching_recommendations (
        rec_id INTEGER PRIMARY KEY AUTOINCREMENT,
        salesperson_id INTEGER NOT NULL,
        metric_key TEXT NOT NULL,
        issue_description TEXT NOT NULL,
        suggested_action TEXT NOT NULL,
        priority TEXT NOT NULL CHECK(priority IN ('high', 'medium', 'low')),
        created_at TEXT NOT NULL,
        FOREIGN KEY (salesperson_id) REFERENCES users(user_id)
    );
    """)
    
    conn.commit()
    
    # Check users count and seed all 4 PRD Personas
    cursor.execute("SELECT COUNT(*) FROM users;")
    if cursor.fetchone()[0] == 0:
        seed_prd_data(conn)
        
    conn.close()

def seed_prd_data(conn):
    cursor = conn.cursor()
    pw = hash_password("password123")
    
    # PRD Personas (Section 3 of PRD)
    users = [
        ("Aditya Kulkarni", "aditya@salespulse.ai", pw, "rep"),
        ("Sarah Jenkins", "sarah@salespulse.ai", pw, "rep"),
        ("David Miller", "david@salespulse.ai", pw, "rep"),
        ("Michael Chang", "michael@salespulse.ai", pw, "rep"),
        ("Elena Rostova", "elena@salespulse.ai", pw, "rep"),
        ("Meera Nair", "meera@salespulse.ai", pw, "manager"),
        ("Rohan Bhatt", "rohan@salespulse.ai", pw, "admin"),
        ("Ishita Ghosh", "ishita@salespulse.ai", pw, "admin")
    ]
    cursor.executemany("INSERT OR IGNORE INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?);", users)
    
    # Customers
    customers = [
        ("Acme Corp", "John Smith", "john@acme.com", "+1-555-0192"),
        ("GlobalTech Inc", "Mark Lee", "mlee@globaltech.com", "+1-555-0183"),
        ("Nexus Media", "David Ross", "dross@nexus.com", "+1-555-0144"),
        ("Apex Dynamics", "Rachel Davis", "rdavis@apexdyn.com", "+1-555-0175"),
        ("Summit Financial", "Kiran Patel", "kpatel@summit.com", "+1-555-0166"),
        ("Vanguard Tech", "Lisa Wong", "lwong@vanguard.com", "+1-555-0199")
    ]
    cursor.executemany("INSERT INTO customers (company_name, contact_person, email, phone_number) VALUES (?, ?, ?, ?);", customers)
    
    # Deals
    deals = [
        (1, 1, 125000.0, "Negotiation", "open", "2024-07-01", None),
        (2, 2, 85000.0, "Proposal", "open", "2024-07-05", None),
        (3, 3, 45000.0, "Qualification", "open", "2024-07-10", None),
        (4, 4, 110000.0, "Negotiation", "open", "2024-06-15", None),
        (5, 1, 95000.0, "Closed Won", "won", "2024-05-10", "2024-06-20"),
        (6, 2, 60000.0, "Closed Lost", "lost", "2024-05-15", "2024-06-25")
    ]
    cursor.executemany("INSERT INTO deals (customer_id, salesperson_id, deal_value, current_stage, status, created_date, closed_date) VALUES (?, ?, ?, ?, ?, ?, ?);", deals)
    
    # Activities
    activities = [
        (1, "call", "2024-07-02 10:30:00", "Discovery call completed with CTO. Strong interest in AI modules."),
        (1, "email", "2024-07-03 14:15:00", "Sent customized proposal and enterprise pricing sheet."),
        (1, "meeting", "2024-07-12 11:00:00", "Executive demo session with VP of Sales."),
        (2, "call", "2024-07-06 09:45:00", "Initial qualification phone conversation."),
        (2, "email", "2024-07-08 16:20:00", "Follow-up email sent regarding security compliance."),
        (3, "email", "2024-07-11 13:10:00", "Initial outreach email. Awaiting client response."),
        (4, "meeting", "2024-06-20 15:00:00", "Security architecture review meeting with Infosec lead.")
    ]
    cursor.executemany("INSERT INTO activities (deal_id, activity_type, activity_date, notes) VALUES (?, ?, ?, ?);", activities)
    
    # Emails
    emails = [
        (1, "john@acme.com", "sarah@salespulse.ai", "Re: Enterprise Proposal & AI Capability", "We reviewed the proposal. The AI analytics capabilities look very impressive and fit our roadmap well.", 0.85, "positive", "2024-07-03 15:20:00"),
        (1, "sarah@salespulse.ai", "john@acme.com", "Re: Contract Terms & Final Approval", "I have attached the updated contract with the 10% multi-year discount as requested.", 0.65, "assertive", "2024-07-13 09:10:00"),
        (2, "mlee@globaltech.com", "david@salespulse.ai", "Security Questionnaire Followup", "Can you send over your latest SOC2 Type II audit report for our compliance review?", 0.20, "passive", "2024-07-09 11:45:00"),
        (3, "dross@nexus.com", "michael@salespulse.ai", "Re: Intro Call Scheduling", "We are currently evaluating budget constraints and might delay this project until Q4.", -0.40, "negative", "2024-07-12 16:30:00"),
        (4, "rdavis@apexdyn.com", "elena@salespulse.ai", "Pricing Objections", "Your competitor offered a 25% lower price point. We need to see significant justification.", -0.35, "negative", "2024-06-22 14:15:00")
    ]
    cursor.executemany("INSERT INTO emails (deal_id, sender, receiver, subject, email_body, sentiment_score, tone, sent_timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", emails)
    
    # Coaching Recommendations
    recs = [
        (4, "response_time", "Average response time is 14.2 hours (benchmark is < 4 hours).", "Set automated email notifications and reduce follow-up delay on active proposals.", "high", "2024-07-14 10:00:00"),
        (4, "email_sentiment", "Email tone in recent deal threads detected as negative/defensive (-0.35 score).", "Adopt consultative objection-handling templates focusing on ROI rather than price defense.", "high", "2024-07-14 10:00:00"),
        (3, "followup_frequency", "Follow-up frequency has dropped to 1 activity every 12 days.", "Schedule a 15-minute check-in call with Nexus Media account sponsor.", "medium", "2024-07-14 10:00:00")
    ]
    cursor.executemany("INSERT INTO coaching_recommendations (salesperson_id, metric_key, issue_description, suggested_action, priority, created_at) VALUES (?, ?, ?, ?, ?, ?);", recs)
    
    conn.commit()

# --- Legacy View Query Helpers ---
def fetch_pipeline_data(start_date=None, end_date=None, segment="All"):
    stages = [
        {"stage": "1. Prospecting", "count": 142, "value": 425000, "conversion": "100%", "avg_days": 4},
        {"stage": "2. Qualification", "count": 98, "value": 340000, "conversion": "69%", "avg_days": 8},
        {"stage": "3. Proposal", "count": 64, "value": 285000, "conversion": "65%", "avg_days": 12},
        {"stage": "4. Negotiation", "count": 38, "value": 195000, "conversion": "59%", "avg_days": 15},
        {"stage": "5. Closed Won", "count": 29, "value": 162000, "conversion": "76%", "avg_days": 21},
    ]
    df_stages = pd.DataFrame(stages)
    deals = [
        {"deal_id": "DL-9041", "account": "Acme Corp", "owner": "Sarah Jenkins", "stage": "Negotiation", "amount": "$45,000", "probability": "85%", "close_date": "2024-08-25", "status": "At Risk"},
        {"deal_id": "DL-9042", "account": "GlobalTech Inc", "owner": "Michael Chang", "stage": "Proposal", "amount": "$78,000", "probability": "60%", "close_date": "2024-09-02", "status": "On Track"},
        {"deal_id": "DL-9043", "account": "Nexus Media", "owner": "Elena Rostova", "stage": "Qualification", "amount": "$32,000", "probability": "40%", "close_date": "2024-09-15", "status": "Needs Attention"},
        {"deal_id": "DL-9044", "account": "Apex Dynamics", "owner": "David Miller", "stage": "Negotiation", "amount": "$110,000", "probability": "90%", "close_date": "2024-08-28", "status": "On Track"},
        {"deal_id": "DL-9045", "account": "Summit Financial", "owner": "Sarah Jenkins", "stage": "Proposal", "amount": "$55,000", "probability": "70%", "close_date": "2024-09-10", "status": "High Priority"},
    ]
    df_deals = pd.DataFrame(deals)
    insights = [
        {"title": "Qualification Bottleneck Detected", "desc": "34% of deals are stuck in Qualification stage longer than 10 days.", "category": "Pipeline Health", "tag": "High Risk", "tag_type": "danger"},
        {"title": "Proposal-to-Negotiation Velocity Up 14%", "desc": "Enterprise deals moving 2.3 days faster following new pricing template.", "category": "Velocity", "tag": "Positive", "tag_type": "success"},
        {"title": "Negotiation Value Concentrated in Top 3 Reps", "desc": "68% of Q3 negotiation value is held by Sarah Jenkins & David Miller.", "category": "Capacity", "tag": "Attention", "tag_type": "warning"}
    ]
    return df_stages, df_deals, insights

def fetch_sales_performance(start_date=None, end_date=None, segment="All"):
    metrics = {"total_revenue": "$1,407,000", "quota_attainment": "94.2%", "avg_deal_size": "$42,850", "yoy_growth": "+18.4%"}
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    revenue = [85000, 92000, 105000, 98000, 115000, 128000, 140000, 135000, 150000, 162000, 155000, 180000]
    target = [90000, 90000, 100000, 100000, 110000, 120000, 130000, 130000, 140000, 150000, 150000, 160000]
    df_trend = pd.DataFrame({"Month": months, "Revenue": revenue, "Target": target})
    table_data = [
        {"segment": "Enterprise Solutions", "deals_closed": 48, "revenue": "$680,000", "aov": "$14,166", "win_rate": "38.2%", "growth": "+22.1%", "status": "Strong Growth"},
        {"segment": "Mid-Market SaaS", "deals_closed": 112, "revenue": "$448,000", "aov": "$4,000", "win_rate": "31.5%", "growth": "+14.8%", "status": "On Target"},
        {"segment": "SMB Core", "deals_closed": 210, "revenue": "$210,000", "aov": "$1,000", "win_rate": "24.8%", "growth": "+5.2%", "status": "Lagging"},
        {"segment": "Custom Services", "deals_closed": 15, "revenue": "$195,000", "aov": "$13,000", "win_rate": "42.0%", "growth": "+31.0%", "status": "High Margin"}
    ]
    return metrics, df_trend, pd.DataFrame(table_data)

def fetch_win_loss_data(start_date=None, end_date=None, segment="All"):
    chart_data = pd.DataFrame({
        "Category": ["Closed Won", "Lost to Competitor", "Lost to No Decision", "Budget Cancelled"],
        "Count": [142, 68, 45, 22],
        "Percentage": ["51.3%", "24.5%", "16.2%", "7.9%"]
    })
    win_drivers = [
        {"rank": 1, "driver": "Superior AI Analytics & Reporting Feature Set", "impact": "+34% Win Rate Contribution", "tag": "Positive Match", "tag_type": "success"},
        {"rank": 2, "driver": "Strong ROI / TCO Demonstration in Demo", "impact": "+28% Win Rate Contribution", "tag": "Value Proven", "tag_type": "success"},
        {"rank": 3, "driver": "Flexible Enterprise Security & SOC2 Compliance", "impact": "+22% Win Rate Contribution", "tag": "Compliance Pass", "tag_type": "success"},
        {"rank": 4, "driver": "Executive Sponsor Involvement by Week 2", "impact": "+19% Win Rate Contribution", "tag": "Exec Buy-in", "tag_type": "success"},
        {"rank": 5, "driver": "Competitor Price Discounting (20%+ undercut)", "impact": "-25% Loss Cause", "tag": "Price Friction", "tag_type": "danger"}
    ]
    deals_table = pd.DataFrame([
        {"deal": "Vanguard Tech", "value": "$95,000", "outcome": "Won", "competitor": "Salesforce", "primary_reason": "AI Feature Superiority", "cycle_days": 34, "tag": "Closed Won", "tag_type": "success"},
        {"deal": "Horizon Logistics", "value": "$62,000", "outcome": "Lost", "competitor": "HubSpot", "primary_reason": "Price Sensitivity", "cycle_days": 48, "tag": "Closed Lost", "tag_type": "danger"},
        {"deal": "Pinnacle Health", "value": "$120,000", "outcome": "Won", "competitor": "Gong.io", "primary_reason": "Security & On-Prem Options", "cycle_days": 29, "tag": "Closed Won", "tag_type": "success"},
        {"deal": "Starlight Retail", "value": "$45,000", "outcome": "Lost", "competitor": "None (No Dec)", "primary_reason": "Budget Freeze", "cycle_days": 65, "tag": "Stalled", "tag_type": "warning"},
        {"deal": "Atlas Energy", "value": "$88,000", "outcome": "Won", "competitor": "Clari", "primary_reason": "Seamless CRM Integration", "cycle_days": 41, "tag": "Closed Won", "tag_type": "success"}
    ])
    return chart_data, win_drivers, deals_table

def fetch_behaviour_data(start_date=None, end_date=None, segment="All"):
    summary_metrics = pd.DataFrame([
        {"metric": "Monthly Active Users (MAU)", "value": "12,480", "benchmark": "10,000 target", "trend": "+12.4%", "status": "Optimal", "tag_type": "success"},
        {"metric": "Average Session Duration", "value": "24m 15s", "benchmark": "18m benchmark", "trend": "+8.1%", "status": "High Engagement", "tag_type": "success"},
        {"metric": "Feature Adoption Rate (AI Insights)", "value": "78.4%", "benchmark": "65% goal", "trend": "+15.2%", "status": "Strong Adopt", "tag_type": "success"},
        {"metric": "Customer Satisfaction (CSAT)", "value": "4.8 / 5.0", "benchmark": "4.5 minimum", "trend": "+0.3 pts", "status": "Excellent", "tag_type": "success"},
        {"metric": "High Churn Risk Accounts", "value": "14 Accounts", "benchmark": "< 10 target", "trend": "-2 accounts", "status": "Requires Review", "tag_type": "warning"}
    ])
    event_log = pd.DataFrame([
        {"account": "Acme Corp", "user_email": "j.smith@acme.com", "event": "Exported Custom Sales Dashboard", "timestamp": "2024-08-11 14:22", "usage_tier": "Power User", "health_score": "95/100", "status": "Healthy", "tag_type": "success"},
        {"account": "GlobalTech", "user_email": "m.lee@globaltech.com", "event": "Triggered Pipeline Alert Email", "timestamp": "2024-08-11 13:58", "usage_tier": "Core Admin", "health_score": "88/100", "status": "Active", "tag_type": "success"},
        {"account": "Apex Dynamics", "user_email": "r.davis@apexdyn.com", "event": "No login for 14 consecutive days", "timestamp": "2024-08-11 11:15", "usage_tier": "At Risk", "health_score": "42/100", "status": "Inactivity Risk", "tag_type": "danger"},
        {"account": "Summit Financial", "user_email": "k.patel@summit.com", "event": "Invited 5 New Team Members", "timestamp": "2024-08-11 09:40", "usage_tier": "Expansion", "health_score": "98/100", "status": "Expanding", "tag_type": "success"},
        {"account": "Nexus Media", "user_email": "d.ross@nexus.com", "event": "Failed Export Attempt (Quota Limit)", "timestamp": "2024-08-10 16:50", "usage_tier": "Standard", "health_score": "71/100", "status": "Support Needed", "tag_type": "warning"}
    ])
    return summary_metrics, event_log

def fetch_team_performance(start_date=None, end_date=None, segment="All"):
    reps_data = [
        {"id": 1, "name": "Sarah Jenkins", "role": "Senior Enterprise AE", "quota": "$250,000", "closed": "$285,000", "attainment": "114%", "deals": 18, "avg_cycle": "24 days", "activity_score": 96, "status": "Top Performer", "tag_type": "success", "avatar": "👩‍💼"},
        {"id": 2, "name": "David Miller", "role": "Enterprise AE", "quota": "$220,000", "closed": "$215,000", "attainment": "97.7%", "deals": 14, "avg_cycle": "28 days", "activity_score": 91, "status": "On Track", "tag_type": "success", "avatar": "👨‍💼"},
        {"id": 3, "name": "Michael Chang", "role": "Mid-Market AE", "quota": "$180,000", "closed": "$162,000", "attainment": "90%", "deals": 22, "avg_cycle": "19 days", "activity_score": 85, "status": "Solid", "tag_type": "info", "avatar": "👨‍💻"},
        {"id": 4, "name": "Elena Rostova", "role": "Mid-Market AE", "quota": "$180,000", "closed": "$135,000", "attainment": "75%", "deals": 16, "avg_cycle": "32 days", "activity_score": 72, "status": "Needs Coaching", "tag_type": "warning", "avatar": "👩‍💻"},
        {"id": 5, "name": "Alex Thompson", "role": "Commercial AE", "quota": "$150,000", "closed": "$95,000", "attainment": "63.3%", "deals": 12, "avg_cycle": "38 days", "activity_score": 64, "status": "At Risk", "tag_type": "danger", "avatar": "👨‍💼"}
    ]
    df_reps = pd.DataFrame(reps_data)
    rep_details = {
        1: {
            "name": "Sarah Jenkins", "role": "Senior Enterprise AE", "attainment": "114%", "revenue": "$285,000", "deals_won": 18, "pipeline_held": "$420,000", "win_rate": "54.5%",
            "strengths": ["Executive Pitching", "AI Demo Excellence"],
            "coaching_notes": "Exceeding target consistently. Ready to assist onboarding new AE cohort.",
            "risk_flags": "High workload risk due to 12 active enterprise deals.",
            "recommended_action": "Schedule Q4 territory expansion review."
        },
        2: {
            "name": "David Miller", "role": "Enterprise AE", "attainment": "97.7%", "revenue": "$215,000", "deals_won": 14, "pipeline_held": "$310,000", "win_rate": "48.2%",
            "strengths": ["Technical Discovery", "ROI Calculation"],
            "coaching_notes": "Strong technical execution.",
            "risk_flags": "Slight slippage on deal close dates.",
            "recommended_action": "Provide legal closing support."
        },
        3: {
            "name": "Michael Chang", "role": "Mid-Market AE", "attainment": "90%", "revenue": "$162,000", "deals_won": 22, "pipeline_held": "$240,000", "win_rate": "42.0%",
            "strengths": ["High Activity Volume", "Rapid Follow-up"],
            "coaching_notes": "Great transactional momentum.",
            "risk_flags": "Low executive sponsor attendance.",
            "recommended_action": "Conduct executive engagement workshop."
        },
        4: {
            "name": "Elena Rostova", "role": "Mid-Market AE", "attainment": "75%", "revenue": "$135,000", "deals_won": 16, "pipeline_held": "$190,000", "win_rate": "34.8%",
            "strengths": ["Relationship Building"],
            "coaching_notes": "Deals stalling in Proposal stage due to price objections.",
            "risk_flags": "Win rate down 8% compared to Q2 baseline.",
            "recommended_action": "Assign 1-on-1 objection handling roleplay session."
        },
        5: {
            "name": "Alex Thompson", "role": "Commercial AE", "attainment": "63.3%", "revenue": "$95,000", "deals_won": 12, "pipeline_held": "$140,000", "win_rate": "28.5%",
            "strengths": ["Outbound Cold Calling"],
            "coaching_notes": "High activity level but low conversion.",
            "risk_flags": "Pipelined value below quota requirement.",
            "recommended_action": "Implement mandatory deal review checklist."
        }
    }
    return df_reps, rep_details

# Ensure DB is initialized upon module load
init_db()
