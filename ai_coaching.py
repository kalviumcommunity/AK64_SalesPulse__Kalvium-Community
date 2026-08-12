"""
SalesPulse AI Recommendation Engine Module
------------------------------------------
Implements FR-23 to FR-26:
  - Personalized AI coaching recommendations per representative
  - Automated weak metric detection (slow response time, low follow-up, tone friction)
  - Actionable advice generation with priority tagging
  - Database persistence in coaching_recommendations table
"""

from datetime import datetime
from database_manager import get_db
from behaviour_analytics import compute_rep_behaviour_metrics

def generate_coaching_recommendations_for_rep(user_id):
    """
    Evaluates representative telemetry and generates at least 3 personalized coaching tips.
    """
    metrics = compute_rep_behaviour_metrics(salesperson_id=user_id)
    if not metrics:
        return []
        
    rep_name = metrics["name"]
    resp_hrs = float(metrics["avg_response_time"])
    follow_days = float(metrics["followup_frequency"])
    sentiment = float(metrics["avg_sentiment"])
    score = float(metrics["performance_score"])
    
    recommendations = []
    
    # 1. Response Time Check
    if resp_hrs > 6.0:
        recommendations.append({
            "metric_key": "response_time",
            "issue": f"Response Time Slow ({resp_hrs} hrs vs < 4.0 hrs target)",
            "action": "Enable desktop notification alerts for inbound enterprise emails to reduce initial response delay under 2 hours.",
            "priority": "high"
        })
    else:
        recommendations.append({
            "metric_key": "response_time",
            "issue": f"Response Speed Optimal ({resp_hrs} hrs)",
            "action": "Maintain rapid response momentum. Consider sharing speed best practices during team sync.",
            "priority": "low"
        })
        
    # 2. Follow-up Cadence Check
    if follow_days > 5.0:
        recommendations.append({
            "metric_key": "followup_frequency",
            "issue": f"Follow-up Frequency Low ({follow_days} days gap between touchpoints)",
            "action": "Implement a mandatory 3-day touchpoint rule for all deals currently in Proposal/Negotiation stages.",
            "priority": "high"
        })
    else:
        recommendations.append({
            "metric_key": "followup_frequency",
            "issue": f"Follow-up Cadence Strong ({follow_days} days avg gap)",
            "action": "Ensure touchpoints add value (send case studies or ROI templates) rather than checking in passively.",
            "priority": "medium"
        })
        
    # 3. Sentiment & Tone Check
    if sentiment < 0.2:
        recommendations.append({
            "metric_key": "email_tone",
            "issue": f"Email Sentiment Low ({sentiment} NLP score)",
            "action": "Focus email communication on prospect ROI justification and positive value proposition rather than pricing friction.",
            "priority": "high"
        })
    else:
        recommendations.append({
            "metric_key": "email_tone",
            "issue": f"Communication Tone Positive ({sentiment} NLP score)",
            "action": "Leverage current positive prospect rapport to request executive sponsor involvement before next stage.",
            "priority": "medium"
        })
        
    # Persist generated recommendations to DB
    conn = get_db()
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for r in recommendations:
        cursor.execute(
            """INSERT INTO coaching_recommendations (salesperson_id, metric_key, issue_description, suggested_action, priority, created_at)
               VALUES (?, ?, ?, ?, ?, ?);""",
            (user_id, r["metric_key"], r["issue"], r["action"], r["priority"], created_at)
        )
    conn.commit()
    conn.close()
    
    return recommendations

def get_coaching_recommendations(salesperson_id):
    """Retrieve coaching recommendations for a specific sales representative."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT rec_id, metric_key, issue_description, suggested_action, priority, created_at
           FROM coaching_recommendations
           WHERE salesperson_id = ?
           ORDER BY rec_id DESC LIMIT 5;""",
        (salesperson_id,)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    
    if not rows:
        return generate_coaching_recommendations_for_rep(salesperson_id)
        
    return rows
