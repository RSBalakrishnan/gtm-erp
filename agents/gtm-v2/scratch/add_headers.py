import sys
import os

sys.path.append(os.path.join(os.getcwd(), "scripts"))

try:
    from gsheets_helper import GSheetsHelper
    helper = GSheetsHelper()
    rows = helper.get_all_rows()
    if len(rows) > 2:
        header = rows[2]
        new_headers = ["Tracking ID", "Pixel URL"]
        added = False
        for h in new_headers:
            if h not in header:
                header.append(h)
                added = True
        
        if added:
            # Update the header row (Row 3, index 3 in 1-indexing)
            if helper.update_row(3, header):
                print("SUCCESS: Headers updated.")
            else:
                print("ERROR: Failed to update headers.")
        else:
            print("INFO: Headers already exist.")
    else:
        print("ERROR: Sheet structure invalid.")
except Exception as e:
    print(f"ERROR: {e}")
