

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