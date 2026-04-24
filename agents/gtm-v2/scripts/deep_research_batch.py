#!/usr/bin/env python3
import json
import subprocess
import os
import time
import argparse
import socket
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load credentials from .env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(env_path)

def is_website_reachable(url):
    """Perform a quick DNS check to see if the website exists."""
    if not url or url.strip().lower() == "n/a":
        return False
    try:
        # Normalize URL to get the hostname
        clean_url = url.strip()
        if not clean_url.startswith('http'):
            clean_url = 'http://' + clean_url
        hostname = urlparse(clean_url).hostname
        if not hostname:
            return False
            
        # Try DNS resolution
        socket.gethostbyname(hostname)
        return True
    except (socket.gaierror, socket.timeout):
        return False

def call_scraper_api(url):
    """Call the external scraper API with cache-first strategy."""
    api_url = os.getenv("SCRAPER_API_URL")
    try:
        # Step 0: Check cache first
        print(f"📡 Checking cache for {url}...")
        exists_res = requests.get(f"{api_url}/scrape/exists", params={"websiteURL": url}, timeout=10)
        if exists_res.status_code == 200 and exists_res.json().get("exists"):
            print(f"⚡ Cache HIT for {url}. Fetching instantly...")
            data_res = requests.get(f"{api_url}/scrape/getData", params={"websiteURL": url}, timeout=10)
            if data_res.status_code == 200:
                return data_res.json()

        # Step 1: Full discovery if cache miss
        print(f"📡 Calling Scraper API for {url} (Cache Miss)...")
        res = requests.post(f"{api_url}/scrape", json={"websiteURL": url}, timeout=15)
        if res.status_code == 200:
            job_id = res.json().get("job_id")
            print(f"⏳ Scraper Job {job_id} started. Polling...")
            result_data = None
            for i in range(10): # 5 min total polling (30s * 10)
                status_res = requests.get(f"{api_url}/scrape/{job_id}/status", timeout=10)
                if status_res.status_code == 200:
                    status = status_res.json().get("status")
                    print(f"   [{i*30}s] Scraper Status: {status}")
                    if status == "completed":
                        result_res = requests.get(f"{api_url}/scrape/{job_id}/result", timeout=10)
                        if result_res.status_code == 200:
                            result_data = result_res.json()
                            break
                    elif status == "failed":
                        return None
                time.sleep(30)
            
            if result_data:
                # Step 2: After job completes, get page-level breakdown
                try:
                    pages_res = requests.get(f"{api_url}/scrape/{job_id}/pages", timeout=10)
                    if pages_res.status_code == 200:
                        result_data["pages_breakdown"] = pages_res.json()
                except Exception as e:
                    print(f"⚠️ Could not fetch pages breakdown: {e}")
                return result_data

    except Exception as e:
        print(f"⚠️ Scraper API Error: {e}")
    return None

