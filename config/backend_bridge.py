#!/usr/bin/env python3
"""
Backend Bridge — Unified API client for GTM Engine <-> Marketing Backend communication.
Handles campaign fetching, result reporting, and telemetry syncing.
"""
import requests
import os
import json
import time
from dotenv import load_dotenv

# Load .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
if not os.path.exists(env_path):
    env_path = '/app/.env'
load_dotenv(env_path)

BACKEND_URL = os.getenv("GTM_BACKEND_URL", "http://localhost:8000")
ANALYTICA_URL = os.getenv("ANALYTICA_BASE", "http://3.110.134.234:3000")
API_TOKEN = os.getenv("OPENCLAW_GATEWAY_TOKEN", "")


class BackendBridge:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_TOKEN}"
        }

    # --- Campaign Management ---
    def get_campaign(self, campaign_id):
        """Fetch the full campaign context object."""
        try:
            response = requests.get(f"{self.base_url}/campaigns/{campaign_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ BackendBridge: Failed to fetch campaign {campaign_id}: {e}")
            return None

    # --- Target Reporting ---
    def update_target_result(self, target_id, result_data):
        """Push research/outreach results back to the backend DB."""
        try:
            response = requests.patch(
                f"{self.base_url}/targets/{target_id}/result",
                headers=self.headers,
                json=result_data
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"❌ BackendBridge: Failed to update target {target_id}: {e}")
            return False

    # --- Telemetry Sync ---
    def push_telemetry(self, event_type, agent_id, target_id, message, metadata=None):
        """Report agent activity for live monitoring."""
        payload = {
            "timestamp": time.time(),
            "event": event_type,
            "agent": agent_id,
            "target_id": target_id,
            "message": message,
            "metadata": metadata or {}
        }
        try:
            # Pushes to the agent telemetry endpoint on your backend
            requests.post(f"{self.base_url}/agents/telemetry", headers=self.headers, json=payload)
        except Exception:
            pass # Telemetry is best-effort, don't break the pipeline on failure

    # --- Analytica Tracking ---
    def create_tracking(self, target_name, campaign_id):
        """Create a new tracking ID in Analytica."""
        try:
            payload = {
                "label": target_name,
                "campaign_id": campaign_id,
                "metadata": {"source": "gtm-engine-v4"}
            }
            response = requests.post(f"{ANALYTICA_URL}/tracking/create", json=payload)
            response.raise_for_status()
            return response.json() # {tracking_id, pixel_url, redirect_base}
        except Exception as e:
            print(f"❌ BackendBridge: Failed to create tracking in Analytica: {e}")
            return None


if __name__ == "__main__":
    # Quick test
    bridge = BackendBridge()
    print(f"Testing bridge to {BACKEND_URL}...")
    # Add real tests here if needed
