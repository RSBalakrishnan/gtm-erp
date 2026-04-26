#!/usr/bin/env python3
"""
Email Sender — SMTP sender with tracking pixel injection.
Part of the email-sender skill for the Outreach Writer agent.
"""
import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', '.env')
if not os.path.exists(env_path):
    env_path = '/app/.env'
load_dotenv(env_path)

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")


def send_email(to_email, subject, body_plain, pixel_url=None, tracking_id=None):
    """Send a tracked HTML email via SMTP with invisible tracking pixel."""
    if not SMTP_USER or not SMTP_PASSWORD:
        return False, "SMTP credentials missing in .env"

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email

        # Convert plain text to HTML
        html_content = body_plain.replace("\n", "<br>")

        # Inject tracking pixel (MANDATORY for open tracking)
        if pixel_url:
            html_content += f'<br><br><img src="{pixel_url}" width="1" height="1" style="display:none" />'

        part1 = MIMEText(body_plain, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, to_email, msg.as_string())

        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_email = sys.argv[2] if len(sys.argv) > 2 else "test@example.com"
        print(f"🚀 Sending test email to {test_email}...")
        success, msg = send_email(
            test_email,
            "GTM V4 SMTP Test",
            "This is a test of the V4 automated SMTP outreach system.\n\nIf you see this, the connection is working!",
            pixel_url=os.getenv("TEST_PIXEL_URL")
        )
        print(f"{'✅' if success else '❌'} {msg}")
    else:
        print("Usage: python3 email_sender.py --test <email>")
