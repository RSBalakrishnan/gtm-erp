import requests
import json
import os
from dotenv import load_dotenv

# Load credentials from .env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(env_path)

ANALYTICA_BASE = os.getenv("ANALYTICA_BASE")

def create_tracking_id(target_urls):
    """Call POST /track/id with a list of target URLs.
    Returns dict: {trackingId, pixelUrl, redirectUrlBase, links[{original, tracking}]}
    """
    res = requests.post(f"{ANALYTICA_BASE}/track/id",
                        json={"targets": target_urls}, timeout=10)
    res.raise_for_status()
    return res.json()

def get_email_status(tracking_id):
    """Call GET /analytics/email/:trackingId.
    Returns dict with email open status and count.
    """
    res = requests.get(f"{ANALYTICA_BASE}/analytics/email/{tracking_id}", timeout=10)
    res.raise_for_status()
    return res.json()

def get_link_analytics(tracking_id):
    """Call GET /analytics/link/:trackingId.
    Returns dict with link click data.
    """
    res = requests.get(f"{ANALYTICA_BASE}/analytics/link/{tracking_id}", timeout=10)
    res.raise_for_status()
    return res.json()

def get_journey(tracking_id):
    """Call GET /analytics/tracking/:trackingId.
    Returns full chronological event journey.
    """
    res = requests.get(f"{ANALYTICA_BASE}/analytics/tracking/{tracking_id}", timeout=10)
    res.raise_for_status()
    return res.json()

if __name__ == "__main__":
    try:
        result = create_tracking_id(["https://oncampuserp.com/demo"])
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error testing analytica_helper: {e}")
