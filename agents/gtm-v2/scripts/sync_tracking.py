import os
import json
import subprocess

TRACKING_DIR = "/Users/apple/Desktop/gtm/agents/gtm-v2/tracking"
UPDATE_SCRIPT = "/Users/apple/Desktop/gtm/update_excel.py"

def sync_all():
    if not os.path.exists(TRACKING_DIR):
        print("No tracking directory found.")
        return

    json_files = [f for f in os.listdir(TRACKING_DIR) if f.endswith('.json')]
    if not json_files:
        print("No JSON files to sync.")
        return

    print(f"Found {len(json_files)} files to sync...")

    for filename in json_files:
        file_path = os.path.join(TRACKING_DIR, filename)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Use update_excel.py to sync to master XLSX and CSV
            data_str = json.dumps(data)
            print(f"Syncing {filename}...")
            subprocess.run(["python3", UPDATE_SCRIPT, data_str], check=True)
            
            # Optional: Delete after sync
            # os.remove(file_path)
            
        except Exception as e:
            print(f"Error syncing {filename}: {e}")

if __name__ == "__main__":
    sync_all()
