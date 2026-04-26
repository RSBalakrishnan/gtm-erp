import os
import time
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Path relative to the agent skill
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', '.env')
load_dotenv(env_path)

BACKEND_URL = os.getenv("GTM_BACKEND_URL", "http://localhost:8000")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', 'logs', 'agent_telemetry.jsonl')

def ship_log(log_data):
    """Send log to backend telemetry endpoint."""
    try:
        # 1. Send Telemetry
        telemetry_payload = {
            "job_id": log_data.get("job_id"),
            "agent_name": log_data.get("agent_name"),
            "message": log_data.get("message"),
            "level": log_data.get("level"),
            "timestamp": log_data.get("timestamp", datetime.utcnow().isoformat())
        }
        requests.post(f"{BACKEND_URL}/agents/telemetry", json=telemetry_payload, timeout=5)
        
        # 2. Trigger Handover if applicable
        if "next_step" in log_data or "intent_score" in log_data or "demo_booking_url" in log_data:
            target_id = log_data.get("job_id")
            if target_id:
                result_payload = {
                    "intent_score": log_data.get("intent_score"),
                    "demo_booking_url": log_data.get("demo_booking_url"),
                    "metadata": log_data.get("metadata", {}),
                    "next_step": log_data.get("next_step")
                }
                result_payload = {k: v for k, v in result_payload.items() if v is not None}
                requests.patch(f"{BACKEND_URL}/targets/{target_id}/result", json=result_payload, timeout=5)

    except Exception as e:
        print(f"❌ Telemetry Agent Error: {e}")

def tail_f(filename):
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        open(filename, 'a').close()
        
    with open(filename, 'r') as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

def main():
    print(f"🕵️ Telemetry Agent Active. Monitoring logs...")
    for line in tail_f(LOG_FILE):
        try:
            ship_log(json.loads(line))
        except: pass

if __name__ == "__main__":
    main()
