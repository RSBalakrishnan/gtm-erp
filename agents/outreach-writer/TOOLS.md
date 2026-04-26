# TOOLS.md — Outreach Writer Agent

## Custom Skills

### email-generator
Creates Analytica tracking IDs and generates tracked email templates.
- `analytica_helper.py` — `create_tracking_id(urls)` → Returns trackingId, pixelUrl, redirectUrlBase
- Usage: `python3 workspace/skills/email-generator/analytica_helper.py`

### email-sender
Sends tracked HTML emails via SMTP with pixel injection.
- `email_sender.py` — SMTP sender: `send_email(to, subject, body, pixel_url, tracking_id)`
- `process_outreach.py` — Batch processor for sending drafted emails from the sheet
- Usage: `python3 workspace/skills/email-sender/email_sender.py --test <email>`
- Usage: `python3 workspace/skills/email-sender/process_outreach.py --row <X> --limit <N>`
