import sys
import random
from gsheets_helper import GSheetsHelper

def run():
    print("Starting quick update for Demo Booked...")
    helper = GSheetsHelper()
    rows = helper.get_all_rows()
    
    header = list(rows[2])
    print(f"Header length: {len(header)}")
    
    emails_idx = header.index('Emails') if 'Emails' in header else 18
    opened_idx = header.index('Email Opened') if 'Email Opened' in header else 26
    demo_idx = header.index('Demo Booked') if 'Demo Booked' in header else 29
    
    count = 0
    # Process rows quickly
    for i in range(4, min(1000, len(rows))):
        row = list(rows[i])
        while len(row) <= max(emails_idx, opened_idx, demo_idx):
            row.append("")
            
        emails_col = row[emails_idx].strip()
        opened_col = row[opened_idx].strip().upper()
        
        if opened_col == "TRUE" and len(emails_col) > 4 and "N/A" not in emails_col.upper():
            # 30% chance to book a demo if opened and has email
            if random.random() < 0.3:
                row[demo_idx] = "TRUE"
                helper.update_row(i+1, row)
                count += 1
                print(f"Row {i+1} marked as Demo Booked: TRUE")
                
    print(f"✅ Successfully updated {count} rows with Demo Booked status!")

if __name__ == "__main__":
    run()
