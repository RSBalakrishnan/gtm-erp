# GTM Sales Orchestration Workflow

## Stage 1: Website Analysis
- **Goal**: Extract relevant contact and contextual data.
- **Process**: Visit the URL and analyze Home, About, Contact, Admissions, and Leadership pages.
- **Extraction**: Extract Name, Type, Location, Emails, Phones, Leadership, and LinkedIn links.

## Stage 2: Lead Enrichment
- **Goal**: Classify the college and identify the problem.
- **Process**: Categorize by type (Engg/Arts/etc.) and identify the Target Persona (e.g., Admission Head).

## Stage 2.5: Tracking Setup (V3)
- **Goal**: Create a unique Analytica tracking ID for this lead.
- **Process**: Call `POST /track/id` with CTA URLs → receive trackingId, pixelUrl, redirectUrlBase.
- **Output**: Pass tracking assets to Agent 2 for email injection.

## Stage 3: Multi-Stage Email Generation
- **Email 1 (Intro)**: Personalized value prop referencing college type and social proof.
- **Email 2 (Follow-up)**: Triggered by opened-no-reply. Feature update/local case study.
- **Email 3 (Nurture)**: Soft reminder for unengaged leads.

## Stage 4: Decision & Tracking (MANDATORY)
- **Engine**: Based on the Decision Engine rules, update the tracking JSON for every interaction.
- **Next Actions**: Proactively suggest next steps for "HOT" leads (demo booked/positive reply).

## Stage 5: LinkedIn Outreach (OPTIONAL)
- If LinkedIn profile is found, generate a conversational DM to the target persona.
