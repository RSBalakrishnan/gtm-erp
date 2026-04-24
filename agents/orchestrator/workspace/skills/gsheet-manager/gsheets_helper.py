#!/usr/bin/env python3
"""
GSheets Helper — Google Sheets connector for GTM V4 Multi-Agent System.
Provides read/write operations on the lead management Google Sheet.
"""
import gspread
import json
import os
import time
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load credentials from root .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', '.env')
if not os.path.exists(env_path):
    # Fallback: try /app/.env (Docker container path)
    env_path = '/app/.env'
load_dotenv(env_path)

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

# Cache
_client = None
_sheet = None
_last_fetch = 0
_cached_rows = None
CACHE_TTL = 30  # seconds

def _get_client():
    """Get authenticated gspread client using .env credentials."""
    global _client
    if _client:
        return _client

    creds_info = {
        "type": "service_account",
        "project_id": os.getenv("GCP_PROJECT_ID"),
        "private_key_id": os.getenv("GCP_PRIVATE_KEY_ID"),
        "private_key": os.getenv("GCP_PRIVATE_KEY", "").replace("\\n", "\n"),
        "client_email": os.getenv("GCP_CLIENT_EMAIL"),
        "client_id": os.getenv("GCP_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_info(creds_info, scopes=scopes)
    _client = gspread.authorize(credentials)
    return _client

def _get_sheet():
    """Get the worksheet object."""
    global _sheet
    if _sheet:
        return _sheet
    client = _get_client()
    _sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    return _sheet

class GSheetsHelper:
    def __init__(self):
        self.sheet = _get_sheet()

    def get_all_rows(self, force_refresh=False):
        global _last_fetch, _cached_rows
        now = time.time()
        if not force_refresh and _cached_rows and (now - _last_fetch) < CACHE_TTL:
            return _cached_rows
        _cached_rows = self.sheet.get_all_values()
        _last_fetch = now
        return _cached_rows

    def update_row(self, row_index, values):
        """Update a specific row (1-indexed)."""
        cell_range = f"A{row_index}:{chr(64 + len(values))}{row_index}"
        self.sheet.update(cell_range, [values])

    def get_headers(self):
        rows = self.get_all_rows()
        if len(rows) >= 3:
            return rows[2]  # Headers in row 3
        return []

if __name__ == "__main__":
    helper = GSheetsHelper()
    rows = helper.get_all_rows()
    print(f"Total rows: {len(rows)}")
    if len(rows) >= 3:
        print(f"Headers: {rows[2]}")
