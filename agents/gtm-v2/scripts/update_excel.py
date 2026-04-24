#!/usr/bin/env python3
import json
import sys
import os
from gsheets_helper import GSheetsHelper

def flatten_json(data):
    """Map the agent's nested JSON to the spreadsheet column structure"""
    flat = {}
    flat['College Name'] = data.get('college_name', '')
    flat['Website'] = data.get('website', '')
    
    # Combined Research Column
    # We prioritize the deep research report, but prefix it with the brief extraction summary if present
    extraction = data.get('website_extraction', '')
    research = data.get('website_extraction_research', '')
    if extraction and research:
        flat['Website Extraction Research'] = f"{extraction}\n\n{research}"
    else:
        flat['Website Extraction Research'] = research or extraction
    
    # Exhaustive Contact Mapping
    contacts = data.get('contacts', {})
    flat['Emails'] = ", ".join(contacts.get('emails', [])) if isinstance(contacts.get('emails'), list) else contacts.get('emails', '')
    flat['Phones'] = ", ".join(contacts.get('phones', [])) if isinstance(contacts.get('phones'), list) else contacts.get('phones', '')
    flat['LinkedIn Profiles'] = ", ".join(contacts.get('linkedin_profiles', [])) if isinstance(contacts.get('linkedin_profiles'), list) else contacts.get('linkedin_profiles', '')
    
    # Target Persona
    classification = data.get('classification', {})
    flat['Target Persona'] = classification.get('target_persona', '')
    
    # Outreach Templates Mapping
    templates = data.get('outreach_templates', {})
    emails_data = data.get('emails', {})
    
    # We populate Email 1, 2, and 3 columns with the specific drafts found in outreach_templates
    flat['Email 1'] = templates.get('email_1', '')
    flat['Email 2'] = templates.get('email_2', '')
    flat['Email 3'] = templates.get('email_3', '')
    
    # Tracking & Status
    tracking = data.get('tracking', {})
    flat['Email 1 Sent'] = str(tracking.get('email_1_sent', False)).upper()
    flat['Email Opened'] = str(tracking.get('email_opened', False)).upper()
    flat['Email 2 Sent'] = str(tracking.get('email_2_sent', False)).upper()
    flat['Email 3 Sent'] = str(tracking.get('email_3_sent', False)).upper()
    flat['Demo Booked'] = str(tracking.get('demo_booked', False)).upper()
    flat['Status'] = tracking.get('status', 'open')
    flat['Crawled'] = 'TRUE'
    flat['Tracking ID'] = data.get('tracking_id', '')
    flat['Pixel URL'] = data.get('pixel_url', '')
    
    return flat

def update_gsheet(json_data):
    helper = GSheetsHelper()
    rows = helper.get_all_rows()
    
    if not rows or len(rows) < 3:
        print("Error: Sheet structure invalid.")
        return False

    header = rows[2] # Row 3 contains headers
    col_map = {name: i for i, name in enumerate(header)}
    flat_data = flatten_json(json_data)
    
    target_row_idx = json_data.get('row_idx')
    current_row = None

    if target_row_idx:
        # If row_idx is provided, we still fetch all rows once to get header mapping and the initial row content 
        # (Though in a perfect world, we'd only fetch that specific row range to be lightning fast)
        if len(rows) >= target_row_idx:
            current_row = rows[target_row_idx - 1]
            print(f"📍 Using direct Row Index: {target_row_idx}")
    else:
        # Fallback to search logic
        college_name = flat_data.get('College Name', '').lower()
        website = flat_data.get('Website', '').lower()
        
        name_idx = col_map.get('College Name')
        web_idx = col_map.get('Website')

        for i in range(4, len(rows)):
            row = rows[i]
            match = False
            if name_idx is not None and len(row) > name_idx:
                if row[name_idx].lower().strip() == college_name.strip():
                    match = True
            if not match and web_idx is not None and len(row) > web_idx:
                if website != "" and website.strip() in row[web_idx].lower():
                    match = True
            
            if match:
                target_row_idx = i + 1 # 1-indexed
                current_row = row
                break

    if target_row_idx is None:
        print(f"Warning: Could not find college {college_name} in list. Appending is not supported.")
        return False

    # Create a full row with same length as header
    updated_row = (list(current_row) + [""] * len(header))[:len(header)]
    
    # Update the cells with VALUE PROTECTION
    for key, value in flat_data.items():
        if key in col_map:
            idx = col_map[key]
            # PROTECT: Don't overwrite existing Name/Website with empty data
            if key in ['College Name', 'Website'] and not value:
                if len(current_row) > idx and current_row[idx]:
                    continue
            updated_row[idx] = value

    # Write back to GSheet
    print(f"Updating GSheet row {target_row_idx}...")
    success = helper.update_row(target_row_idx, updated_row)
    
    if success:
        print(f"✅ Successfully updated GSheet: {flat_data.get('College Name')}")
    return success

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        raw_json = None
        
        # Handle file paths (direct or with @ prefix)
        potential_path = arg[1:] if arg.startswith('@') else arg
        if os.path.exists(potential_path):
            try:
                with open(potential_path, 'r') as f:
                    raw_json = f.read()
            except Exception as e:
                print(f"Error reading file {potential_path}: {e}")
        
        # If not a file or file read failed, treat as literal JSON
        if raw_json is None:
            raw_json = arg
            
        try:
            input_data = json.loads(raw_json)
            update_gsheet(input_data)
        except Exception as e:
            import traceback
            print(f"Error: {e}")
            traceback.print_exc()
    else:
        print("Usage: python3 update_excel.py '<json_string>' or python3 update_excel.py <file_path>")
