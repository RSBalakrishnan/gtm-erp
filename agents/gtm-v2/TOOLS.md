# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

### Custom Scripts (Lead Management)
All scripts are located in `scripts/` and should be run with `python3 scripts/<name>.py`.

- **`analytica_helper.py`**: Wrapper for the Analytica tracking API.
  - Usage: `from analytica_helper import create_tracking_id, get_email_status, get_link_analytics, get_journey`
  - `create_tracking_id(["url1", "url2"])` → Returns `{trackingId, pixelUrl, redirectUrlBase, links}`
  - `get_email_status("tracking_id")` → Returns email open count
  - `get_link_analytics("tracking_id")` → Returns link click data
  - `get_journey("tracking_id")` → Returns full event timeline
- **`update_excel.py`**: Saves agent research directly to the Google Sheet. 
  - Usage: `python3 scripts/update_excel.py '<json_string>'`.
  - Maps `college_name`, `website`, and `website_extraction_research`, `Tracking ID`, `Pixel URL`.
- **`batch_runner.py`**: Pulls un-crawled leads from the sheet.
  - Usage: `python3 -c "from scripts.batch_runner import get_next_batch; print(get_next_batch(5))"`.
- **`status_report.py`**: Returns JSON summary of lead statuses including real Analytica stats.
  - Usage: `python3 scripts/status_report.py`.
- **`reset_leads.py`**: Resets lead status (`Crawled: FALSE`) and clears research.
  - Usage: `python3 scripts/reset_leads.py`.
- **`update_headers.py`**: Renames and consolidates GSheet columns.
  - Usage: `python3 scripts/update_headers.py`.
- **`deep_research_batch.py`**: V3: Cache-first scraping + Analytica tracking + multi-agent pipeline.
  - Usage: `python3 scripts/deep_research_batch.py`.
- **`email_sender.py`**: Core SMTP sender with tracking pixel injection.
  - Usage: `python3 scripts/email_sender.py --test <email>`.
- **`process_outreach.py`**: Batch processor that sends drafted emails from the Google Sheet.
  - Usage: `python3 scripts/process_outreach.py --row <X> --limit <N>`.


## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
