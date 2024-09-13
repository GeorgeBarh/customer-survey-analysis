class Survey:
    """
    Handles customer survey responses.
    """
    def __init__(self, google_sheet):
        self.sheet = google_sheet.get_worksheet("survey")

    def get_customer_answers(self):
        """
        collect customer survey responses and assign a new customer id
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
        last_customer_id = self.get_last_customer_id()  # Get the last customer id
        current_customer_id = last_customer_id + 1  # Increment for the new customer

        questions = [
            "How would you rate your overall satisfaction with our service? (1-5): \n",
            "How satisfied are you with the quality of the product you received? (1-5): \n",
            "How would you rate your experience with our customer support team? (1-5): \n",
            "How likely are you to recommend our product/service to a friend or colleague? (1-5): \n"
        ]

        responses.append(current_customer_id)  # Add the customer id

        for question in questions:
            while True:
                response = input(question)  
                try:
                    validated_response = self.validate_response(response)  # Validate input
                    responses.append(validated_response)  # Add validated response
                    break
                except ValueError as e:
                    print(e)  

        return responses

    def validate_response(self, response):
        """
        Ensure the response is a number between 1 and 5.
        """
        try:
            response = int(response)
            if response >= 1 and response <= 5:
                return response
            else:
                raise ValueError("Number must be between 1 and 5.")
        except ValueError:
            raise ValueError("Invalid input. Please enter a number between 1 and 5.")

    def get_last_customer_id(self):
        """
        retrieve the last customer ID from the survey worksheet.
        """
        data = self.sheet.get_all_values()
        if len(data) > 1:
            last_row = data[-1]
            last_customer_id = int(last_row[0])  # customers id is in the first column
        else:
            last_customer_id = 1  # Start with 1 if no data
        return last_customer_id

    def update_survey_worksheet(self, data):
        """
        Update survey worksheet with new row of data.
        """
        print("Updating survey worksheet...\n")
        self.sheet.append_row(data)
        print("Survey worksheet updated successfully.\n")