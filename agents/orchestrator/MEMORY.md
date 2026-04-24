# Agent Memory
This file serves as the persistent memory for the GTM Sales Orchestrator V4.

## Version History
- V2: Single-agent with manual research
- V3: Integrated Analytica tracking, cache-first scraping, live Google Sheet
- V4: True multi-agent architecture with 5 specialist agents + Docker deployment

## Architecture
- Orchestrator delegates to: researcher, summarizer, outreach-writer, tracker
- Google Sheet (ID loaded from `GOOGLE_SHEET_ID` in `.env`) is the ONLY source of truth
- Analytica provides real-time email open and link click tracking
- Scraper API provides cache-first website data extraction
