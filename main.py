
import survey_module
import analysis_module

def main():
    """
    Run the appropriate module based on user input.
    """
    user_role = input("Are you a customer or the owner? (Enter 'customer' or 'owner'): ").strip().lower()
    
    if user_role == 'customer':
        customer_responses = survey_module.get_customer_answers()
        survey_module.update_survey_worksheet(customer_responses)
    elif user_role == 'owner':
        averages = analysis_module.calculate_averages()
        analysis_module.update_analysis_worksheet(averages)
        analysis_module.print_survey_averages()
    else:
        print("Invalid role. Please enter 'customer' or 'owner'.")

    main()