def run_deep_research(row_idx=None, batch_size=None, start_row=None):
    if row_idx:
        print(f"🚀 Starting Targeted GTM Research for Row {row_idx}...")
    elif start_row:
        print(f"🚀 Starting GTM Deep Research Batch ({batch_size}) from Row {start_row}...")
    else:
        actual_size = batch_size if batch_size else 2
        print(f"🚀 Starting GTM Deep Research Batch ({actual_size} leads)...")
    
    # Ensure current directory is gtm-v2/scripts
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 0. Cleanup any stale locks to prevent stalls
    try:
        session_dir = os.path.expanduser("~/.openclaw/agents/gtm-v2/sessions")
        if os.path.exists(session_dir):
            subprocess.run(f"find {session_dir} -name '*.lock' -delete", shell=True)
            print("🧹 Cleared stale session locks.")
    except Exception as e:
        print(f"⚠️ Lock cleanup warning: {e}")
    
    # 1. Get the leads
    try:
        from gsheets_helper import GSheetsHelper
        helper = GSheetsHelper()
        if row_idx:
            rows = helper.get_all_rows()
            if row_idx <= len(rows):
                row = rows[row_idx - 1]
                leads = [{
                    'college_name': row[4] if len(row) > 4 else "Unknown",
                    'website': row[7] if len(row) > 7 else "",
                    'row_idx': row_idx
                }]
            else:
                print(f"❌ Row {row_idx} out of range.")
                return
        else:
            from batch_runner import get_next_batch
            leads = get_next_batch(batch_size or 2, start_from=start_row)
            if isinstance(leads, dict) and "error" in leads:
                print(f"❌ Error getting leads: {leads['error']}")
                return
    except Exception as e:
        print(f"❌ Error getting leads: {e}")
        return

    if not leads:
        print("❌ No leads found to process.")
        return

    # 2. Process each lead concurrently
    import concurrent.futures

    def process_lead(lead):
        name = lead.get('college_name')
        url = lead.get('website')
        idx = lead.get('row_idx')
        ts = int(time.time())
        print(f"\n🔍 [Step 1/2] Agent 1 Technical Audit: {name} ({url}) [Row: {idx}]")
        
        if not is_website_reachable(url):
            print(f"⏩ Website unreachable - Skipping Agent for {name}.")
            unreachable_data = {
                "college_name": name, "website": url, "row_idx": idx,
                "website_extraction_research": f"### Summary\n- Institution: {name}\n- Website Type: Unreachable\n\n### Digital Gaps Identified\n- Website unreachable (DNS resolution failed). Marking as OUT OF SCOPE. #",
                "outreach_templates": { "email_1": f"Dear Admissions Head,\n\nI was trying to reach {name} website but it seems to be down...", "email_2": "...", "email_3": "..." },
                "contacts": { "emails": [], "phones": [], "linkedin_profiles": [] },
                "classification": { "target_persona": "Unknown" }, "tracking": { "status": "unreachable" }
            }
            temp_file = f"temp_unreachable_{idx}.json"
            with open(temp_file, "w") as f: json.dump(unreachable_data, f)
            subprocess.run([sys.executable, "update_excel.py", temp_file])
            if os.path.exists(temp_file): os.remove(temp_file)
            return

        env = os.environ.copy()
        env["OPENCLAW_CONFIG_PATH"] = os.path.abspath("../batch-openclaw.json")
        env["PATH"] = f"/usr/local/opt/node/bin:{env.get('PATH', '')}"
        
        worker_home = f"/tmp/gtm-worker-{idx}-{ts}"
        os.makedirs(worker_home, exist_ok=True)
        env["HOME"] = worker_home

        def clear_worker_locks():
            try:
                l_path = os.path.join(worker_home, ".openclaw/agents/gtm-v2/sessions")
                if os.path.exists(l_path):
                    subprocess.run(f"find {l_path} -name '*.lock' -delete", shell=True)
            except: pass

        # --- AGENT 1 PHASE: SCRAPER API CALL ---
        api_data = call_scraper_api(url)
        context_str = ""
        if api_data:
            print(f"✅ Scraper API returned technical data for {name}.")
            context_str = f"HERE IS THE RAW TECHNICAL REPORT FROM THE SCRAPER:\n{json.dumps(api_data, indent=2)}\n\n"

        # --- PHASE 1: AGENT 1 (THE STRATEGIC SUMMARIZER) ---
        clear_worker_locks()
        prompt_agent_1 = (
            f"You are Agent 1 (Strategic Summarizer). Perform an EXHAUSTIVE technical audit of '{name}' at '{url}'.\n"
            f"{context_str}"
            "1. CRAWL/ANALYZE the site. Find: NAAC status, Affiliation, total courses, and Digital Gaps (e.g. outdated framesets, PDF-only forms).\n"
            "2. OUTPUT the 'Strategic Summary' following the EXACT format in SOUL.md.\n"
            "3. BE TECHNICAL: Mention framesets, HTML versions, or specific missing modules (Admissions/Fees).\n"
            "Output MANDATORY JSON with college_name, website, website_extraction_research, contacts, and classification."
        )
        
        cmd_1 = ["/usr/local/opt/node/bin/npx", "openclaw", "agent", "--agent", "gtm-v2", "--local", "--session-id", f"audit-{idx}-{ts}", "--message", prompt_agent_1, "--json"]

        try:
            print(f"⏳ Agent 1 is finalizing Technical Audit for {name} (10m quality limit)...")
            res_1 = subprocess.run(cmd_1, capture_output=True, text=True, env=env, timeout=600)
            
            if res_1.returncode != 0 or "{" not in res_1.stdout:
                print(f"⚠️ Agent 1 failed to generate summary for {name}. Fallback error: {res_1.stderr[-200:]}")
                return
            
            # Extract Agent 1's strategic research to feed into Agent 2
            audit_json_str = res_1.stdout[res_1.stdout.find("{"):res_1.stdout.rfind("}")+1]
            audit_data = json.loads(audit_json_str)
            strategic_summary = audit_data.get('website_extraction_research', '')

            # --- NEW V3: CREATE ANALYTICA TRACKING ---
            tracking_assets = {"tracking_id": "", "pixel_url": "", "redirect_base": ""}
            try:
                from analytica_helper import create_tracking_id
                cta_urls = ["https://oncampuserp.com/demo", "https://oncampuserp.com"]
                analytica_result = create_tracking_id(cta_urls)
                tracking_assets["tracking_id"] = analytica_result.get("trackingId", "")
                tracking_assets["pixel_url"] = analytica_result.get("pixelUrl", "")
                tracking_assets["redirect_base"] = analytica_result.get("redirectUrlBase", "")
                print(f"🎯 Analytica Tracking ID: {tracking_assets['tracking_id']}")
            except Exception as e:
                print(f"⚠️ Analytica tracking creation failed: {e}")

            # --- PHASE 2: AGENT 2 (THE OUTREACH GHOSTWRITER) ---
            time.sleep(3) # Breathing room for FS locks
            clear_worker_locks()
            print(f"✍️ [Step 2/2] Agent 2 Generating Outreach for: {name}")
            
            prompt_agent_2 = (
                f"You are Agent 2 (Outreach Ghostwriter). Take this STRATEGIC AUDIT of '{name}':\n\n"
                f"{strategic_summary}\n\n"
                "BUSINESS CONTEXT (OnCampus ERP):\n"
                "- We offer: Mobile-first ERP, WhatsApp/SMS Parent alerts, Integrated NEET/Admission Portals, 40% Admin workload reduction.\n"
                "- GOAL: Map the Technical Debt found by Agent 1 to our specific solutions.\n"
                "TASK: Generate 3 HIGHLY PERSONALIZED outreach emails. No generic templates. Reference specific audit findings.\n\n"
                "TRACKING ASSETS (MANDATORY - embed these in every email):\n"
                f"- Tracking ID: {tracking_assets['tracking_id']}\n"
                f"- Pixel URL (invisible image at bottom of EVERY email): {tracking_assets['pixel_url']}\n"
                f"- Redirect Base (replace ALL CTA links): {tracking_assets['redirect_base']}\n"
                "RULES:\n"
                "1. At the bottom of EVERY email, add this invisible pixel: <img src=\"PIXEL_URL\" width=\"1\" height=\"1\" style=\"display:none\" />\n"
                "2. Replace ALL links to oncampuserp.com with: REDIRECT_BASE + encoded_original_url\n"
                "3. Include tracking_id in your output JSON.\n\n"
                "Output MANDATORY JSON with outreach_templates: {email_1, email_2, email_3} and tracking: {status: 'ready_for_outreach'}."
            )
            
            cmd_2 = ["/usr/local/opt/node/bin/npx", "openclaw", "agent", "--agent", "gtm-v2", "--local", "--session-id", f"outreach-{idx}-{ts}", "--message", prompt_agent_2, "--json"]
            res_2 = subprocess.run(cmd_2, capture_output=True, text=True, env=env, timeout=300)
            
            if res_2.returncode == 0 and "{" in res_2.stdout:
                outreach_json_str = res_2.stdout[res_2.stdout.find("{"):res_2.stdout.rfind("}")+1]
                outreach_data = json.loads(outreach_json_str)
                
                # Merge the results
                final_data = audit_data.copy()
                final_data['outreach_templates'] = outreach_data.get('outreach_templates', {})
                final_data['tracking'] = outreach_data.get('tracking', {})
                final_data['tracking_id'] = tracking_assets['tracking_id']
                final_data['pixel_url'] = tracking_assets['pixel_url']
                final_data['row_idx'] = idx

                temp_file = f"temp_res_{idx}.json"
                with open(temp_file, "w") as f: json.dump(final_data, f)
                subprocess.run([sys.executable, "update_excel.py", temp_file])
                if os.path.exists(temp_file): os.remove(temp_file)
                print(f"✅ Multi-Agent Pipeline complete for {name}.")

        except subprocess.TimeoutExpired:
            print(f"⏰ Pipeline timeout reached for {name}.")
        except Exception as e:
            print(f"❌ Pipeline error: {e}")

    # Launch the thread pool
    print(f"\n🚀 Launching 10 parallel workers for maximum speed...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_lead, leads)

    print("\n✨ Processing complete. Check Google Sheet for updates.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GTM Deep Research Batch Tool")
    parser.add_argument("count", type=int, nargs="?", help="Number of leads to research (batch size)")
    parser.add_argument("--row", "-r", type=int, help="Target a specific row index")
    parser.add_argument("--start", "-s", type=int, help="Start batching from this row index")
    
    args = parser.parse_args()
    
    if args.row:
        run_deep_research(row_idx=args.row)
    else:
        run_deep_research(batch_size=args.count, start_row=args.start)
