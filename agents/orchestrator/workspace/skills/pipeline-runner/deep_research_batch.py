#!/usr/bin/env python3
"""
Deep Research Batch — V4 Multi-Agent Pipeline Orchestrator.
Invokes researcher, summarizer, and outreach-writer agents for each lead.
"""
import json
import subprocess
import os
import sys
import time
import argparse
import socket
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', '.env')
if not os.path.exists(env_path):
    env_path = '/app/.env'
load_dotenv(env_path)

# Add gsheet-manager skill to path
gsheet_skill_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gsheet-manager')
sys.path.insert(0, gsheet_skill_path)


def is_website_reachable(url):
    """Quick DNS check to see if the website exists."""
    if not url or url.strip().lower() == "n/a":
        return False
    try:
        clean_url = url.strip()
        if not clean_url.startswith('http'):
            clean_url = 'http://' + clean_url
        hostname = urlparse(clean_url).hostname
        if not hostname:
            return False
        socket.gethostbyname(hostname)
        return True
    except (socket.gaierror, socket.timeout):
        return False


def run_agent(agent_id, message, session_suffix, env):
    """Invoke an OpenClaw agent by ID and return its output."""
    ts = int(time.time())
    cmd = [
        "npx", "openclaw", "agent",
        "--agent", agent_id,
        "--local",
        "--session-id", f"{agent_id}-{session_suffix}-{ts}",
        "--message", message,
        "--json"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=600)
        if result.returncode == 0 and "{" in result.stdout:
            json_str = result.stdout[result.stdout.find("{"):result.stdout.rfind("}") + 1]
            return json.loads(json_str)
        else:
            print(f"⚠️ Agent {agent_id} returned non-JSON: {result.stderr[-200:]}")
            return None
    except subprocess.TimeoutExpired:
        print(f"⏰ Agent {agent_id} timed out.")
        return None
    except Exception as e:
        print(f"❌ Agent {agent_id} error: {e}")
        return None


def process_lead(lead, env):
    """Process a single lead through the 3-agent pipeline."""
    name = lead.get('college_name')
    url = lead.get('website')
    idx = lead.get('row_idx')

    print(f"\n{'='*60}")
    print(f"🔍 Processing: {name} ({url}) [Row: {idx}]")
    print(f"{'='*60}")

    # Step 0: Reachability check
    if not is_website_reachable(url):
        print(f"⏩ Website unreachable — marking as OUT OF SCOPE.")
        unreachable_data = {
            "college_name": name, "website": url, "row_idx": idx,
            "website_extraction_research": f"### Summary\n- Institution: {name}\n- Website Type: Unreachable\n\n### Digital Gaps Identified\n- Website unreachable (DNS resolution failed).\n\n### Key Insights\n- GTM Assessment: OUT OF SCOPE\nLead Score: 🔴 0 - Unreachable #",
            "contacts": {"emails": [], "phones": [], "linkedin_profiles": []},
            "classification": {"target_persona": "Unknown"},
            "tracking": {"status": "unreachable"}
        }
        temp_file = f"/tmp/temp_unreachable_{idx}.json"
        with open(temp_file, "w") as f:
            json.dump(unreachable_data, f)
        update_script = os.path.join(gsheet_skill_path, "update_excel.py")
        subprocess.run([sys.executable, update_script, temp_file])
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return

    # Step 1: RESEARCHER — Scrape the website
    print(f"🔬 [1/3] @researcher — Scraping {url}...")
    researcher_result = run_agent(
        "researcher",
        f"Scrape and extract raw data from '{name}' at '{url}'. Return ALL raw content, contacts, and technical details as JSON.",
        f"row-{idx}",
        env
    )
    if not researcher_result:
        print(f"❌ Researcher failed for {name}. Skipping.")
        return

    # Step 2: SUMMARIZER — Analyze raw data
    print(f"📝 [2/3] @summarizer — Analyzing raw data for {name}...")
    raw_data_str = json.dumps(researcher_result, indent=2)
    summarizer_result = run_agent(
        "summarizer",
        f"Analyze this raw scraped data for '{name}' ({url}):\n\n{raw_data_str}\n\nGenerate: strategic summary, NAAC analysis, digital gaps, contacts extraction, lead score. Output as JSON.",
        f"row-{idx}",
        env
    )
    if not summarizer_result:
        print(f"⚠️ Summarizer failed for {name}. Using raw researcher data.")
        summarizer_result = researcher_result

    # Step 3: OUTREACH-WRITER — Generate tracked emails
    print(f"✍️ [3/3] @outreach-writer — Generating outreach for {name}...")
    summary_str = json.dumps(summarizer_result, indent=2)
    outreach_result = run_agent(
        "outreach-writer",
        f"Generate 3 hyper-personalized tracked outreach emails for '{name}' based on this analysis:\n\n{summary_str}\n\nCreate Analytica tracking first, then inject pixel and redirect links. Output JSON with outreach_templates and tracking.",
        f"row-{idx}",
        env
    )

    # Step 4: MERGE & SAVE
    final_data = summarizer_result.copy()
    if outreach_result:
        final_data['outreach_templates'] = outreach_result.get('outreach_templates', {})
        final_data['tracking'] = outreach_result.get('tracking', {})
        final_data['tracking_id'] = outreach_result.get('tracking_id', '')
        final_data['pixel_url'] = outreach_result.get('pixel_url', '')
    final_data['row_idx'] = idx

    temp_file = f"/tmp/temp_res_{idx}.json"
    with open(temp_file, "w") as f:
        json.dump(final_data, f)
    update_script = os.path.join(gsheet_skill_path, "update_excel.py")
    subprocess.run([sys.executable, update_script, temp_file])
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print(f"✅ Pipeline complete for {name}.")


def run_deep_research(row_idx=None, batch_size=None, start_row=None):
    """Main entry point for the multi-agent research pipeline."""
    if row_idx:
        print(f"🚀 Starting V4 Multi-Agent Pipeline for Row {row_idx}...")
    else:
        actual_size = batch_size if batch_size else 2
        print(f"🚀 Starting V4 Multi-Agent Pipeline ({actual_size} leads)...")

    # Setup environment
    env = os.environ.copy()
    env["OPENCLAW_CONFIG_PATH"] = os.getenv("OPENCLAW_CONFIG_PATH", "/app/openclaw.json")

    # Get leads
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

    # Process leads (sequential for multi-agent to avoid conflicts)
    for lead in leads:
        process_lead(lead, env)

    print(f"\n✨ V4 Pipeline complete. Check Google Sheet for updates.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GTM V4 Multi-Agent Pipeline")
    parser.add_argument("count", type=int, nargs="?", help="Number of leads to research")
    parser.add_argument("--row", "-r", type=int, help="Target a specific row index")
    parser.add_argument("--start", "-s", type=int, help="Start batching from this row index")

    args = parser.parse_args()

    if args.row:
        run_deep_research(row_idx=args.row)
    else:
        run_deep_research(batch_size=args.count, start_row=args.start)
