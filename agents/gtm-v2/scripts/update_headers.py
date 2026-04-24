#!/usr/bin/env python3
from gsheets_helper import GSheetsHelper

def update_headers():
    helper = GSheetsHelper()
    rows = helper.get_all_rows()
    
    if len(rows) < 3:
        print("Error: Could not find header row (3).")
        return
        
    header = list(rows[2])
    print(f"Current headers: {header}")
    
    # Rename 'Website Extraction' to 'Website Extraction Research'
    if "Website Extraction" in header:
        idx = header.index("Website Extraction")
        header[idx] = "Website Extraction Research"
        print(f"Renamed column at index {idx} to 'Website Extraction Research'")

    # Deduplicate: if 'Website Extraction Research' appears more than once, remove the second one
    indices = [i for i, x in enumerate(header) if x == "Website Extraction Research"]
    if len(indices) > 1:
        # Remove the second occurrence
        del header[indices[1]]
        print(f"Removed duplicate 'Website Extraction Research' column at index {indices[1]}")

    # Final check: if it doesn't exist at all, add it
    if "Website Extraction Research" not in header:
        header.insert(17, "Website Extraction Research")
        print("Inserted 'Website Extraction Research' column at index 17")

    print(f"New headers: {header}")
    
    # Update row 3 (1-indexed)
    success = helper.update_row(3, header)
    if success:
        print("✅ Successfully updated headers in Google Sheet.")
    else:
        print("❌ Failed to update headers.")

if __name__ == "__main__":
    update_headers()
