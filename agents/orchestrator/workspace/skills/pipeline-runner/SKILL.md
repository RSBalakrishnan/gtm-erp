---
name: pipeline-runner
description: Orchestrates the multi-agent batch research pipeline — scrape, summarize, outreach for multiple leads
tools:
  - shell
---

# Pipeline Runner Skill

## Purpose
Manages batch processing of leads through the multi-agent pipeline:
Lead → Researcher → Summarizer → Outreach Writer → Google Sheet

## Scripts
- `deep_research_batch.py` — Main pipeline: invokes agents by ID for each lead
- `batch_runner.py` — Fetches un-crawled leads from Google Sheet

## Usage
```bash
# Process a specific row
python3 workspace/skills/pipeline-runner/deep_research_batch.py --row 5

# Process next N leads
python3 workspace/skills/pipeline-runner/deep_research_batch.py 10

# Start from a specific row
python3 workspace/skills/pipeline-runner/deep_research_batch.py 10 --start 50
```
