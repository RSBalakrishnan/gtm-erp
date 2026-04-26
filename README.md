# Autonomous College ERP GTM Engine: Project Requirements

This document outlines the full set of requirements to achieve parity with the **"Engineering the Autonomous GTM Engine"** technical architecture. Use this as your pre-flight checklist before launching the daily autonomous scheduler.

## 1. Infrastructure Requirements (Localhost)
- **OpenClaw CLI**: Version 2026.3+ (Check with `openclaw --version`).
- **Ollama Engine**: Must be running on port 11434 with the following models pulled:
  - `llama3.2:latest` (Data Cleaning & Formatting)
  - `phi3:mini` (Enrichment Scoring)
  - `qwen2.5:7b` (Technical Scraping & Intent Analysis)
- **Node.js**: Version 22+ (for Gateway and MCP servers).
- **Python**: Version 3.9+ (for auxiliary sourcing scripts).

## 2. Mandatory API Keys
Environment variables must be set in your terminal or [run-gtm.sh](file:///Users/apple/Desktop/gtm/run-gtm.sh):

| Key | Purpose | Phase |
| :--- | :--- | :--- |
| `MINIMAX_API_KEY` | Premium Reasoning & Outreach (m2.7) | Phase 3 |
| `SMARTLEAD_API_KEY` | Automated Email Outreach & Reply Monitoring | Phase 4 |
| `APIFY_API_KEY` | Deep Web Scraping (Google Maps/Lead Finder) | Phase 1 |
| `HUNTER_API_KEY` | Waterfall Lead Enrichment (Contact Emails) | Phase 2 |
| `BUILTWITH_API_KEY` | Technographic Signals (e.g., detecting Ellucian) | Phase 1 |

## 3. Configuration & Governance (The Nervous System)
Ensure the following files are synced with the [blueprints](file:///Users/apple/Desktop/gtm/agents/gtm-engine/):

- **[openclaw.json](file:///Users/apple/Desktop/gtm/config/openclaw.json)**: Must contain the `minimax` provider and `mcpServers` definitions.
- **[SOUL.md](file:///Users/apple/Desktop/gtm/agents/gtm-engine/SOUL.md)**: Defines the **Closed-Loop Workflow** (Trigger → Context → Decision → Action → Confirmation).
- **[AGENTS.md](file:///Users/apple/Desktop/gtm/agents/gtm-engine/AGENTS.md)**: Defines the 10-day multi-channel outreach strategy.
- **[HEARTBEAT.md](file:///Users/apple/Desktop/gtm/agents/gtm-engine/HEARTBEAT.md)**: Configured for the daily 08:00 AM autonomous run.

## 4. Third-Party Integrations (MCP/Skills)
The engine relies on the following native OpenClaw skills:
- **`browser`**: For visiting university portals and detecting technical deadlocks.
- **`linkedin`**: For profile views and connection requests.
- **`gog`**: For syncing leads to Google Sheets for "Vibe Checks."
- **`fetch`**: For high-speed institutional research.

## 5. Security & Sandbox (Recommended)
- **Docker**: For running agents in isolated containers to ensure system safety during shell command execution (`exec`).

---
**Status**: Ready for Configuration. 
*Next Step: Update your `run-gtm.sh` with the API keys listed above.*
