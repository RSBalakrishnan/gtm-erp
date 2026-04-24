---
name: email-generator
description: Create Analytica tracking IDs and pixel URLs for lead tracking
tools:
  - shell
---

# Email Generator Skill

## Purpose
Creates unique Analytica tracking IDs for each lead, providing pixel URLs and redirect base URLs for email open and link click tracking.

## Usage
```bash
python3 workspace/skills/email-generator/analytica_helper.py
```

## Environment Variables
- `ANALYTICA_BASE` — Analytica API base URL
