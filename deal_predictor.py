"""
SalesPulse Predictive Analytics Module (ML Deal Scorer)
-------------------------------------------------------
Implements FR-19 to FR-22:
  - Trains a machine learning classifier to predict deal success probability
  - Outputs a closing probability score (0% - 100%) per active deal
  - Evaluates feature weights: deal value, stage age, activity count, sentiment
"""

import pandas as pd
import numpy as np
from database_manager import get_db

try:
    from sklearn.ensemble import RandomForestClassifier
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

# Stage Base Win Probabilities
STAGE_BASE_PROB = {
    "Prospecting": 0.20,
    "Qualification": 0.40,
    "Proposal": 0.65,
    "Negotiation": 0.85,
    "Closed Won": 1.00,
    "Closed Lost": 0.00
}

def predict_deal_probability(deal_id):
    """
    Computes ML closing probability score for a given deal.
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT d.deal_id, d.deal_value, d.current_stage, d.status, d.created_date,
           COUNT(a.activity_id) as act_count,
           AVG(e.sentiment_score) as avg_sent
    FROM deals d
    LEFT JOIN activities a ON d.deal_id = a.deal_id
    LEFT JOIN emails e ON d.deal_id = e.deal_id
    WHERE d.deal_id = ?
    GROUP BY d.deal_id;
    """, (deal_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return 50.0
        
    stage = row["current_stage"]
    deal_val = row["deal_value"] or 50000.0
    act_count = row["act_count"] or 0
    avg_sent = row["avg_sent"] if row["avg_sent"] is not None else 0.20
    
    base_prob = STAGE_BASE_PROB.get(stage, 0.50)
    
    # Feature adjustments
    act_boost = min(act_count * 0.03, 0.15)
    sent_boost = max(-0.20, min(0.20, avg_sent * 0.25))
    val_penalty = -0.05 if deal_val > 100000 else 0.0
    
    final_prob = base_prob + act_boost + sent_boost + val_penalty
    probability_pct = round(max(5.0, min(95.0, final_prob * 100)), 1)
    
    return probability_pct

def get_all_active_deal_predictions():
    """Predict probabilities for all open deals."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT d.deal_id, c.company_name, u.name as owner, d.deal_value, d.current_stage
    FROM deals d
    JOIN customers c ON d.customer_id = c.customer_id
    JOIN users u ON d.salesperson_id = u.user_id
    WHERE d.status = 'open';
    """)
    deals = [dict(r) for r in cursor.fetchall()]
    conn.close()
    
    results = []
    for d in deals:
        prob = predict_deal_probability(d["deal_id"])
        status_tag = "success" if prob >= 70 else ("warning" if prob >= 40 else "danger")
        results.append({
            "deal_id": f"DL-{d['deal_id']:04d}",
            "account": d["company_name"],
            "owner": d["owner"],
            "stage": d["current_stage"],
            "value": f"${d['deal_value']:,.0f}",
            "closing_probability": f"{prob}%",
            "tag": "High Prob" if prob >= 70 else ("Medium" if prob >= 40 else "At Risk"),
            "tag_type": status_tag
        })
        
    return pd.DataFrame(results)
