#!/usr/bin/env python3
"""
Scoring Engine — Lead scoring based on digital maturity, accreditation, and contacts.
Part of the lead-scorer skill for the Summarizer agent.
"""
import json
import sys


NAAC_SCORES = {
    "A++": 30, "A+": 25, "A": 20,
    "B++": 15, "B+": 10, "B": 5,
    None: 0, "": 0
}


def calculate_score(analysis):
    """
    Calculate lead score (0-100) based on:
    - NAAC grade (0-30 pts)
    - Digital gaps count (0-30 pts, more gaps = higher score)
    - Contact availability (0-20 pts)
    - Course count (0-20 pts)
    """
    score = 0
    reasons = []

    # NAAC grade
    naac = analysis.get("naac_grade", "")
    naac_pts = NAAC_SCORES.get(naac, 0)
    score += naac_pts
    if naac:
        reasons.append(f"NAAC {naac} (+{naac_pts})")

    # Digital gaps (more gaps = more opportunity)
    gaps = analysis.get("digital_gaps", [])
    gap_pts = min(len(gaps) * 6, 30)
    score += gap_pts
    if gaps:
        reasons.append(f"{len(gaps)} digital gaps identified (+{gap_pts})")

    # Contact availability
    contacts = analysis.get("contacts", {})
    emails = contacts.get("emails", [])
    phones = contacts.get("phones", [])
    linkedin = contacts.get("linkedin_profiles", [])
    contact_pts = min(len(emails) * 5 + len(phones) * 3 + len(linkedin) * 7, 20)
    score += contact_pts
    if emails or phones:
        reasons.append(f"{len(emails)} emails, {len(phones)} phones (+{contact_pts})")

    # Course count
    courses = analysis.get("course_count", 0)
    course_pts = min(courses, 20)
    score += course_pts
    if courses:
        reasons.append(f"{courses} courses (+{course_pts})")

    # Determine tier
    if score >= 80:
        tier = "🟢 HOT"
    elif score >= 50:
        tier = "🟡 WARM"
    else:
        tier = "🔴 COLD"

    return {
        "score": score,
        "tier": tier,
        "justification": f"{tier} ({score}/100) — {'; '.join(reasons)}",
        "breakdown": {
            "naac": naac_pts,
            "digital_gaps": gap_pts,
            "contacts": contact_pts,
            "courses": course_pts
        }
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scoring_engine.py '<analysis_json>'")
        sys.exit(1)

    analysis = json.loads(sys.argv[1])
    result = calculate_score(analysis)
    print(json.dumps(result, indent=2))
