# TOOLS.md — Tracker Agent

## Custom Skills

### analytica-monitor
Query Analytica API for email open and link click analytics.
- `analytica_helper.py` — Query functions: `get_email_status()`, `get_link_analytics()`, `get_journey()`
- Usage: `python3 workspace/skills/analytica-monitor/analytica_helper.py <tracking_id>`

### status-reporter
Generate pipeline status reports from Google Sheet + Analytica data.
- `status_report.py` — JSON status report generator
- Usage: `python3 workspace/skills/status-reporter/status_report.py`
- Usage: `python3 workspace/skills/status-reporter/status_report.py <search_query>`
