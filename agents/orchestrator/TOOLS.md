# TOOLS.md — Orchestrator Agent

## Custom Skills (Workspace)

### gsheet-manager
Google Sheets read/write operations.
- `gsheets_helper.py` — Core GSheet connector (read rows, update cells)
- `update_excel.py` — Save agent pipeline results to the Google Sheet
- Usage: `python3 workspace/skills/gsheet-manager/update_excel.py '<json_string>'`

### pipeline-runner
Batch pipeline orchestration for processing multiple leads.
- `deep_research_batch.py` — Orchestrates the full multi-agent pipeline for batches
- `batch_runner.py` — Fetches un-crawled leads from the sheet
- Usage: `python3 workspace/skills/pipeline-runner/deep_research_batch.py --row <X>`
- Usage: `python3 workspace/skills/pipeline-runner/deep_research_batch.py <count>`
