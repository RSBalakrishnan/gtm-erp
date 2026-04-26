---
name: analytica-monitor
description: Query Analytica API for email open and link click analytics per tracking ID
tools:
  - shell
  - fetch
---

# Analytica Monitor Skill

## Purpose
Queries the Analytica tracking API for real-time email engagement data.

## Usage
```bash
# Query a specific tracking ID
python3 workspace/skills/analytica-monitor/analytica_helper.py <tracking_id>
```

## Environment Variables
- `ANALYTICA_BASE` — Analytica API base URL
