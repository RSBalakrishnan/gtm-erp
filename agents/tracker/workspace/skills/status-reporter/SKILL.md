---
name: status-reporter
description: Generate pipeline status reports combining Google Sheet data with Analytica engagement metrics
tools:
  - shell
---

# Status Reporter Skill

## Purpose
Generates comprehensive lead status reports by querying the Google Sheet and enriching with real-time Analytica engagement data.

## Usage
```bash
# Full report
python3 workspace/skills/status-reporter/status_report.py

# Search specific lead
python3 workspace/skills/status-reporter/status_report.py "college name"
```
