#!/usr/bin/env python3
"""
Campaign Context — Loads and provides campaign configuration to all GTM agents and skills.

The Campaign Context Object is the core abstraction that makes the GTM Engine domain-agnostic.
Instead of hardcoded OnCampus ERP / college references, every agent reads its instructions
from the active campaign context.

Sources (checked in order):
  1. MongoDB: campaigns collection (production)
  2. Local JSON file: config/sample_campaigns/*.json (development/testing)
  3. Environment variable: CAMPAIGN_CONTEXT_PATH (override)
"""
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
if not os.path.exists(_env_path):
    _env_path = '/app/.env'
load_dotenv(_env_path)

# Cache
_cached_context = None


class CampaignContext:
    """
    Provides structured access to the active campaign configuration.

    Usage:
        from campaign_context import load_campaign_context
        ctx = load_campaign_context("camp_abc123")

        print(ctx.product_name)         # "CloudSync Pro"
        print(ctx.target_personas)      # ["CTO", "VP Engineering"]
        print(ctx.research_pages)       # ["About", "Pricing", "Careers"]
        print(ctx.gap_mapping)          # {"No cloud storage": "CloudSync replaces..."}
        print(ctx.email_sequence)       # [{"stage": "introduction", ...}, ...]
        print(ctx.scoring_rubric)       # {"hot": {...}, "warm": {...}, "cold": {...}}
    """

    def __init__(self, raw: dict):
        self._raw = raw

    # --- Campaign Identity ---
    @property
    def campaign_id(self) -> str:
        return self._raw.get("campaign_id", "")

    @property
    def campaign_name(self) -> str:
        return self._raw.get("campaign_name", "")

    # --- Product ---
    @property
    def product(self) -> dict:
        return self._raw.get("product", {})

    @property
    def product_name(self) -> str:
        return self.product.get("name", "")

    @property
    def product_tagline(self) -> str:
        return self.product.get("tagline", "")

    @property
    def product_website(self) -> str:
        return self.product.get("website", "")

    @property
    def demo_url(self) -> str:
        return self.product.get("demo_url", "")

    @property
    def key_features(self) -> list:
        return self.product.get("key_features", [])

    @property
    def value_propositions(self) -> list:
        return self.product.get("value_propositions", [])

    # --- Audience ---
    @property
    def audience(self) -> dict:
        return self._raw.get("audience", {})

    @property
    def domain(self) -> str:
        return self.audience.get("domain", "")

    @property
    def target_type(self) -> str:
        return self.audience.get("target_type", "company")

    @property
    def ideal_profile(self) -> str:
        return self.audience.get("ideal_profile", "")

    @property
    def target_personas(self) -> list:
        return self.audience.get("target_personas", [])

    @property
    def locations(self) -> list:
        return self.audience.get("locations", [])

    @property
    def audience_filters(self) -> dict:
        return self.audience.get("filters", {})

    # --- Research Instructions ---
    @property
    def research_instructions(self) -> dict:
        return self._raw.get("research_instructions", {})

    @property
    def what_to_look_for(self) -> list:
        return self.research_instructions.get("what_to_look_for", [])

    @property
    def research_pages(self) -> list:
        return self.research_instructions.get("pages_to_crawl", [])

    @property
    def gap_mapping(self) -> dict:
        return self.research_instructions.get("gap_mapping", {})

    @property
    def domain_specific_fields(self) -> list:
        return self.research_instructions.get("domain_specific_fields", [])

    # --- Outreach Strategy ---
    @property
    def outreach_strategy(self) -> dict:
        return self._raw.get("outreach_strategy", {})

    @property
    def outreach_goal(self) -> str:
        return self.outreach_strategy.get("goal", "book_demo")

    @property
    def email_sequence(self) -> list:
        return self.outreach_strategy.get("email_sequence", [])

    @property
    def subject_line_template(self) -> str:
        return self.outreach_strategy.get("subject_line_template", "")

    @property
    def sender_persona(self) -> dict:
        return self.outreach_strategy.get("sender_persona", {})

    @property
    def sender_name(self) -> str:
        return self.sender_persona.get("name", "")

    @property
    def sender_title(self) -> str:
        return self.sender_persona.get("title", "")

    @property
    def sender_company(self) -> str:
        return self.sender_persona.get("company", "")

    # --- Scoring Rubric ---
    @property
    def scoring_rubric(self) -> dict:
        return self._raw.get("scoring_rubric", {})

    # --- Targets (inline) ---
    @property
    def targets(self) -> list:
        return self._raw.get("targets", [])

    # --- Raw Access ---
    @property
    def raw(self) -> dict:
        return self._raw

    # --- Serialization for Agent Prompts ---
    def to_product_brief(self) -> str:
        """Generates a text brief about the product for injection into agent prompts."""
        features = "\n".join(f"  - {f}" for f in self.key_features)
        vps = "\n".join(f"  - {v}" for v in self.value_propositions)
        return (
            f"Product: {self.product_name}\n"
            f"Tagline: {self.product_tagline}\n"
            f"Website: {self.product_website}\n"
            f"Demo URL: {self.demo_url}\n"
            f"Key Features:\n{features}\n"
            f"Value Propositions:\n{vps}"
        )

    def to_audience_brief(self) -> str:
        """Generates a text brief about the target audience."""
        personas = ", ".join(self.target_personas)
        locs = ", ".join(self.locations) if self.locations else "Global"
        return (
            f"Domain: {self.domain}\n"
            f"Target Type: {self.target_type}\n"
            f"Ideal Profile: {self.ideal_profile}\n"
            f"Decision Makers: {personas}\n"
            f"Locations: {locs}"
        )

    def to_research_brief(self) -> str:
        """Generates research instructions for the Researcher and Summarizer agents."""
        look_for = "\n".join(f"  - {item}" for item in self.what_to_look_for)
        pages = ", ".join(self.research_pages)
        gaps = "\n".join(f"  - \"{k}\" → {v}" for k, v in self.gap_mapping.items())
        extras = "\n".join(f"  - {f}" for f in self.domain_specific_fields) if self.domain_specific_fields else "  (none)"
        return (
            f"What to Look For:\n{look_for}\n"
            f"Pages to Crawl: {pages}\n"
            f"Gap-to-Solution Mapping:\n{gaps}\n"
            f"Domain-Specific Fields:\n{extras}"
        )

    def to_outreach_brief(self) -> str:
        """Generates outreach strategy context for the Outreach-Writer agent."""
        goal = self.outreach_goal.replace("_", " ").title()
        sender = f"{self.sender_name}, {self.sender_title} at {self.sender_company}"
        seq_lines = []
        for step in self.email_sequence:
            trigger = f" (trigger: {step.get('trigger', 'immediate')})" if step.get('trigger') else ""
            seq_lines.append(
                f"  - Stage: {step['stage']} | Day {step['delay_days']} | Tone: {step['tone']} | Angle: {step['angle']}{trigger}"
            )
        seq = "\n".join(seq_lines)
        return (
            f"Goal: {goal}\n"
            f"Sender: {sender}\n"
            f"Subject Template: {self.subject_line_template}\n"
            f"Email Sequence:\n{seq}"
        )

    def to_scoring_brief(self) -> str:
        """Generates scoring rubric for the Summarizer agent."""
        lines = []
        for tier in ["hot", "warm", "cold"]:
            data = self.scoring_rubric.get(tier, {})
            emoji = {"hot": "🟢", "warm": "🟡", "cold": "🔴"}.get(tier, "⚪")
            lines.append(f"  {emoji} {tier.upper()} (>={data.get('min_score', 0)}): {data.get('criteria', '')}")
        return "Lead Scoring Rubric:\n" + "\n".join(lines)

    def to_full_context(self) -> str:
        """Generates the complete campaign context for the Orchestrator."""
        return (
            f"=== CAMPAIGN: {self.campaign_name} (ID: {self.campaign_id}) ===\n\n"
            f"--- PRODUCT ---\n{self.to_product_brief()}\n\n"
            f"--- AUDIENCE ---\n{self.to_audience_brief()}\n\n"
            f"--- RESEARCH INSTRUCTIONS ---\n{self.to_research_brief()}\n\n"
            f"--- OUTREACH STRATEGY ---\n{self.to_outreach_brief()}\n\n"
            f"--- SCORING ---\n{self.to_scoring_brief()}"
        )


