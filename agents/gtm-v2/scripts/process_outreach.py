#!/usr/bin/env python3
import json
import time
import sys
import os
from gsheets_helper import GSheetsHelper
from email_sender import send_email

def process_outreach(row_index=None, limit=5):
    """
    Finds leads ready for outreach and sends the drafted emails.
    """
    helper = GSheetsHelper()
    rows = helper.get_all_rows(force_refresh=True)
    
    if not rows or len(rows) < 4:
        print("Error: Sheet empty or invalid.")
        return

    header = rows[2]
    col_map = {name: i for i, name in enumerate(header)}
    
    # Required columns
    email_col = col_map.get('Emails')
    status_col = col_map.get('Status')
    draft_col = col_map.get('Email 1')
    sent_col = col_map.get('Email 1 Sent')
    tracking_id_col = col_map.get('Tracking ID')
    pixel_col = col_map.get('Pixel URL')
    college_col = col_map.get('College Name')

    if None in [email_col, status_col, draft_col, sent_col]:
        print("Error: Required outreach columns missing in sheet.")
        return

    processed_count = 0
    start_idx = row_index - 1 if row_index else 4
    end_idx = row_index if row_index else len(rows)

    for i in range(start_idx, end_idx):
        row = rows[i]
        
        # Skip if already sent or not ready
        status = row[status_col].strip().lower() if len(row) > status_col else "open"
        already_sent = row[sent_col].strip().upper() == "TRUE" if len(row) > sent_col else False
        
        if (status == "ready_for_outreach" or status == "sent") and not already_sent:
            to_email = row[email_col].split(",")[0].strip() if len(row) > email_col else ""
            college = row[college_col] if len(row) > college_col else "Institution"
            draft = row[draft_col] if len(row) > draft_col else ""
            tracking_id = row[tracking_id_col] if len(row) > tracking_id_col else ""
            pixel_url = row[pixel_col] if len(row) > pixel_col else ""

            if not to_email or not draft:
                print(f"⏩ Skipping Row {i+1}: Missing email or draft.")
                continue

            print(f"📧 Sending outreach to {college} ({to_email})...")
            
            subject = f"Improving Digital Infrastructure for {college}"
            success, msg = send_email(to_email, subject, draft, pixel_url, tracking_id)
            
            if success:
                print(f"✅ Success: {msg}")
                # Update sheet
                row_update = list(row) + [""] * (len(header) - len(row))
                row_update[sent_col] = "TRUE"
                row_update[status_col] = "outreach_sent"
                
                # Try to add timestamp if column exists
                ts_col = col_map.get('Email 1 Sent Timestamp')
                if ts_col:
                    row_update[ts_col] = time.strftime("%Y-%m-%d %H:%M:%S")

                helper.update_row(i + 1, row_update)
                processed_count += 1
            else:
                print(f"❌ Failed Row {i+1}: {msg}")

            if processed_count >= limit and not row_index:
                break
            
            time.sleep(2) # Anti-spam delay

    print(f"\n✨ Outreach processing complete. Emails sent: {processed_count}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Process and send outreach emails")
    parser.add_argument("--row", type=int, help="Target a specific row index")
    parser.add_argument("--limit", type=int, default=5, help="Max emails to send in this batch")
    
    args = parser.parse_args()
    process_outreach(row_index=args.row, limit=args.limit)
