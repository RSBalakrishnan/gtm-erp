import requests
import time
import json
import os
from dotenv import load_dotenv

# Load credentials from .env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(env_path)

API_BASE_URL = os.getenv("SCRAPER_API_URL")

def test_scraper_api(url):
    print(f"🚀 Testing Scraper API for: {url}")
    
    # 1. Check if data already exists
    print("🔍 Checking for existing data...")
    try:
        res = requests.get(f"{API_BASE_URL}/scrape/getData", params={"websiteURL": url}, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data and "data" in data:
                print("✅ Found existing data in cache!")
                return data["data"]
    except Exception as e:
        print(f"⚠️ Cache check failed: {e}")

    # 2. Trigger new scrape
    print("⚡ Triggering new scrape...")
    res = requests.post(f"{API_BASE_URL}/scrape", json={"websiteURL": url}, timeout=10)
    if res.status_code != 200:
        print(f"❌ Failed to trigger scrape: {res.text}")
        return None
    
    job_id = res.json().get("job_id")
    print(f"⏳ Job started. ID: {job_id}. Polling for completion...")

    # 3. Poll for status
    for i in range(20): # 10 minute timeout (30s * 20)
        status_res = requests.get(f"{API_BASE_URL}/scrape/{job_id}/status")
        if status_res.status_code == 200:
            status = status_res.json().get("status")
            print(f"   [{i*30}s] Status: {status}")
            if status == "completed":
                # 4. Get result
                result_res = requests.get(f"{API_BASE_URL}/scrape/{job_id}/result")
                return result_res.json()
            elif status == "failed":
                print("❌ Scrape job failed.")
                return None
        time.sleep(30)
    
    print("⏰ API Timeout reached.")
    return None

if __name__ == "__main__":
    test_url = "http://www.srivikascon.org/"
    result = test_scraper_api(test_url)
    if result:
        print("\n--- SCRAPE RESULT ---")
        print(json.dumps(result, indent=2))
    else:
        print("❌ Final test failed.")
