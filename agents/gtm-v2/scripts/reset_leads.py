#!/usr/bin/env python3
from gsheets_helper import GSheetsHelper

def reset_first_five():
    helper = GSheetsHelper()
    rows = helper.get_all_rows()
    
    if len(rows) < 5:
        print("Not enough rows.")
        return

    header = rows[2]
    crawled_idx = header.index('Crawled')
    research_idx = header.index('Website Extraction Research')

    processed = 0
    for i in range(4, len(rows)):
        if processed >= 5:
            break
        
        # Pad row to match header length if needed
        while len(rows[i]) < len(header):
            rows[i].append("")

        # Reset columns
        rows[i][crawled_idx] = "FALSE"
        rows[i][research_idx] = ""
        
        helper.update_row(i + 1, rows[i])
        processed += 1
        print(f"Reset lead {processed}: {rows[i][header.index('College Name')]}")

if __name__ == "__main__":
    reset_first_five()
