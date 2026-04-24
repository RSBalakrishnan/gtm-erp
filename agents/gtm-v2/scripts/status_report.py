#!/usr/bin/env python3
import json
import sys
from gsheets_helper import GSheetsHelper
from analytica_helper import get_email_status, get_link_analytics

def get_status(query=""):
    try:
        helper = GSheetsHelper()
        rows = helper.get_all_rows()
        
        if not rows or len(rows) < 4:
            return {"error": "Google Sheet empty or invalid structure."}
            
        results = []
        query = query.lower().strip()
        
        # Headers are in Row 3 (index 2)
        header = rows[2]
        col_map = {name: i for i, name in enumerate(header)}
        
        name_idx = col_map.get('College Name')
        web_idx = col_map.get('Website')
        crawled_idx = col_map.get('Crawled')
        status_idx = col_map.get('Status')
        target_idx = col_map.get('Target Persona')
        tracking_id_idx = col_map.get('Tracking ID')

        for i in range(4, len(rows)):
            row = rows[i]
            college = row[name_idx] if name_idx is not None and len(row) > name_idx else ""
            website = row[web_idx] if web_idx is not None and len(row) > web_idx else ""
            
            if not query or query in college.lower() or query in website.lower():
                tracking_id = row[tracking_id_idx] if tracking_id_idx is not None and len(row) > tracking_id_idx else ""
                opens = 0
                clicks = 0
                if tracking_id:
                    try:
                        email_data = get_email_status(tracking_id)
                        opens = email_data.get("openCount", email_data.get("opens", 0))
                        link_data = get_link_analytics(tracking_id)
                        clicks = link_data.get("totalClicks", link_data.get("clicks", 0))
                    except:
                        pass

                results.append({
                    "College": college,
                    "Website": website,
                    "Crawled": row[crawled_idx] if crawled_idx is not None and len(row) > crawled_idx else 'N/A',
                    "Status": row[status_idx] if status_idx is not None and len(row) > status_idx else 'open',
                    "Target": row[target_idx] if target_idx is not None and len(row) > target_idx else 'N/A',
                    "Tracking ID": tracking_id,
                    "Opens": opens,
                    "Clicks": clicks
                })
            
            if len(results) >= 10:
                break
        
        return results
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(get_status(query), indent=2))
