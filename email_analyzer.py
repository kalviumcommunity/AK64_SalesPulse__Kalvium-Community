"""
SalesPulse NLP Email Analysis Module
------------------------------------
Implements FR-10 to FR-13:
  - Upload and storage of email conversations linked to deals
  - NLP sentiment scoring (-1.0 to +1.0)
  - Tone classification (positive, assertive, passive, negative)
  - Sentiment trend evaluation over deal lifespans
"""

import re
from datetime import datetime
from database_manager import get_db

# Rule-based / NLP Lexicon Sentiment Analyzer Fallback
POSITIVE_WORDS = {"great", "excellent", "impressive", "approved", "love", "awesome", "good", "positive", "strong", "valuable", "seamless", "perfect", "deal", "excited"}
NEGATIVE_WORDS = {"delay", "issue", "problem", "expensive", "cancel", "stalled", "budget", "objection", "poor", "slow", "risk", "difficult", "unhappy", "concern"}
ASSERTIVE_WORDS = {"contract", "terms", "deadline", "agreement", "pricing", "discount", "requirement", "must", "confirm", "decision"}
PASSIVE_WORDS = {"maybe", "evaluating", "checking", "later", "next quarter", "considering", "tentative", "might"}

def analyze_text_nlp(text):
    """
    Computes sentiment score (-1.0 to +1.0) and detects tone classification.
    """
    if not text:
        return 0.0, "passive"
        
    words = [w.lower().strip(".,!?\"'") for w in text.split()]
    total_words = max(len(words), 1)
    
    pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)
    assertive_count = sum(1 for w in words if w in ASSERTIVE_WORDS)
    passive_count = sum(1 for w in words if w in PASSIVE_WORDS)
    
    # Calculate score
    score = (pos_count - neg_count) / max(pos_count + neg_count, 1)
    score = round(max(-1.0, min(1.0, score)), 2)
    
    # Classify tone
    if score > 0.3:
        tone = "positive"
    elif score < -0.2:
        tone = "negative"
    elif assertive_count >= passive_count:
        tone = "assertive"
    else:
        tone = "passive"
        
    return score, tone

def upload_and_analyze_email(deal_id, sender, receiver, subject, email_body, sent_timestamp=None):
    """Store email and run sentiment & tone analysis."""
    if sent_timestamp is None:
        sent_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    score, tone = analyze_text_nlp(f"{subject} {email_body}")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO emails (deal_id, sender, receiver, subject, email_body, sentiment_score, tone, sent_timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
        (deal_id, sender.strip(), receiver.strip(), subject.strip(), email_body.strip(), score, tone, sent_timestamp)
    )
    conn.commit()
    email_id = cursor.lastrowid
    conn.close()
    
    return {
        "email_id": email_id,
        "deal_id": deal_id,
        "sentiment_score": score,
        "tone": tone
    }

def get_deal_sentiment_summary(deal_id):
    """Returns aggregated sentiment metrics for a deal."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sentiment_score, tone FROM emails WHERE deal_id = ?;", (deal_id,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return {"avg_sentiment": 0.0, "dominant_tone": "neutral", "count": 0}
        
    scores = [r["sentiment_score"] for r in rows]
    tones = [r["tone"] for r in rows]
    
    avg_score = round(sum(scores) / len(scores), 2)
    dominant_tone = max(set(tones), key=tones.count)
    
    return {
        "avg_sentiment": avg_score,
        "dominant_tone": dominant_tone,
        "count": len(rows)
    }
