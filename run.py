import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('customer_survey')

def get_customer_answers():
    """
    Get customer's review regarding customer support based on four questions.
    """

    print("Please rate your customer experience in the next four questions so as to help us improve our work.\n")
    print("Data must be a number from 1-5 based on the following:")
    print("""
    1 - Bad experience
    2 - Poor experience
    3 - Neutral experience
    4 - Good experience
    5 - Best experience
    """)

    responses = []

    questions = [
        "How would you rate your overall satisfaction with our service? (1-5): \n",
        "How satisfied are you with the quality of the product you received? (1-5):\n ",
        "How would you rate your experience with our customer support team? (1-5):\n ",
        "How likely are you to recommend our product/service to a friend or colleague? (1-5):\n "
    ]

    for question in questions:
        while True:
            try:
                response = int(input(question))
                if (1 <= response) and (response <= 5):
                    responses.append(response)
                    break  # Exit loop if response is valid
                else: # Raise ValueError if response is outside the expected range
                    raise ValueError("Data must be a number between 1 and 5.")
            except ValueError as e:
                # Print the error message
                print(e)
                print("Please provide a number betwwen 1 and 5.")

    print("Thank you for your feedback!")

get_customer_answers()
    
    