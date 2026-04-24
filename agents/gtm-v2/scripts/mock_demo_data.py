import sys
import os
import random
from datetime import datetime, timedelta

def run_mock_demo():
    try:
        from gsheets_helper import GSheetsHelper
        helper = GSheetsHelper()
        print("Fetching sheet...")
        rows = helper.get_all_rows()
        
        if not rows or len(rows) < 3:
            print("Error: Sheet empty.")
            return

        header = list(rows[2])
        
        # We need to add Timestamp columns if they don't exist
        # We'll just add them to the end
        sent_ts_idx = -1
        opened_ts_idx = -1
        
        if 'Email 1 Sent Timestamp' in header:
            sent_ts_idx = header.index('Email 1 Sent Timestamp')
        else:
            sent_ts_idx = len(header)
            header.append('Email 1 Sent Timestamp')
            
        if 'Email Opened Timestamp' in header:
            opened_ts_idx = header.index('Email Opened Timestamp')
        else:
            opened_ts_idx = len(header)
            header.append('Email Opened Timestamp')
        
        print("Updating headers...")
        helper.update_row(3, header) # Update row 3
        
        count = 0
        for i in range(4, min(len(rows), 1000)):  # Only do first ~1000 rows to be safe
            row = list(rows[i])
            
            # Pad row to match new header length
            while len(row) <= max(sent_ts_idx, opened_ts_idx):
                row.append("")
                
            email_1 = row[22] if len(row) > 22 else ""
            
            # "Do captured leads only" -> Check if it has a real email draft
            if email_1 and len(email_1) > 15 and "N/A" not in email_1 and "Unreachable" not in email_1:
                
                # 40% chance of being sent
                is_sent = random.random() < 0.40
                if is_sent:
                    row[25] = "TRUE" # Email 1 Sent
                    
                    # Generate a timestamp sometime in the last 48 hours
                    hours_ago = random.randint(2, 48)
                    sent_time = datetime.now() - timedelta(hours=hours_ago, minutes=random.randint(0, 59))
                    row[sent_ts_idx] = sent_time.strftime("%Y-%m-%d %H:%M:%S")
                    
                    # If it was sent, 50% chance of being opened
                    is_opened = random.random() < 0.50
                    if is_opened:
                        row[26] = "TRUE"
                        # Opened between 15 mins and (hours_ago - 1) hours after sending
                        open_delay_hours = random.uniform(0.25, max(0.5, hours_ago - 0.5))
                        open_time = sent_time + timedelta(hours=open_delay_hours)
                        row[opened_ts_idx] = open_time.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        row[26] = "FALSE"
                        row[opened_ts_idx] = ""
                        
                    print(f"Updating row {i+1} - Sent: {row[25]}, Opened: {row[26]}")
                    helper.update_row(i+1, row)
                    count += 1
                    
        print(f"✅ Successfully injected mock data for {count} captured leads.")

    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_mock_demo()
