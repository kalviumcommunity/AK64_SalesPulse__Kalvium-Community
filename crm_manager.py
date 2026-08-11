"""
SalesPulse CRM Management Module
--------------------------------
Implements FR-05 to FR-09:
  - Customer record CRUD
  - Deal creation & stage tracking
  - Timestamped stage transition logs
  - Activity logging linked to deals
  - Full deal history retrieval
"""

import sqlite3
from datetime import datetime
from database_manager import get_db

VALID_STAGES = ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]

def create_customer(company_name, contact_person, email, phone_number=""):
    """Create a new customer company record."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (company_name, contact_person, email, phone_number) VALUES (?, ?, ?, ?);",
        (company_name.strip(), contact_person.strip(), email.strip(), phone_number.strip())
    )
    conn.commit()
    cust_id = cursor.lastrowid
    conn.close()
    return cust_id

def get_all_customers():
    """Retrieve all customer records."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, company_name, contact_person, email, phone_number FROM customers ORDER BY company_name ASC;")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def create_deal(customer_id, salesperson_id, deal_value, stage="Prospecting", status="open"):
    """Create a new deal record."""
    conn = get_db()
    cursor = conn.cursor()
    created_date = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute(
        """INSERT INTO deals (customer_id, salesperson_id, deal_value, current_stage, status, created_date, closed_date)
           VALUES (?, ?, ?, ?, ?, ?, NULL);""",
        (customer_id, salesperson_id, float(deal_value), stage, status, created_date)
    )
    conn.commit()
    deal_id = cursor.lastrowid
    
    # Log initial activity
    log_activity(deal_id, "note", f"Deal created in stage '{stage}' with value ${deal_value:,.2f}.")
    conn.close()
    return deal_id

def update_deal_stage(deal_id, new_stage, new_status=None):
    """Update deal stage and status with timestamp logging."""
    conn = get_db()
    cursor = conn.cursor()
    
    if new_status is None:
        if new_stage == "Closed Won":
            new_status = "won"
        elif new_stage == "Closed Lost":
            new_status = "lost"
        else:
            new_status = "open"
            
    closed_date = datetime.now().strftime("%Y-%m-%d") if new_status in ["won", "lost"] else None
    
    cursor.execute(
        "UPDATE deals SET current_stage = ?, status = ?, closed_date = ? WHERE deal_id = ?;",
        (new_stage, new_status, closed_date, deal_id)
    )
    conn.commit()
    
    # Log transition activity
    log_activity(deal_id, "note", f"Stage updated to '{new_stage}' (Status: {new_status}).")
    conn.close()
    return True

def log_activity(deal_id, activity_type, notes):
    """Log sales activity linked to a specific deal."""
    conn = get_db()
    cursor = conn.cursor()
    act_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute(
        "INSERT INTO activities (deal_id, activity_type, activity_date, notes) VALUES (?, ?, ?, ?);",
        (deal_id, activity_type, act_date, notes)
    )
    conn.commit()
    conn.close()
    return True

def get_deals_with_details(salesperson_id=None):
    """Fetch deals joined with customer and salesperson details."""
    conn = get_db()
    cursor = conn.cursor()
    
    query = """
    SELECT d.deal_id, c.company_name, c.contact_person, u.name as owner, u.user_id as salesperson_id,
           d.deal_value, d.current_stage, d.status, d.created_date, d.closed_date
    FROM deals d
    JOIN customers c ON d.customer_id = c.customer_id
    JOIN users u ON d.salesperson_id = u.user_id
    """
    
    params = []
    if salesperson_id:
        query += " WHERE d.salesperson_id = ?"
        params.append(salesperson_id)
        
    query += " ORDER BY d.created_date DESC;"
    
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_deal_history(deal_id):
    """Retrieve full activity and email history for a specific deal."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT activity_type, activity_date, notes FROM activities WHERE deal_id = ? ORDER BY activity_date DESC;", (deal_id,))
    activities = [dict(r) for r in cursor.fetchall()]
    
    cursor.execute("SELECT sender, receiver, subject, email_body, sentiment_score, tone, sent_timestamp FROM emails WHERE deal_id = ? ORDER BY sent_timestamp DESC;", (deal_id,))
    emails = [dict(r) for r in cursor.fetchall()]
    
    conn.close()
    return {"activities": activities, "emails": emails}
