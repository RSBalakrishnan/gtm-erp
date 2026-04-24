import random
from gsheets_helper import GSheetsHelper

def simulate_demos():
    helper = GSheetsHelper()
    rows = helper.get_all_rows()
    if not rows or len(rows) < 4:
        return

    header = rows[2]
    col_map = {name: i for i, name in enumerate(header)}
    
    opened_idx = col_map.get('Email Opened')
    emails_idx = col_map.get('Emails')
    demo_idx = col_map.get('Demo Booked')
    status_idx = col_map.get('Status')

    updated_count = 0
    for i in range(4, len(rows)):
        row = rows[i]
        # Check if already booked
        if len(row) > demo_idx and row[demo_idx].upper() == 'TRUE':
            continue
            
        # Check if email was opened (don't strictly require email string for this simulation demo)
        if (len(row) > opened_idx and row[opened_idx].strip().upper() == 'TRUE'):
            
            print(f"📊 Row {i+1} candidate: {row[4] if len(row)>4 else 'Unknown'}")
            # Simulate 35% booking rate, but force the very first one to succeed for the demo
            if updated_count == 0 or random.random() < 0.35:
                # Update row
                new_row = list(row)
                while len(new_row) <= max(demo_idx, status_idx):
                    new_row.append('')
                
                new_row[demo_idx] = 'TRUE'
                new_row[status_idx] = 'demo_booked'
                
                print(f"🎉 Booking demo for Row {i+1}: {row[4] if len(row)>4 else 'Unknown'}")
                helper.update_row(i+1, new_row)
                updated_count += 1

    print(f"\n✅ Simulation complete. {updated_count} demos booked.")

if __name__ == "__main__":
    simulate_demos()
