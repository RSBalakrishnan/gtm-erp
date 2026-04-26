#!/usr/bin/env python3
"""
Process Outreach — Batch processor for sending drafted emails from Google Sheet.
Part of the email-sender skill for the Outreach Writer agent.
"""
import json
import time
import sys
import os
from dotenv import load_dotenv

# Load .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', '.env')
if not os.path.exists(env_path):
    env_path = '/app/.env'
load_dotenv(env_path)

# Add gsheet-manager from orchestrator (shared dependency)
# Load config and db-manager
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', 'config')
sys.path.insert(0, config_path)

from gsheets_helper import GSheetsHelper
from email_sender import send_email
from campaign_context import load_campaign_context


def process_outreach(campaign_id=None, row_index=None, limit=5):
    """Find targets ready for outreach and send drafted emails."""
    # Load Campaign Context
    try:
        ctx = load_campaign_context(campaign_id)
    except Exception as e:
        print(f"❌ Could not load campaign context: {e}")
        return

    helper = GSheetsHelper()
    rows = helper.get_all_rows(force_refresh=True)

    if not rows or len(rows) < 4:
        print("❌ Sheet empty or invalid.")
        return

    header = rows[2]
    col_map = {name: i for i, name in enumerate(header)}

    email_col = col_map.get('Emails')
    status_col = col_map.get('Status')
    draft_col = col_map.get('Email 1')
    sent_col = col_map.get('Email 1 Sent')
    tracking_id_col = col_map.get('Tracking ID')
    pixel_col = col_map.get('Pixel URL')
    target_col = col_map.get('Target Name') or col_map.get('College Name')

    if None in [email_col, status_col, draft_col, sent_col]:
        print("❌ Required outreach columns missing.")
        return

    processed = 0
    start_idx = row_index - 1 if row_index else 4
    end_idx = row_index if row_index else len(rows)

    for i in range(start_idx, end_idx):
        row = rows[i]
        status = row[status_col].strip().lower() if len(row) > status_col else "open"
        already_sent = row[sent_col].strip().upper() == "TRUE" if len(row) > sent_col else False

        if (status in ["ready_for_outreach", "sent"]) and not already_sent:
            to_email = row[email_col].split(",")[0].strip() if len(row) > email_col else ""
            target_name = row[target_col] if len(row) > target_col else "Institution"
            draft = row[draft_col] if len(row) > draft_col else ""
            tracking_id = row[tracking_id_col] if len(row) > tracking_id_col else ""
            pixel_url = row[pixel_col] if len(row) > pixel_col else ""

            if not to_email or not draft:
                print(f"⏩ Skipping Row {i+1}: Missing email or draft.")
                continue

            # Generate Dynamic Subject
            subject = ctx.subject_line_template.replace("{{target_name}}", target_name)
            if not subject:
                subject = f"Following up with {target_name}"

            print(f"📧 Sending to {target_name} ({to_email})...")
            success, msg = send_email(to_email, subject, draft, pixel_url, tracking_id)

            if success:
                print(f"✅ {msg}")
                row_update = list(row) + [""] * (len(header) - len(row))
                row_update[sent_col] = "TRUE"
                row_update[status_col] = "outreach_sent"
                ts_col = col_map.get('Email 1 Sent Timestamp')
                if ts_col:
                    row_update[ts_col] = time.strftime("%Y-%m-%d %H:%M:%S")
                helper.update_row(i + 1, row_update)
                processed += 1
            else:
                print(f"❌ Failed Row {i+1}: {msg}")

            if processed >= limit and not row_index:
                break
            time.sleep(2)

    print(f"\n✨ Outreach complete. Emails sent: {processed}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Process and send outreach emails")
    parser.add_argument("--campaign", type=str, help="Campaign ID")
    parser.add_argument("--row", type=int, help="Target a specific row")
    parser.add_argument("--limit", type=int, default=5, help="Max emails to send")
    args = parser.parse_args()
    process_outreach(campaign_id=args.campaign, row_index=args.row, limit=args.limit)
