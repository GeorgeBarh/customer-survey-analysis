import gspread
from google.oauth2.service_account import Credentials

# Initialize Google Sheets API
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
    Collect customer survey responses and assign a new customer ID.
    """
    print("Please rate your customer experience in the next four questions.\n")
    print("Data must be a number from 1-5 based on the following:")
    print("""
    1 - Bad experience
    2 - Poor experience
    3 - Neutral experience
    4 - Good experience
    5 - Best experience
    """)

    responses = [] 
    last_customer_id = get_last_customer_id()  # Get the last customer ID
    current_customer_id = last_customer_id + 1  # Increment for the new customer

    questions = [
        "How would you rate your overall satisfaction with our service? (1-5): \n",
        "How satisfied are you with the quality of the product you received? (1-5): \n",
        "How would you rate your experience with our customer support team? (1-5): \n",
        "How likely are you to recommend our product/service to a friend or colleague? (1-5): \n"
    ]

    responses.append(current_customer_id)  # Add the customer ID

    for question in questions:
        while True:
            response = input(question)  
            try:
                validated_response = validate_response(response)  # Validate input
                responses.append(validated_response)  # Add validated response
                break
            except ValueError as e:
                print(e)  # Print error message

    return responses

def validate_response(response):
    """
    Ensure the response is a number between 1 and 5.
    """
    try:
        response = int(response)
        if 1 <= response <= 5:
            return response
        else:
            raise ValueError("Number must be between 1 and 5.")
    except ValueError as e:
        raise ValueError(f"Invalid input: {e}. Please enter a number between 1 and 5.")

def get_last_customer_id():
    """
    Retrieve the last customer ID from the survey worksheet.
    """
    try:
        survey_worksheet = SHEET.worksheet("survey") 
        data = survey_worksheet.get_all_values()
        if len(data) > 1:
            last_row = data[-1]
            last_customer_id = int(last_row[0])  # Customer ID is in the first column
        else:
            last_customer_id = 0  # Start with 0 if no data
    except Exception as e:
        print(f"Error retrieving last customer ID: {e}")
        last_customer_id = 0
    return last_customer_id
    
def update_survey_worksheet(data):
    """
    Update the survey worksheet with the new responses.
    """
    print("Updating survey worksheet...\n")
    survey_worksheet = SHEET.worksheet("survey") 
    survey_worksheet.append_row(data)
    print("Survey worksheet updated successfully.\n")

# Collect responses and update the worksheet
customer_responses = get_customer_answers()
print(f"Your responses are {customer_responses}")
update_survey_worksheet(customer_responses)