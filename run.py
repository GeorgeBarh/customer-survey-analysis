import gspread
from google.oauth2.service_account import Credentials

# initialize Google Sheets API
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file('creds.json')
scoped_creds = creds.with_scopes(scope)
gspread_client = gspread.authorize(scoped_creds)
sheet = gspread_client.open('customer_survey')

def get_customer_answers():
    """
    collect customer survey responses and assign a new customer id.
    """
    print("\nPlease rate your customer experience in the next four questions.\n")
    print("Data must be a number from 1-5 based on the following:")
    print("""
    1 - Bad experience
    2 - Poor experience
    3 - Neutral experience
    4 - Good experience
    5 - Best experience
          """)

    responses = [] 
    last_customer_id = get_last_customer_id()  # Get the last customer id
    current_customer_id = last_customer_id + 1  # Increment for the new customer

    questions = [
        "How would you rate your overall satisfaction with our service? (1-5): \n",
        "How satisfied are you with the quality of the product you received? (1-5): \n",
        "How would you rate your experience with our customer support team? (1-5): \n",
        "How likely are you to recommend our product/service to a friend or colleague? (1-5): \n"
    ]

    responses.append(current_customer_id)  # add the customer id

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
    retrieve the last customer id from the survey worksheet.
    """
    try:
        survey_worksheet = sheet.worksheet("survey") 
        data = survey_worksheet.get_all_values()
        if len(data) > 1:
            last_row = data[-1]
            last_customer_id = int(last_row[0])  # Customer id is in the first column
        else:
            last_customer_id = 1  # Start with 1 if no data
    except Exception as e:
        print(f"Error retrieving last customer ID: {e}")
        last_customer_id = 1
    return last_customer_id
    
def update_survey_worksheet(data):
    """
    update survey worksheet, add new row with the list data provided.
    """
    print("Updating survey worksheet...\n")
    survey_worksheet = sheet.worksheet("survey")
    survey_worksheet.append_row(data)
    print("Survey worksheet updated succesfully.\n")  # Slight typo here

def get_survey_data():
    """
    retrieve all survey responses from the 'survey' worksheet.
    """
    survey_worksheet = sheet.worksheet("survey")
    data = survey_worksheet.get_all_values()  
    return data[1:]  # Exclude the header row

def calculate_averages():
    """
    calculate the average rating for each survey question.
    """
    data = get_survey_data()
    
    total_sums = [0, 0, 0, 0]  # There are 4 questions
    count = len(data)  # Number of responses (rows)

    for row in data:
        total_sums[0] += int(row[1])  # Overall satisfaction
        total_sums[1] += int(row[2])  # Product quality
        total_sums[2] += int(row[3])  # Customer support
        total_sums[3] += int(row[4])  # Recomdation  # Typo here

    averages = [round(total / count) for total in total_sums]
    return averages

def update_analysis_worksheet(averages):
    """
    update the 'analysis' worksheet with the latest survey averages.
    """
    print("Updating analysis worksheet with averages...\n")
    
    analysis_worksheet = sheet.worksheet("analysis")
    survey_data = get_survey_data()
    number_of_responses = len(survey_data)  # Total number of survey responses
    
    data = [
        number_of_responses,  # Number of responses
        averages[0],  # Overall satisfaction
        averages[1],  # Product quality
        averages[2],  # Customer support
        averages[3],  # Recommendation
    ]
    
    analysis_worksheet.append_row(data)
    print("Analysis worksheet updated succesfully.\n")  # Typo here

def print_survey_averages():
    """
    retrieve and print survey averages from the 'analysis' worksheet with descriptive messages.
    """
    analysis_worksheet = sheet.worksheet("analysis")
    
    # Get all rows of data from the 'analysis' worksheet
    rows = analysis_worksheet.get_all_values()
    
    # Check if there are at least two rows (headers and at least one data row)
    if len(rows) < 2:
        print("No data available in the analysis worksheet.")
        return
    
    # Extract headers and the latest data row
    headers = rows[0]  # Headers are in the first row
    latest_data = rows[-1]  # Latest data should be in the last row

    # Print the survey averages with messages
    print("\nSurvey Averages:")
    for header, value in zip(headers, latest_data):
        rating = int(value)
        message = get_rating_message(rating)
        print(f"{header} {value} ({message})\n")

def get_rating_message(rating):
    if rating == 1:
        return "Very Poor Experiance"  # Typo here
    elif rating == 2:
        return "Poor Experiance"  # Typo here
    elif rating == 3:
        return "Okay/Neutral Experiance"  # Typo here
    elif rating == 4:
        return "Good Experiance"  # Typo here
    elif rating == 5:
        return "Excellent Experiance"  # Typo here
    else:
        return("Responses in total")

def main():
    """
    Run all program functions.
    """
    customer_responses = get_customer_answers()
    print(f"Your responses are {customer_responses}")
    update_survey_worksheet(customer_responses)
    
    averages = calculate_averages()
    update_analysis_worksheet(averages)
    
    print_survey_averages()

main()