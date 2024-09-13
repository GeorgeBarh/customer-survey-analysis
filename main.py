import modules.google_sheet as gs
import modules.survey_module as sm
import modules.analysis_module as am

def validate_password():
    """Verify the password for accessing the owner functionalities."""
    try:
        from password import PASSWORD
    except ImportError:
        print("Configuration file missing. Please ensure 'password.py' is present.")
        exit(1)

    print("The password is 'owner'. For evaluation purposes, the user is aware of the password")
    password = input("Enter the password 'owner': ").strip()
    if password == PASSWORD:
        print("Password correct. Proceeding with analysis...")
        return True
    else:
        print(f"Incorrect password. The correct password is '{PASSWORD}'.")
        return False

def handle_user_role(user_role, google_sheet):
    """
    Handle the actions based on user role input.
    """
    try:
        if user_role == 'customer':
            try:
                survey = sm.Survey(google_sheet)  # Pass the GoogleSheet instance to Survey
                customer_responses = survey.get_customer_answers()
                survey.update_survey_worksheet(customer_responses)
            except Exception as e:
                print(f"An error occurred while processing customer responses: {e}")

        elif user_role == 'owner':
            if validate_password():  
                try:
                    analysis = am.Analysis(google_sheet)  # Pass the GoogleSheet instance to Analysis
                    averages = analysis.calculate_averages()
                    analysis.update_analysis_worksheet(averages)
                    analysis.print_survey_averages()
                    
                    while True:
                        # Ask the owner if they want to export the analysis to CSV
                        export_choice = input("Do you want to export the analysis data to a CSV file? (yes/no): ").strip().lower()
                        if export_choice == 'yes':
                            analysis.export_analysis_to_csv()  # Call without filename
                            break  # Exit the loop
                        elif export_choice == 'no':
                            print("Skipping export to CSV.")
                            break  
                        else:
                            print("Invalid input. Please enter 'yes' or 'no'.")

                except Exception as e:
                    print(f"An error occurred while processing survey analysis: {e}")

        else:
            print("Invalid role. Please enter 'customer' or 'owner'.")
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
    google_sheet = gs.GoogleSheet('customer_survey')  # Initialize GoogleSheet instance with the correct sheet name

    while True:
        user_role = input("Are you a customer or the owner? (Enter 'customer' or 'owner'): ").strip().lower()
        if handle_user_role(user_role, google_sheet):
            continue_prompt = get_user_continue_response()
            if continue_prompt != 'yes':
                print("Exiting the program.")
                break

main()