#!/usr/bin/env python3
"""
Update Excel (Google Sheets) — Saves agent pipeline results to the GTM Google Sheet.
Part of the gsheet-manager skill for the Orchestrator agent.
"""
import json
import sys
import os
from dotenv import load_dotenv

# Add skill directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gsheets_helper import GSheetsHelper

# Load .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', '.env')
if not os.path.exists(env_path):
    env_path = '/app/.env'
load_dotenv(env_path)


def update_lead(data):
    """Update a lead row in the Google Sheet with pipeline results."""
    helper = GSheetsHelper()
    rows = helper.get_all_rows(force_refresh=True)

    if not rows or len(rows) < 4:
        print("❌ Sheet is empty or has invalid structure.")
        return False

    header = rows[2]
    col_map = {name: i for i, name in enumerate(header)}

    # Find the target row
    row_idx = data.get('row_idx')
    college_name = data.get('college_name', '')

    if not row_idx:
        # Search by college name
        name_col = col_map.get('College Name', 4)
        for i in range(4, len(rows)):
            if len(rows[i]) > name_col and rows[i][name_col].strip().lower() == college_name.strip().lower():
                row_idx = i + 1
                break

    if not row_idx:
        print(f"❌ Could not find row for '{college_name}'")
        return False

    # Build the update
    row = list(rows[row_idx - 1]) if row_idx <= len(rows) else [''] * len(header)
    row.extend([''] * (len(header) - len(row)))  # Pad if needed

    # Map data fields to columns
    field_map = {
        'Website Extraction': 'website_extraction',
        'Website Extraction Research': 'website_extraction_research',
        'Emails': lambda d: ', '.join(d.get('contacts', {}).get('emails', [])),
        'Phone Numbers': lambda d: ', '.join(d.get('contacts', {}).get('phones', [])),
        'LinkedIn': lambda d: ', '.join(d.get('contacts', {}).get('linkedin_profiles', [])),
        'Target Persona': lambda d: d.get('classification', {}).get('target_persona', ''),
        'College Type': lambda d: d.get('classification', {}).get('college_type', ''),
        'Email 1': lambda d: d.get('outreach_templates', {}).get('email_1', ''),
        'Email 2': lambda d: d.get('outreach_templates', {}).get('email_2', ''),
        'Email 3': lambda d: d.get('outreach_templates', {}).get('email_3', ''),
        'Tracking ID': 'tracking_id',
        'Pixel URL': 'pixel_url',
        'Status': lambda d: d.get('tracking', {}).get('status', 'researched'),
        'Crawled': lambda d: 'TRUE',
    }

    for col_name, source in field_map.items():
        if col_name in col_map:
            idx = col_map[col_name]
            if callable(source):
                row[idx] = source(data)
            elif source in data and data[source]:
                row[idx] = str(data[source])

    helper.update_row(row_idx, row)
    print(f"✅ Updated Row {row_idx}: {college_name}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 update_excel.py '<json_string>' OR python3 update_excel.py <file.json>")
        sys.exit(1)

    arg = sys.argv[1]

    # Check if it's a file path or JSON string
    if os.path.isfile(arg):
        with open(arg, 'r') as f:
            data = json.load(f)
    else:
        data = json.loads(arg)

    update_lead(data)
