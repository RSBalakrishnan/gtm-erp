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
# Load db-manager and config
db_skill_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db-manager')
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', 'config')
sys.path.insert(0, db_skill_path)
sys.path.insert(0, config_path)

from db_helper import DBHelper
from campaign_context import load_campaign_context


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


def process_target(target, env, db, ctx):
    """Process a single target through the 3-agent pipeline with campaign context."""
    target_id = target.get('id')
    name = target.get('name') or target.get('target_name')
    url = target.get('website')

    print(f"\n{'='*60}")
    print(f"🔍 Processing: {name} ({url}) [ID: {target_id}]")
    print(f"{'='*60}")

    # Mark as Researching
    db.update_target(target_id, {"status": "RESEARCHING"})

    # Step 0: Reachability check
    if not is_website_reachable(url):
        print(f"⏩ Website unreachable — marking as OUT OF SCOPE.")
        db.update_target(target_id, {
            "status": "UNREACHABLE",
            "research_summary": f"### Summary\n- Entity: {name}\n- Status: Unreachable\n\n### Key Insights\n- GTM Assessment: OUT OF SCOPE\nLead Score: 🔴 0 - Unreachable #"
        })
        return

    # Step 1: RESEARCHER — Scrape the website
    print(f"🔬 [1/3] @researcher — Scraping {url}...")
    research_brief = ctx.to_research_brief()
    researcher_result = run_agent(
        "researcher",
        f"CAMPAIGN CONTEXT:\n{research_brief}\n\nTASK: Scrape and extract data from '{name}' at '{url}'. Focus on the domain-specific findings requested in the context.",
        f"target-{target_id}",
        env
    )
    if not researcher_result:
        print(f"❌ Researcher failed for {name}. Skipping.")
        db.update_target(target_id, {"status": "FAILED_RESEARCH"})
        return

    # Step 2: SUMMARIZER — Analyze raw data
    print(f"📝 [2/3] @summarizer — Analyzing raw data for {name}...")
    db.update_target(target_id, {"status": "ANALYZING"})
    scoring_brief = ctx.to_scoring_brief()
    raw_data_str = json.dumps(researcher_result, indent=2)
    summarizer_result = run_agent(
        "summarizer",
        f"CAMPAIGN CONTEXT:\n{scoring_brief}\n\nTASK: Analyze this raw data for '{name}' ({url}):\n\n{raw_data_str}\n\nGenerate strategic summary and lead score based on the campaign rubric.",
        f"target-{target_id}",
        env
    )
    if not summarizer_result:
        print(f"⚠️ Summarizer failed for {name}. Using raw researcher data.")
        summarizer_result = researcher_result

    # Step 3: OUTREACH-WRITER — Generate tracked emails
    print(f"✍️ [3/3] @outreach-writer — Generating outreach for {name}...")
    product_brief = ctx.to_product_brief()
    outreach_strategy = ctx.to_outreach_brief()
    summary_str = json.dumps(summarizer_result, indent=2)
    outreach_result = run_agent(
        "outreach-writer",
        f"CAMPAIGN CONTEXT:\n{product_brief}\n{outreach_strategy}\n\nTASK: Generate hyper-personalized tracked emails for '{name}' based on this analysis:\n\n{summary_str}",
        f"target-{target_id}",
        env
    )

    # Step 4: SAVE TO DB
    db_update = {
        "status": "COMPLETED",
        "lead_score": summarizer_result.get('lead_score_numeric', 0),
        "lead_tier": summarizer_result.get('lead_tier', 'COLD'),
        "research_summary": summarizer_result.get('analysis_research', ''),
        "emails": summarizer_result.get('contacts', {}).get('emails', []),
        "target_persona": summarizer_result.get('classification', {}).get('persona_identified', '')
    }
    
    if outreach_result:
        templates = outreach_result.get('outreach_templates', {})
        for i in range(1, 4):
            key = f"email_{i}"
            if templates.get(key):
                db_update[f"outreach_email_{i}"] = templates[key]
        
        db_update["tracking_id"] = outreach_result.get('tracking_id', '')
        db_update["pixel_url"] = outreach_result.get('pixel_url', '')

    db.update_target(target_id, db_update)
    print(f"✅ Pipeline complete for {name}. Data saved to MongoDB.")


def run_deep_research(campaign_id=None, batch_size=None):
    """Main entry point for the multi-agent research pipeline."""
    print(f"🚀 Starting Generic GTM Multi-Agent Pipeline...")

    # Load Context
    try:
        ctx = load_campaign_context(campaign_id)
        print(f"📊 Active Campaign: {ctx.campaign_name}")
    except Exception as e:
        print(f"❌ Could not load campaign context: {e}")
        return

    # Setup environment
    env = os.environ.copy()
    env["OPENCLAW_CONFIG_PATH"] = os.getenv("OPENCLAW_CONFIG_PATH", "/app/openclaw.json")

    # Get targets from DB
    try:
        db = DBHelper()
        targets = db.get_pending_targets(campaign_id)
        
        if batch_size:
            targets = targets[:batch_size]
            
    except Exception as e:
        print(f"❌ Error connecting to DB: {e}")
        return

    if not targets:
        print(f"❌ No PENDING targets found for campaign '{campaign_id or 'default'}'.")
        return

    print(f"📈 Found {len(targets)} targets to process.")

    # Process targets
    for target in targets:
        process_target(target, env, db, ctx)

    print(f"\n✨ Pipeline complete for campaign: {ctx.campaign_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generic GTM Multi-Agent Pipeline")
    parser.add_argument("--campaign", type=str, help="Campaign ID to process")
    parser.add_argument("--count", type=int, help="Number of targets to research")

    args = parser.parse_args()

    run_deep_research(campaign_id=args.campaign, batch_size=args.count)
