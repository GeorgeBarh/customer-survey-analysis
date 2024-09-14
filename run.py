import modules.google_sheet as gs
import modules.survey_module as sm
import modules.analysis_module as am

def handle_user_role(user_role, google_sheet):
    """
    Handle actions based on the user role. Calls different functions 
    depending on whether the role is 'customer' or 'owner'. 
    Prints an error message for invalid roles and handles exceptions.
    """
    try:
        if user_role == 'customer':
            handle_customer_role(google_sheet)  # Handle actions specific to customers

        elif user_role == 'owner':
            handle_owner_role(google_sheet)  # Handle actions specific to owners

        else:
            print("Invalid role. Please enter 'customer' or 'owner'.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def handle_customer_role(google_sheet):
    """
    Manage actions for the customer role. Collects customer survey responses 
    and updates the Google Sheet with these responses.
    """
    try:
        survey = sm.Survey(google_sheet)  # Initialize Survey instance
        customer_responses = survey.get_customer_answers()  # Collect responses
        survey.update_survey_worksheet(customer_responses)  # Update worksheet
    except Exception as e:
        print(f"An error occurred while processing customer responses: {e}")

def validate_password():
    """
    Check the password for accessing owner functionalities. 
    Prompts the user for the password and verifies it.
    """
    try:
        from password import PASSWORD  # Import the correct password
    except ImportError:
        print("Configuration file missing. Please ensure 'password.py' is present.")
        exit(1)

    print("\nThe password is 'owner'.") 
    print("For the project's assessment purposes, the user is aware of the password.")
    password = input("Enter the password 'owner': \n").strip()  # Prompt user for password
    if password == PASSWORD:
        print("\nPassword correct. Proceeding with analysis...")
        return True
    else:
        print(f"\nIncorrect password. The correct password is '{PASSWORD}'.")
        return False

def handle_owner_role(google_sheet):
    """
    Manage actions for the owner role. Validates the password and, if correct, 
    updates the analysis and displays a menu of functionalities.
    """
    if validate_password():
        try:
            analysis = am.Analysis(google_sheet)  # Initialize Analysis instance
            analysis.update_analysis_worksheet()  # Update analysis worksheet

            # Display menu of functionalities
            analysis.display_functionality_menu()

        except Exception as e:
            print(f"An error occurred while processing survey analysis: {e}")

def get_user_continue_response():
    """
    Ask the user if they want to perform another action. 
    Continues to prompt until a valid response ('yes' or 'no') is provided.
    """
    while True:
        try:
            answer = input("Do you want to perform another action? (yes/no): \n").strip().lower()
            if answer in ['yes', 'no']:
                return answer
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        except Exception as e:
            print(f"An error occurred while processing your input: {e}")

def display_welcome_message():
    """
    Display a welcome message and introduce the program. 
    Informs the user about the two available roles: customer and owner.
    """
    print("\nWelcome to the Customer Survey Analysis Program.\n")
    print("This program is designed for educational purposes.")
    print("You can run the app in one of two roles:")
    print("1. **Customer**: Complete the survey to provide feedback.")
    print("2. **Owner**: Analyze the survey data and generate reports.")
    print("\nPlease choose your role to proceed.\n")

def main():
    """
    Main function to run the program. Initializes the GoogleSheet instance, 
    handles user role input, and allows the user to perform actions based on their role.
    """
    # Display the welcome message
    display_welcome_message()
    google_sheet = gs.GoogleSheet('customer_survey')  # Initialize GoogleSheet instance

    while True:
        user_role = input("Are you a customer or the owner? (Enter 'customer' or 'owner'): \n").strip().lower()
        if handle_user_role(user_role, google_sheet):
            continue_prompt = get_user_continue_response()
            if continue_prompt != 'yes':
                print("Exiting the program.")
                break

main()