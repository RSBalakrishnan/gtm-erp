---
name: scraper
description: Cache-first web scraping via Scraper API with automatic async polling
tools:
  - shell
  - fetch
---

# Scraper Skill

## Purpose
Handles all Scraper API interactions: cache checks, job triggering, status polling, and result fetching.

## Usage
```bash
python3 workspace/skills/scraper/scraper_client.py <url>
```

## Environment Variables
- `SCRAPER_API_URL` — Scraper API base URL
