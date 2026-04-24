import sys
import os

# Add the current directory to sys.path so we can import scripts
sys.path.append(os.path.join(os.getcwd(), "scripts"))

try:
    from gsheets_helper import GSheetsHelper
    helper = GSheetsHelper()
    rows = helper.get_all_rows()
    if len(rows) > 2:
        print("HEADERS_FOUND:" + ",".join(rows[2]))
    else:
        print("NO_HEADERS_FOUND")
except Exception as e:
    print(f"ERROR: {e}")
