#!/usr/bin/env python3
"""
Scraper Client — Cache-first web scraping with async polling.
Extracted from deep_research_batch.py for the Researcher agent.
"""
import requests
import json
import time
import sys
import os
from dotenv import load_dotenv

# Load .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', '.env')
if not os.path.exists(env_path):
    env_path = '/app/.env'
load_dotenv(env_path)

SCRAPER_API_URL = os.getenv("SCRAPER_API_URL")


def scrape_website(url):
    """Scrape a website using cache-first strategy with async polling."""
    try:
        # Step 0: Check cache
        print(f"📡 Checking cache for {url}...")
        exists_res = requests.get(f"{SCRAPER_API_URL}/scrape/exists", params={"websiteURL": url}, timeout=10)
        if exists_res.status_code == 200 and exists_res.json().get("exists"):
            print(f"⚡ Cache HIT for {url}.")
            data_res = requests.get(f"{SCRAPER_API_URL}/scrape/getData", params={"websiteURL": url}, timeout=10)
            if data_res.status_code == 200:
                return data_res.json()

        # Step 1: Trigger full scrape
        print(f"📡 Cache MISS. Triggering full scrape for {url}...")
        res = requests.post(f"{SCRAPER_API_URL}/scrape", json={"websiteURL": url}, timeout=15)
        if res.status_code != 200:
            print(f"❌ Scraper API returned {res.status_code}")
            return None

        job_id = res.json().get("job_id")
        print(f"⏳ Job {job_id} started. Polling...")

        # Step 2: Poll for status
        result_data = None
        for i in range(10):  # 5 min total (30s × 10)
            status_res = requests.get(f"{SCRAPER_API_URL}/scrape/{job_id}/status", timeout=10)
            if status_res.status_code == 200:
                status = status_res.json().get("status")
                print(f"   [{i * 30}s] Status: {status}")
                if status == "completed":
                    # Step 3: Fetch result
                    result_res = requests.get(f"{SCRAPER_API_URL}/scrape/{job_id}/result", timeout=10)
                    if result_res.status_code == 200:
                        result_data = result_res.json()
                        break
                elif status == "failed":
                    print(f"❌ Scrape job failed.")
                    return None
            time.sleep(30)

        if result_data:
            # Step 4: Get page-level breakdown
            try:
                pages_res = requests.get(f"{SCRAPER_API_URL}/scrape/{job_id}/pages", timeout=10)
                if pages_res.status_code == 200:
                    result_data["pages_breakdown"] = pages_res.json()
            except Exception as e:
                print(f"⚠️ Could not fetch pages: {e}")
            return result_data

    except Exception as e:
        print(f"⚠️ Scraper API Error: {e}")
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scraper_client.py <url>")
        sys.exit(1)
    result = scrape_website(sys.argv[1])
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("❌ Scraping failed.")
