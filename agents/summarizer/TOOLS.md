# TOOLS.md — Summarizer Agent

## Custom Skills

### content-analyzer
Parses raw HTML/JSON from scraper into structured sections.
- `content_parser.py` — Extracts contacts, technology markers, accreditation data
- Usage: `python3 workspace/skills/content-analyzer/content_parser.py '<raw_json>'`

### lead-scorer
Calculates lead scores based on configurable criteria.
- `scoring_engine.py` — Scoring rubric: website quality + course count + digital maturity + NAAC grade
- Usage: `python3 workspace/skills/lead-scorer/scoring_engine.py '<analysis_json>'`
