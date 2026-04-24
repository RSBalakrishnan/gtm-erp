#!/usr/bin/env python3
import os
import json
import subprocess

WORKSPACE_DIR = "/Users/apple/Desktop/gtm/agents/gtm-v2/workspace"
UPDATE_SCRIPT = "/Users/apple/Desktop/gtm/agents/gtm-v2/scripts/update_excel.py"

def sync_workspace():
    synced = 0
    failed = 0
    for filename in sorted(os.listdir(WORKSPACE_DIR)):
        if filename.endswith("_processed.json"):
            file_path = os.path.join(WORKSPACE_DIR, filename)
            print(f"\n--- Syncing {filename} ---")
            with open(file_path, 'r') as f:
                data = json.load(f)
            leads = data if isinstance(data, list) else [data]
            for lead in leads:
                college = lead.get("college_name", "Unknown")
                result = subprocess.run(
                    ["python3", UPDATE_SCRIPT, json.dumps(lead)],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    print(f"  ✅ {college}")
                    synced += 1
                else:
                    print(f"  ❌ {college}: {result.stderr.strip()}")
                    failed += 1
    print(f"\n=== Done: {synced} synced, {failed} failed ===")

if __name__ == "__main__":
    sync_workspace()
