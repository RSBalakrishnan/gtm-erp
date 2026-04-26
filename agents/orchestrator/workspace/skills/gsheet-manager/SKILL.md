---
name: gsheet-manager
description: Read/write operations on the GTM Google Sheet — the single source of truth for all lead data
tools:
  - shell
---

# GSheet Manager Skill

## Purpose
Provides Google Sheets integration for reading leads, updating research results, and managing the pipeline state.

## Scripts
- `gsheets_helper.py` — Core connector: `get_all_rows()`, `update_row()`, `get_headers()`
- `update_excel.py` — Saves agent pipeline JSON results to the sheet

## Usage
```bash
# Update a lead in the sheet
python3 workspace/skills/gsheet-manager/update_excel.py '<json_string>'

# Or from a temp file
python3 workspace/skills/gsheet-manager/update_excel.py temp_result.json
```

## Environment Variables Required
- `SPREADSHEET_ID` — Google Sheet ID
- `GCP_CLIENT_EMAIL` — Service account email
- `GCP_PRIVATE_KEY` — Service account private key
