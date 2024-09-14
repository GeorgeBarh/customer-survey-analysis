import gspread
from google.oauth2.service_account import Credentials

class GoogleSheet:
    """
    Handles Google Sheets API authorization and worksheet access.
    Manages authentication and provides methods to access specific worksheets.
    """
    def __init__(self, sheet_name):
        """
        Initialize Google Sheets API with credentials and scope.
        Authorizes the client and opens the specified Google Sheets document.
        """
        # Define the scope of access for the Google Sheets API
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        # Load credentials from the service account file
        creds = Credentials.from_service_account_file('creds.json')  # ! PROVIDE THE CORRECT PATH TO YOUR 'creds.json' FILE
        # Apply the defined scope to the credentials
        scoped_creds = creds.with_scopes(scope)
        # Authorize the gspread client with the scoped credentials
        gspread_client = gspread.authorize(scoped_creds)
        # Open the specified Google Sheets document
        self.sheet = gspread_client.open(sheet_name)  # ! MAKE SURE 'sheet_name' MATCHES THE NAME OF YOUR GOOGLE SHEETS DOCUMENT

    def get_worksheet(self, worksheet_name):
        """
        Retrieve the worksheet object by its name.
        Provides access to perform operations on the specified worksheet.
        """
        return self.sheet.worksheet(worksheet_name)  # Return the worksheet object