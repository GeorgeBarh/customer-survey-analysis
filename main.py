import modules.google_sheet as gs
import modules.survey_module as sm
import modules.analysis_module as am

def handle_user_role(user_role):
    """
    Handle the actions based on user role input.
    """
    try:
        if user_role == 'customer':
            try:
                customer_responses = survey_module.get_customer_answers()
                survey_module.update_survey_worksheet(customer_responses)
            except Exception as e:
                print(f"An error occurred while processing customer responses: {e}")

        elif user_role == 'owner':
            try:
                averages = analysis_module.calculate_averages()
                analysis_module.update_analysis_worksheet(averages)
                analysis_module.print_survey_averages()
            except Exception as e:
                print(f"An error occurred while processing survey analysis: {e}")

        else:
            print("Invalid role. Please enter 'customer' or 'owner'.")
            # Skip the continuation prompt and loop back to role input
            return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

    return True

def get_user_continue_response():
    """
    Ask the user if they want to perform another action.
    """
    while True:
        try:
            answer = input("Do you want to perform another action? (yes/no): ").strip().lower()
            if answer in ['yes', 'no']:
                return answer
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        except Exception as e:
            print(f"An error occurred while processing your input: {e}")

def main():
    """
    Run the appropriate module based on user input.
    """
    while True:
        user_role = input("Are you a customer or the owner? (Enter 'customer' or 'owner'): ").strip().lower()
        if handle_user_role(user_role):
            continue_prompt = get_user_continue_response()
            if continue_prompt != 'yes':
                print("Exiting the program.")
                break

main()