def load_campaign_context(campaign_id: str = None) -> CampaignContext:
    """
    Load campaign context from the best available source.

    Priority:
      1. CAMPAIGN_CONTEXT_PATH env var (local JSON file override)
      2. MongoDB campaigns collection (by campaign_id)
      3. Default sample campaign (config/sample_campaigns/oncampus_erp.json)

    Args:
        campaign_id: Optional campaign ID to fetch from MongoDB.

    Returns:
        CampaignContext instance.
    """
    global _cached_context

    # Check env override first (for development/testing)
    override_path = os.getenv("CAMPAIGN_CONTEXT_PATH")
    if override_path and os.path.exists(override_path):
        print(f"📋 Loading campaign context from file: {override_path}")
        with open(override_path, "r") as f:
            raw = json.load(f)
        _cached_context = CampaignContext(raw)
        return _cached_context

    # Try MongoDB
    if campaign_id:
        try:
            from pymongo import MongoClient
            mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
            db_name = os.getenv("DB_NAME", "gtm_marketing")
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            db = client[db_name]

            campaign = db.campaigns.find_one({"campaign_id": campaign_id})
            if not campaign:
                # Also try by MongoDB _id
                from bson.objectid import ObjectId
                try:
                    campaign = db.campaigns.find_one({"_id": ObjectId(campaign_id)})
                except Exception:
                    pass

            if campaign:
                # Convert ObjectId to string for JSON compatibility
                campaign.pop("_id", None)
                print(f"📋 Loaded campaign '{campaign.get('campaign_name', campaign_id)}' from MongoDB.")
                _cached_context = CampaignContext(campaign)
                return _cached_context
            else:
                print(f"⚠️ Campaign '{campaign_id}' not found in MongoDB. Falling back to default.")
        except ImportError:
            print("⚠️ pymongo not available. Falling back to local file.")
        except Exception as e:
            print(f"⚠️ MongoDB error: {e}. Falling back to local file.")

    # Fallback: default sample campaign
    config_dir = Path(__file__).parent
    default_path = config_dir / "sample_campaigns" / "oncampus_erp.json"
    if default_path.exists():
        print(f"📋 Loading default campaign context from: {default_path}")
        with open(default_path, "r") as f:
            raw = json.load(f)
        _cached_context = CampaignContext(raw)
        return _cached_context

    raise FileNotFoundError(
        "No campaign context found. Provide CAMPAIGN_CONTEXT_PATH env var, "
        "a valid campaign_id in MongoDB, or place a default campaign in "
        "config/sample_campaigns/oncampus_erp.json"
    )


def get_cached_context() -> CampaignContext:
    """Return the cached campaign context if available, or load default."""
    global _cached_context
    if _cached_context is None:
        return load_campaign_context()
    return _cached_context


# --- CLI for testing ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Load and inspect a campaign context")
    parser.add_argument("--campaign-id", type=str, help="Campaign ID to load from MongoDB")
    parser.add_argument("--file", type=str, help="Path to a campaign JSON file")
    parser.add_argument("--brief", choices=["product", "audience", "research", "outreach", "scoring", "full"],
                        default="full", help="Which brief to print")
    args = parser.parse_args()

    if args.file:
        os.environ["CAMPAIGN_CONTEXT_PATH"] = args.file

    ctx = load_campaign_context(campaign_id=args.campaign_id)

    briefs = {
        "product": ctx.to_product_brief,
        "audience": ctx.to_audience_brief,
        "research": ctx.to_research_brief,
        "outreach": ctx.to_outreach_brief,
        "scoring": ctx.to_scoring_brief,
        "full": ctx.to_full_context,
    }
    print(briefs[args.brief]())
