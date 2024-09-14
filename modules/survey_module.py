class Survey:
    """
    Handles customer survey responses.
    Manages collecting responses from customers, validating input, and updating the worksheet.
    """
    def __init__(self, google_sheet):
        """
        Initialize the Survey class with the Google Sheets worksheet for survey.
        """
        self.sheet = google_sheet.get_worksheet("survey")  # Get the "survey" worksheet from Google Sheets

    def get_customer_answers(self):
        """
        Collect customer survey responses and assign a new customer ID.
        Prompts the user to answer a series of questions and validates their input.
        """
        print("\nPlease rate your customer experience in the next four questions.")
        print("Data must be a number from 1-5 based on the following:")
        print("""
        1 - Bad experience
        2 - Poor experience
        3 - Neutral experience
        4 - Good experience
        5 - Best experience
              """)

        responses = []  # List to store customer responses
        last_customer_id = self.get_last_customer_id()  # Get the last customer ID from the worksheet
        current_customer_id = last_customer_id + 1  # Increment ID for the new customer

        questions = [
            "How would you rate your overall satisfaction with our service? (1-5): \n",
            "How satisfied are you with the quality of the product you received? (1-5): \n",
            "How would you rate your experience with our customer support team? (1-5): \n",
            "Would you to recommend our product/service to a friend or colleague? (1-5): \n"
        ]

        responses.append(current_customer_id)  # Add the new customer ID to the responses

        for question in questions:
            while True:
                response = input(question)  # Prompt user for a response
                try:
                    validated_response = self.validate_response(response)  # Validate and convert response
                    responses.append(validated_response)  # Add validated response to list
                    break
                except ValueError as e:
                    print(e)  # Print validation error message and re-prompt

        return responses

    def validate_response(self, response):
        """
        Ensure the response is a number between 1 and 5.
        Validates the user's input to ensure it is within the acceptable range.
        """
        try:
            response = int(response)  # Convert response to integer
            if response >= 1 and response <= 5:
                return response  # Return valid response
            else:
                raise ValueError("Number must be between 1 and 5.")  # Raise error for out-of-range values
        except ValueError:
            raise ValueError("Invalid input. Please enter a number between 1 and 5.")  # Handle non-integer inputs

    def get_last_customer_id(self):
        """
        Retrieve the last customer ID from the survey worksheet.
        If no previous data exists, start with ID 1.
        """
        data = self.sheet.get_all_values()  # Get all values from the worksheet
        if len(data) > 1:
            last_row = data[-1]  # Get the last row of data
            last_customer_id = int(last_row[0])  # Customer ID is in the first column of the last row
        else:
            last_customer_id = 1  # Start with ID 1 if no data exists
        return last_customer_id

    def update_survey_worksheet(self, data):
        """
        Update the survey worksheet with a new row of data.
        Appends the collected responses to the Google Sheets worksheet.
        """
        self.sheet.append_row(data)  # Append the new row of data to the worksheet
        print("\nSurvey worksheet updated successfully.")  # Confirmation message
        print("Thanks for your feedback! \n")  # Thank the customer for their feedback
