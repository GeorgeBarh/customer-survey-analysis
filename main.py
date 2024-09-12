

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
    update_survey_worksheet(customer_responses)
    
    averages = calculate_averages()
    update_analysis_worksheet(averages)
    
    print_survey_averages()

main()