#!/usr/bin/env python3
import sys
import os

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

from gsheets_helper import GSheetsHelper

def calculate():
    helper = GSheetsHelper()
    print("Fetching sheet data... (might take a moment)")
    rows = helper.get_all_rows()
    
    if not rows or len(rows) < 4:
        print("Error: Sheet empty or invalid.")
        return

    # Headers are in Row 3 (index 2)
    header = rows[2]
    col_map = {name: i for i, name in enumerate(header)}
    
    crawled_idx = col_map.get('Crawled')
    status_idx = col_map.get('Status')
    
    if crawled_idx is None:
        print("Error: 'Crawled' column not found.")
        return

    total_leads = len(rows) - 4
    crawled_count = 0
    reached_count = 0
    unreachable_count = 0
    skipped_count = 0

    for i in range(4, len(rows)):
        row = rows[i]
        crawled = row[crawled_idx].strip().upper() == 'TRUE' if len(row) > crawled_idx else False
        status = row[status_idx].strip().lower() if status_idx is not None and len(row) > status_idx else 'open'
        
        if crawled:
            crawled_count += 1
            if status == 'unreachable':
                unreachable_count += 1
            else:
                reached_count += 1
        elif status == 'skipped':
            skipped_count += 1

    # Pricing assumptions for MiniMax m2.5 (Bedrock)
    # Average 25k input tokens, 1.5k output tokens per reached lead
    input_price_per_m = 0.30
    output_price_per_m = 1.20
    
    avg_input_tokens = 25000
    avg_output_tokens = 1500
    
    cost_per_reached = (avg_input_tokens / 1000000 * input_price_per_m) + (avg_output_tokens / 1000000 * output_price_per_m)
    total_cost = reached_count * cost_per_reached

    print("\n--- GTM Pipeline Summary ---")
    print(f"Total Leads in Sheet: {total_leads}")
    print(f"Total Processed (Crawled): {crawled_count}")
    print(f"  - ✅ Reached & Researched: {reached_count}")
    print(f"  - ❌ Unreachable (DNS/403): {unreachable_count}")
    print(f"Remaining Leads: {total_leads - crawled_count}")
    print("\n--- Estimated Cost (MiniMax m2.5 Bedrock) ---")
    print(f"Cost per Researched Lead: ${cost_per_reached:.4f}")
    print(f"Total Estimated Cost: ${total_cost:.2f}")
    print("----------------------------\n")

if __name__ == "__main__":
    calculate()
