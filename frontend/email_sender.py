"""
SalesPulse Email Delivery Module
--------------------------------
Assignment 2.57 - Task 2, Task 4 & Task 5: SMTPLib Email Dispatch
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_report_email(report_text, recipient, subject="Weekly SalesPulse Analytics Report"):
    """
    Send structured report via email using smtplib.

    Args:
        report_text (str): Report body text
        recipient (str): Recipient email address
        subject (str): Email subject header

    Returns:
        bool: True if email sent successfully, False otherwise (non-blocking)
    """
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))

    if not sender_email or not sender_password:
        print("[EMAIL DISPATCH] Credentials not configured in environment variables (SENDER_EMAIL, SENDER_PASSWORD). Skipping send.")
        return False

    if not recipient:
        print("[EMAIL DISPATCH] Recipient email is empty. Skipping send.")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(report_text, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print(f"[EMAIL DISPATCH] Report successfully delivered to {recipient}")
        return True

    except Exception as e:
        print(f"[EMAIL DISPATCH ERROR] Email send failed: {e}")
        return False


def send_report(report_text, recipient):
    return send_report_email(report_text, recipient)
