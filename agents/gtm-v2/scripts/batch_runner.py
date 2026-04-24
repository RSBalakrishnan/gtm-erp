#!/usr/bin/env python3
import json
import sys
import os
from gsheets_helper import GSheetsHelper

def get_next_batch(batch_size=10, start_from=None):
    try:
        helper = GSheetsHelper()
        rows = helper.get_all_rows()
        
        if not rows or len(rows) < 4:
            return {"error": "Google Sheet empty or invalid structure."}

        # Headers are in Row 3 (index 2)
        header = rows[2]
        col_map = {name: i for i, name in enumerate(header)}
        
        name_idx = col_map.get('College Name')
        web_idx = col_map.get('Website')
        crawled_idx = col_map.get('Crawled')
        univ_idx = col_map.get('University Name')
        state_idx = col_map.get('State')

        research_idx = col_map.get('Website Extraction Research')

        leads = []
        # Data starts from Row 5 (index 4)
        start_idx = max(4, (start_from - 1)) if start_from else 4
        for i in range(start_idx, len(rows)):
            row = rows[i]
            if len(row) <= name_idx or len(row) <= web_idx:
                continue
                
            website = row[web_idx].strip()
            
            # Skip if no website
            if not website:
                continue
                
            # Skip if already researched
            if research_idx is not None and len(row) > research_idx:
                if row[research_idx].strip() != "":
                    continue
                
            leads.append({
                "college_name": row[name_idx].strip(),
                "website": website,
                "university_name": row[univ_idx].strip() if univ_idx is not None and len(row) > univ_idx else "",
                "state": row[state_idx].strip() if state_idx is not None and len(row) > state_idx else "",
                "row_idx": i + 1
            })
            
            if len(leads) >= batch_size:
                break
                
        return leads
    except Exception as e:
        import traceback
        return {"error": str(e), "trace": traceback.format_exc()}

if __name__ == "__main__":
    batch_size = 10
    if len(sys.argv) > 1:
        try:
            batch_size = int(sys.argv[1])
        except:
            pass
            
    print(json.dumps(get_next_batch(batch_size), indent=2))
