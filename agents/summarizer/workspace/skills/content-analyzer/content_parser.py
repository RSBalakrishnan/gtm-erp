#!/usr/bin/env python3
"""
Content Parser — Extracts structured data from raw scraped content.
Part of the content-analyzer skill for the Summarizer agent.
"""
import re
import json
import sys


def extract_emails(text):
    """Extract email addresses from text."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return list(set(re.findall(pattern, text)))


def extract_phones(text):
    """Extract Indian phone numbers from text."""
    patterns = [
        r'\+91[\s-]?\d{5}[\s-]?\d{5}',
        r'0\d{2,4}[\s-]?\d{6,8}',
        r'\d{10}',
    ]
    phones = []
    for pattern in patterns:
        phones.extend(re.findall(pattern, text))
    return list(set(phones))


def extract_naac_info(text):
    """Extract NAAC accreditation details."""
    naac_patterns = [
        r'NAAC\s*(?:accredited|grade|graded)?\s*[:\-]?\s*["\']?([A-B]\+{0,2})',
        r'Grade\s*[:\-]?\s*["\']?([A-B]\+{0,2})',
    ]
    for pattern in naac_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_linkedin(text):
    """Extract LinkedIn profile URLs."""
    pattern = r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_%]+'
    return list(set(re.findall(pattern, text)))


def parse_content(raw_data):
    """Parse raw scraped data into structured sections."""
    if isinstance(raw_data, str):
        try:
            raw_data = json.loads(raw_data)
        except json.JSONDecodeError:
            raw_data = {"raw_content": raw_data}

    # Combine all text content
    all_text = ""
    if isinstance(raw_data, dict):
        all_text = json.dumps(raw_data)
    else:
        all_text = str(raw_data)

    result = {
        "contacts": {
            "emails": extract_emails(all_text),
            "phones": extract_phones(all_text),
            "linkedin_profiles": extract_linkedin(all_text),
        },
        "naac_grade": extract_naac_info(all_text),
        "content_length": len(all_text),
    }

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 content_parser.py '<raw_json>'")
        sys.exit(1)

    result = parse_content(sys.argv[1])
    print(json.dumps(result, indent=2))
