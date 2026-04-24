---
name: email-sender
description: Send tracked HTML emails via SMTP with invisible tracking pixel injection
tools:
  - shell
---

# Email Sender Skill

## Purpose
Sends outreach emails via Gmail SMTP with HTML tracking pixel injection for open tracking.

## Scripts
- `email_sender.py` — Core SMTP sender with tracking pixel injection
- `process_outreach.py` — Batch processor that sends drafted emails from Google Sheet

## Usage
```bash
# Test email
python3 workspace/skills/email-sender/email_sender.py --test <email>

# Send outreach for a specific row
python3 workspace/skills/email-sender/process_outreach.py --row <X>

# Batch send (limit N)
python3 workspace/skills/email-sender/process_outreach.py --limit <N>
```

## Environment Variables
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM`
