import json
import os

def json_to_toon(data, title="Data"):
    """
    Convert a list of dictionaries to TOON (Token-Oriented Object Notation).
    Reduces token overhead by 30-60%.
    Format: [TITLE] count
    Header1 | Header2 | Header3
    V1 | V2 | V3
    """
    if not data:
        return f"[{title}] 0\n(Empty set)"
    
    if not isinstance(data, list):
        # Fallback to simple indented representation for non-list objects
        return f"[{title}]\n" + json.dumps(data, indent=2).replace('"', '').replace('{', '').replace('}', '').strip()

    # Get all unique keys from all items to ensure we don't miss sparse data
    keys = []
    for item in data:
        for k in item.keys():
            if k not in keys:
                keys.append(k)

    header_str = " | ".join(keys)
    rows = []
    for item in data:
        # Use '-' for missing values to keep table structure intact
        row = " | ".join(str(item.get(k, "-")).replace("|", "\\|").replace("\n", " ") for k in keys)
        rows.append(row)
    
    return f"[{title}] {len(data)}\n{header_str}\n" + "\n".join(rows)

def toon_to_json(toon_str):
    """
    Parse a TOON string back into a list of JSON objects.
    """
    lines = [l.strip() for l in toon_str.strip().split('\n') if l.strip()]
    if len(lines) < 2:
        return []

    # First line is metadata [TITLE] COUNT
    # Second line is headers
    headers = [h.strip() for h in lines[1].split('|')]
    
    results = []
    for line in lines[2:]:
        values = [v.strip() for v in line.split('|')]
        # Match values to headers
        obj = {}
        for i, header in enumerate(headers):
            val = values[i] if i < len(values) else "-"
            # Basic type inference
            if val.lower() == "true": val = True
            elif val.lower() == "false": val = False
            elif val.isdigit(): val = int(val)
            obj[header] = val
        results.append(obj)
        
    return results

if __name__ == "__main__":
    # Quick test
    sample = [
        {"College": "Harvard", "Website": "harvard.edu", "Leads": 5},
        {"College": "Stanford", "Website": "stanford.edu", "Leads": 3}
    ]
    toon = json_to_toon(sample, "College Leads")
    print(toon)
    print("\nParsed back:")
    print(json.dumps(toon_to_json(toon), indent=2))
