#!/usr/bin/env python3
"""
Website Analyzer — DNS reachability check and technology detection.
Part of the website-analyzer skill for the Researcher agent.
"""
import socket
import json
import sys
import requests
from urllib.parse import urlparse


def is_reachable(url):
    """Check if a website is reachable via DNS resolution."""
    if not url or url.strip().lower() == "n/a":
        return False
    try:
        clean_url = url.strip()
        if not clean_url.startswith('http'):
            clean_url = 'http://' + clean_url
        hostname = urlparse(clean_url).hostname
        if not hostname:
            return False
        socket.gethostbyname(hostname)
        return True
    except (socket.gaierror, socket.timeout):
        return False


def detect_technology(url):
    """Detect basic technology markers from HTTP headers and content."""
    result = {
        "reachable": False,
        "ssl": False,
        "server": "Unknown",
        "framework": "Unknown",
        "mobile_responsive": "Unknown"
    }

    try:
        clean_url = url.strip()
        if not clean_url.startswith('http'):
            clean_url = 'https://' + clean_url

        result["ssl"] = clean_url.startswith('https')
        result["reachable"] = is_reachable(url)

        if result["reachable"]:
            resp = requests.head(clean_url, timeout=10, allow_redirects=True)
            result["server"] = resp.headers.get("Server", "Unknown")
            powered_by = resp.headers.get("X-Powered-By", "")
            if powered_by:
                result["framework"] = powered_by

    except Exception as e:
        result["error"] = str(e)

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyzer.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    analysis = detect_technology(url)
    print(json.dumps(analysis, indent=2))
