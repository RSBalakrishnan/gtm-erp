import sys
import os
import json
import subprocess
from gsheets_helper import GSheetsHelper

def research_row(row_index):
    helper = GSheetsHelper()
    rows = helper.get_all_rows()
    
    if row_index > len(rows):
        print(f"Row {row_index} out of range.")
        return

    row = rows[row_index - 1]
    college_name = row[4] if len(row) > 4 else "Unknown"
    website = row[7] if len(row) > 7 else ""
    
    if not website:
        print(f"No website found for row {row_index}.")
        return

    print(f"🔍 Researching Row {row_index}: {college_name} ({website})")
    
    # Run the agent using openclaw
    # The agent expects the URL.
    # We will pass the row index to the agent so it can use tracking_id
    prompt = f"Perform deep research on {website}. You are OnCampus ERP Sales Agent. The lead's tracking ID is {row_index}. Output the Summary, Lead Score, Opportunity, and Personalized Outreach Toolkit (Email, LinkedIn, WhatsApp) with embedded tracking links."
    
    cmd = [
        "npx", "openclaw", "run",
        "-p", prompt
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # We won't wait for it here if we want it to run in background, 
    # but for single research it's better to wait and see output.
    stdout, stderr = process.communicate()
    
    print(stdout)
    if stderr:
        print(f"Error: {stderr}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 research_single_row.py <row_index>")
    else:
        research_row(int(sys.argv[1]))
