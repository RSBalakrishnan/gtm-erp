#!/usr/bin/env python3
"""
Analytica Helper (Query) — Email open and link click analytics.
Part of the analytica-monitor skill for the Tracker agent.
"""
import requests
import json
import sys
import os
from dotenv import load_dotenv

# Load .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', '.env')
if not os.path.exists(env_path):
    env_path = '/app/.env'
load_dotenv(env_path)

ANALYTICA_BASE = os.getenv("ANALYTICA_BASE")


def get_email_status(tracking_id):
    """Get email open status and count for a tracking ID."""
    res = requests.get(f"{ANALYTICA_BASE}/analytics/email/{tracking_id}", timeout=10)
    res.raise_for_status()
    return res.json()


def get_link_analytics(tracking_id):
    """Get link click data for a tracking ID."""
    res = requests.get(f"{ANALYTICA_BASE}/analytics/link/{tracking_id}", timeout=10)
    res.raise_for_status()
    return res.json()


def get_journey(tracking_id):
    """Get full chronological event journey for a tracking ID."""
    res = requests.get(f"{ANALYTICA_BASE}/analytics/tracking/{tracking_id}", timeout=10)
    res.raise_for_status()
    return res.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analytica_helper.py <tracking_id>")
        sys.exit(1)

    tid = sys.argv[1]
    try:
        print("📧 Email Status:")
        print(json.dumps(get_email_status(tid), indent=2))
        print("\n🔗 Link Analytics:")
        print(json.dumps(get_link_analytics(tid), indent=2))
        print("\n📋 Journey:")
        print(json.dumps(get_journey(tid), indent=2))
    except Exception as e:
        print(f"Error: {e}")
