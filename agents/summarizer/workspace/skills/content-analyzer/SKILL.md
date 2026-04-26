---
name: content-analyzer
description: Parse raw HTML/JSON scraped data into structured sections — contacts, technology, accreditation
tools:
  - shell
---

# Content Analyzer Skill

## Purpose
Takes raw scraped content and extracts structured data: contacts, NAAC info, course listings, technology markers.

## Usage
```bash
python3 workspace/skills/content-analyzer/content_parser.py '<raw_json>'
```
