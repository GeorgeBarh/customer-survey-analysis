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
            last_customer_id = 1  # Start with 0 if no data
    except Exception as e:
        print(f"Error retrieving last customer ID: {e}")
        last_customer_id = 1
    return last_customer_id
    
def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def main():
    """
    Run all program functions
    """
customer_responses = get_customer_answers()
print(f"Your responses are {customer_responses}")
update_survey_worksheet(customer_responses)

# Survey Analysis

def get_survey_data():
    """
    Retrieve all survey responses from the 'survey' worksheet.
    """
    survey_worksheet = SHEET.worksheet("survey")
    data = survey_worksheet.get_all_values()  
    return data[1:]  # Exclude the header row

def calculate_averages():
    """
    Calculate the average rating for each survey question using basic Python.
    """
    data = get_survey_data()
    
    # Initialize variables to store the total sums and the count for each question
    total_sums = [0, 0, 0, 0]  # There are 4 questions
    count = len(data)  # Number of responses (rows)

    # Loop through each row of responses (excluding Customer_id column)
    for row in data:
        total_sums[0] += int(row[1])  # Overall satisfaction
        total_sums[1] += int(row[2])  # Product quality
        total_sums[2] += int(row[3])  # Customer support
        total_sums[3] += int(row[4])  # Likelihood to recommend

    # Calculate the averages by dividing each sum by the total number of responses
    averages = [total / count for total in total_sums]

    return averages

def update_analysis_worksheet(data):
    """
    Update the analysis worksheet with the average of customer's responses
    """
    print("Updating analysis worksheet...\n")
    analysis_worksheet = SHEET.worksheet("analysis") 
    analysis_worksheet.append_row(data)
    print("Survey worksheet updated successfully.\n")

main()