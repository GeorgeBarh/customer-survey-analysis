import gspread
from google.oauth2.service_account import Credentials

# initialize Google Sheets API
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
    collect customer survey responses and assign a new customer ID.
    """
    print("Please rate your customer experience in the next four questions.\n")
    print("Data must be a number from 1-5 based on the following:")
    print("""1 - Bad experience
    2 - Poor experience
    3 - Neutral experience
    4 - Good experience
    5 - Best experience""")

    responses = [] 
    last_customer_id = get_last_customer_id()  # get the last customer ID
    current_customer_id = last_customer_id + 1  # increment for the new customer

    questions = [
        "How would you rate your overall satisfaction with our service? (1-5): \n",
        "How satisfied are you with the quality of the product you received? (1-5): \n",
        "How would you rate your experience with our customer support team? (1-5): \n",
        "How likely are you to recommend our product/service to a friend or colleague? (1-5): \n"
    ]

    responses.append(current_customer_id)  # add the customer ID

    for question in questions:
        while True:
            response = input(question)  
            try:
                validated_response = validate_response(response)  # validate input
                responses.append(validated_response)  # add validated response
                break
            except ValueError as e:
                print(e)  # print error message

    return responses

def validate_response(response):
    """
    ensure the response is a number between 1 and 5.
    """
    try:
        response = int(response)
        if 1 <= response <= 5:
            return response
        else:
            raise ValueError("Number must be between 1 and 5.")
    except ValueError:
        raise ValueError("Invalid input. Please enter a number between 1 and 5.")

def get_last_customer_id():
    """
    retrieve the last customer ID from the survey worksheet.
    """
    try:
        survey_worksheet = SHEET.worksheet("survey") 
        data = survey_worksheet.get_all_values()
        if len(data) > 1:
            last_row = data[-1]
            last_customer_id = int(last_row[0])  # customer id is in the first column
        else:
            last_customer_id = 1  # start with 1 if no data
    except Exception as e:
        print(f"Error retrieving last customer ID: {e}")
        last_customer_id = 1
    return last_customer_id
    
def update_survey_worksheet(data):
    """
    update survey worksheet, add new row with the list data provided.
    """
    print("Updating survey worksheet...\n")
    survey_worksheet = SHEET.worksheet("survey")
    survey_worksheet.append_row(data)
    print("Survey worksheet updated successfully.\n")

def get_survey_data():
    """
    retrieve all survey responses from the 'survey' worksheet.
    """
    survey_worksheet = SHEET.worksheet("survey")
    data = survey_worksheet.get_all_values()  
    return data[1:]  # exclude the header row

def calculate_averages():
    """
    calculate the average rating for each survey question.
    """
    data = get_survey_data()
    
    total_sums = [0, 0, 0, 0]  # there are 4 questions
    count = len(data)  # number of responses (rows)

    for row in data:
        total_sums[0] += int(row[1])  # overall satisfaction
        total_sums[1] += int(row[2])  # product quality
        total_sums[2] += int(row[3])  # customer support
        total_sums[3] += int(row[4])  # Recomendation

    averages = [round(total / count) for total in total_sums]
    return averages

def update_analysis_worksheet(averages):
    """
    update the 'analysis' worksheet with the latest survey averages.
    """
    print("Updating analysis worksheet with averages...\n")
    
    analysis_worksheet = SHEET.worksheet("analysis")
    survey_data = get_survey_data()
    number_of_responses = len(survey_data)  # total number of survey responses
    
    data = [
        number_of_responses,  # number of responses
        averages[0],  # overall satisfaction
        averages[1],  # product quality
        averages[2],  # customer support
        averages[3],  # recommendation
    ]
    
    analysis_worksheet.append_row(data)
    print("Analysis worksheet updated successfully.\n")

def print_survey_averages():
    """
    Retrieve and print survey averages from the 'analysis' worksheet.
    """
    analysis_worksheet = SHEET.worksheet("analysis")
    headers = analysis_worksheet.row_values(1)  # get headers
    latest_data = analysis_worksheet.row_values(analysis_worksheet.row_count)  # Get latest data
    
    print("\nSurvey Averages:")
    for header, value in zip(headers, latest_data):
        print(f"{header}: {value}")

def main():
    """
    run all program functions.
    """
    customer_responses = get_customer_answers()
    print(f"Your responses are {customer_responses}")
    update_survey_worksheet(customer_responses)
    
    averages = calculate_averages()
    update_analysis_worksheet(averages)
    
    print_survey_averages()

main()