import os
import sys
# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

from gsheets_helper import GSheetsHelper

def add_dummy_lead():
    helper = GSheetsHelper()
    rows = helper.get_all_rows()
    if not rows or len(rows) < 3:
        print("Error: Sheet structure invalid.")
        return

    header = rows[2]
    print("Headers:", header)
    
    # Create a dummy row matching the header length
    new_row = [""] * len(header)
    
    # Fill in the basics based on known mapping
    col_map = {name: i for i, name in enumerate(header)}
    
    if "College Name" in col_map: new_row[col_map["College Name"]] = "Test University"
    if "Website" in col_map: new_row[col_map["Website"]] = "https://example.com"
    if "Emails" in col_map: new_row[col_map["Emails"]] = "scottdbms@gmail.com"
    if "Status" in col_map: new_row[col_map["Status"]] = "open"
    if "Crawled" in col_map: new_row[col_map["Crawled"]] = "FALSE"

    print("Appending row:", new_row)
    success = helper.append_row(new_row)
    if success:
        # Get the new row index (it should be the last one)
        updated_rows = helper.get_all_rows(force_refresh=True)
        print(f"✅ Dummy lead added at Row {len(updated_rows)}")
    else:
        print("❌ Failed to add dummy lead.")

if __name__ == "__main__":
    add_dummy_lead()
