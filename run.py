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
        "How satisfied are you with the quality of the product you received? (1-5): \n",
        "How would you rate your experience with our customer support team? (1-5): \n",
        "How likely are you to recommend our product/service to a friend or colleague? (1-5): \n"
]

    for question in questions:
        while True:  # Repeat until we get a valid response
            response = input(question)  
            try:
                validated_response = validate_response(response)  # Validate the input
                responses.append(validated_response)  # Append the validated response
                break  # Exit loop if response is valid
            except ValueError as e:
                print(e)  # Print error message and ask again


def validate_response(response):
    """
    Validate that the response is a number between 1 and 5.
    
    """
    try:
        response = int(response)
        
        # Check if the integer is between 1 and 5
        if response >= 1 and response <= 5:
            return response  # Return the valid integer response
        else:
            # Raise ValueError if the number is out of the valid range
            raise ValueError("Number must be between 1 and 5.")
    except ValueError as e:
        # Raise an error if conversion to integer fails or if out of range
        print(f"Invalid input: {e}. Please enter a number between 1 and 5.\n")
    
customer_responses = get_customer_answers()
print(f"Your responses are {customer_responses}")
    
    