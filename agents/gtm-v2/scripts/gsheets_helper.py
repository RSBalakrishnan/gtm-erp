import os
import socket
from dotenv import load_dotenv

# Load credentials from .env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(env_path)

# Set a long timeout (300 seconds) for all network sockets to handle large Google Sheets fetches
socket.setdefaulttimeout(300)

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SERVICE_ACCOUNT_FILENAME = os.getenv("SERVICE_ACCOUNT_FILE")
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), SERVICE_ACCOUNT_FILENAME) if SERVICE_ACCOUNT_FILENAME else None
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

class GSheetsHelper:
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        self.creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=self.scopes
        )
        self.service = build("sheets", "v4", credentials=self.creds)
        self._cached_rows = None

    def get_all_rows(self, range_name="A1:ZZ60000", force_refresh=False):
        """Fetch rows from the sheet. Implements caching by default."""
        if self._cached_rows is not None and not force_refresh:
            return self._cached_rows
            
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=range_name
            ).execute()
            self._cached_rows = result.get('values', [])
            return self._cached_rows
        except HttpError as err:
            print(f"Error fetching rows: {err}")
            return []

    def update_row(self, row_index, values, sheet_name=None):
        """Update a specific row (1-indexed)."""
        sheet_prefix = f"{sheet_name}!" if sheet_name else ""
        range_name = f"{sheet_prefix}A{row_index}"
        
        body = {"values": [values]}
        try:
            # Clean data: Replace NaN/None with empty strings
            clean_values = [str(v) if v is not None and not (isinstance(v, float) and v != v) else "" for v in values]
            body["values"] = [clean_values]
            
            self.service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_name,
                valueInputOption="RAW",
                body=body
            ).execute()
            return True
        except HttpError as err:
            print(f"Error updating row {row_index}: {err}")
            return False

    def find_row_index(self, search_val, col_index, start_row=5):
        """Search for a value in a specific column and return 1-indexed row number."""
        rows = self.get_all_rows()
        for i, row in enumerate(rows):
            if i < start_row - 1: continue
            if len(row) > col_index and row[col_index].strip().lower() == search_val.strip().lower():
                return i + 1
        return None
    def append_row(self, values, sheet_name=None):
        """Append a row to the end of the sheet."""
        sheet_prefix = f"{sheet_name}!" if sheet_name else "A:ZZ"
        try:
            clean_values = [str(v) if v is not None and not (isinstance(v, float) and v != v) else "" for v in values]
            body = {"values": [clean_values]}
            self.service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=sheet_prefix,
                valueInputOption="RAW",
                body=body
            ).execute()
            return True
        except HttpError as err:
            print(f"Error appending row: {err}")
            return False
