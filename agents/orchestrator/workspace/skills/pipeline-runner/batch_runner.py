#!/usr/bin/env python3
"""
Batch Runner — Fetches un-crawled leads from Google Sheet.
Part of the pipeline-runner skill for the Orchestrator agent.
"""
import sys
import os
from dotenv import load_dotenv

# Load .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', '.env')
if not os.path.exists(env_path):
    env_path = '/app/.env'
load_dotenv(env_path)

# Add gsheet-manager to path
gsheet_skill_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gsheet-manager')
sys.path.insert(0, gsheet_skill_path)
from gsheets_helper import GSheetsHelper


def get_next_batch(size=2, start_from=None):
    """Get the next batch of un-crawled leads from the Google Sheet."""
    try:
        helper = GSheetsHelper()
        rows = helper.get_all_rows(force_refresh=True)

        if not rows or len(rows) < 4:
            return {"error": "Sheet is empty or has invalid structure."}

        header = rows[2]
        col_map = {name: i for i, name in enumerate(header)}

        name_col = col_map.get('College Name', 4)
        web_col = col_map.get('Website', 7)
        crawled_col = col_map.get('Crawled')

        leads = []
        start_idx = (start_from - 1) if start_from else 4

        for i in range(start_idx, len(rows)):
            row = rows[i]
            crawled = row[crawled_col].strip().upper() if crawled_col and len(row) > crawled_col else ""

            if crawled != "TRUE":
                college = row[name_col] if len(row) > name_col else ""
                website = row[web_col] if len(row) > web_col else ""

                if college and website:
                    leads.append({
                        'college_name': college,
                        'website': website,
                        'row_idx': i + 1
                    })

                if len(leads) >= size:
                    break

        return leads

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import json
    batch = get_next_batch(5)
    print(json.dumps(batch, indent=2))
