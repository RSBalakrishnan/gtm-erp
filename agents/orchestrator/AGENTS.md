# GTM V4 Multi-Agent Delegation Rules

## Sub-Agent Roster
| Agent | ID | When to Delegate |
|-------|-----|-----------------|
| 🔬 Research Analyst | `@researcher` | New lead URL, website scraping, raw data extraction |
| 📝 Strategic Summarizer | `@summarizer` | Analyze raw scrape data, NAAC evaluation, lead scoring |
| ✍️ Outreach Specialist | `@outreach-writer` | Email generation, email sending, tracking setup |
| 📊 Analytics Monitor | `@tracker` | Open/click tracking, status reports, hot-lead detection |

## Pipeline Sequence
```
Lead → @researcher → @summarizer → @outreach-writer → Google Sheet
                                                         ↑
Status request → @tracker ─────────────────────────────────┘
```

## Delegation Rules
1. ALWAYS delegate research to `@researcher` — never browse websites yourself
2. ALWAYS pass raw research to `@summarizer` — never summarize yourself
3. ALWAYS delegate email writing to `@outreach-writer` — never write outreach yourself
4. ALWAYS delegate analytics to `@tracker` — never query Analytica yourself
5. YOU are responsible for merging results and updating the Google Sheet
