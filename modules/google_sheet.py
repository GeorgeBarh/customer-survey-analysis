import gspread
from google.oauth2.service_account import Credentials


class GoogleSheet:
    """
    Handles Google Sheets API authorization and worksheet access.
    """
    def __init__(self, sheet_name):
        # Initialize Google Sheets API
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file('creds.json')
        scoped_creds = creds.with_scopes(scope)
        gspread_client = gspread.authorize(scoped_creds)
        self.sheet = gspread_client.open(sheet_name)

    def get_worksheet(self, worksheet_name):
        """
        returns the worksheet object by name.
        """
        return self.sheet.worksheet(worksheet_name)