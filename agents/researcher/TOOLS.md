# TOOLS.md — Researcher Agent

## Custom Skills

### scraper
Cache-first web scraping via Scraper API with async polling.
- `scraper_client.py` — Handles cache check, job trigger, polling, result fetch
- Usage: `python3 workspace/skills/scraper/scraper_client.py <url>`

### website-analyzer
Website technology and structure analysis.
- `analyzer.py` — DNS reachability check, technology detection
- Usage: `python3 workspace/skills/website-analyzer/analyzer.py <url>`
