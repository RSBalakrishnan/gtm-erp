#!/usr/bin/env python3
"""
Analytica Helper (Create) — Tracking ID and pixel URL creation.
Part of the email-generator skill for the Outreach Writer agent.
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', '.env')
if not os.path.exists(env_path):
    env_path = '/app/.env'
load_dotenv(env_path)

ANALYTICA_BASE = os.getenv("ANALYTICA_BASE")


def create_tracking_id(target_urls=None):
    """Create a new Analytica tracking ID for email open/click tracking.

    Args:
        target_urls: List of CTA URLs to track (default: oncampuserp.com/demo)

    Returns:
        dict: {trackingId, pixelUrl, redirectUrlBase, links[{original, tracking}]}
    """
    if not target_urls:
        target_urls = ["https://oncampuserp.com/demo", "https://oncampuserp.com"]

    res = requests.post(
        f"{ANALYTICA_BASE}/track/id",
        json={"targets": target_urls},
        timeout=10
    )
    res.raise_for_status()
    return res.json()


if __name__ == "__main__":
    try:
        result = create_tracking_id()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
