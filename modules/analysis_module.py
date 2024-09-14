import os
import csv

class SurveyDataAnalyzer:
    """
    Analyzes survey data and calculates averages.
    Provides functionality to retrieve data, calculate averages, and provide feedback.
    """
    def __init__(self, survey_sheet):
        """
        Initialize with a reference to the survey sheet.
        """
        self.survey_sheet = survey_sheet

    def get_survey_data(self):
        """
        Retrieve all survey responses from the worksheet.
        Excludes the header row for processing.
        """
        data = self.survey_sheet.get_all_values()
        return data[1:]  # Exclude the header row

    def calculate_averages(self):
        """
        Calculate average ratings for each survey question.
        Computes total sums and averages for four survey questions.
        """
        data = self.get_survey_data()
        total_sums = [0, 0, 0, 0]  # There are 4 questions in the survey
        count = len(data)  # Number of responses (rows)

        # Accumulate totals for each question
        for row in data:
            total_sums[0] += int(row[1])  # Overall satisfaction
            total_sums[1] += int(row[2])  # Product quality
            total_sums[2] += int(row[3])  # Customer support
            total_sums[3] += int(row[4])  # Recommendation

        if count == 0:
            return [0, 0, 0, 0]  # Avoid division by zero if no data is present

        # Calculate and round averages
        averages = [round(total / count) for total in total_sums]
        return averages

    class FeedbackProvider:
        """
        Provides feedback based on survey averages.
        Maps average ratings to predefined feedback messages.
        """
        def __init__(self):
            self.feedback_messages = {
                1: "Extremely poor. Immediate action is required to address the issues.",
                2: "Below expectations. Significant improvements are needed.",
                3: "Average. Consider changes to enhance satisfaction.",
                4: "Good. Keep up the good work, but look for areas to enhance further.",
                5: "Excellent. Continue with the current practices to maintain high standards."
                }

        def provide_feedback(self, averages):
            """
            Provide feedback based on survey averages.
            Prints feedback for each survey criterion.
            """
            print("\nFeedback Based on Averages:")
            criteria = [
                "Overall Satisfaction",
                "Product Quality",
                "Customer Support",
                "Recommendation"
            ]

            for average, criterion in zip(averages, criteria):
                print(f"{criterion}: {self.get_feedback_message(average)}")

        def get_feedback_message(self, score):
            """
            Return feedback message based on the score.
            Retrieves the message corresponding to the provided score.
            """
            return self.feedback_messages.get(score, "Invalid score.")

class ReportExporter:
    """
    Exports survey analysis data to a CSV file.
    Handles the creation of a CSV report in the 'reports' directory and printing its contents.
    """
    def __init__(self, survey_data_analyzer):
        """
        Initialize with a reference to the SurveyDataAnalyzer.
        
        :param survey_data_analyzer: An instance of SurveyDataAnalyzer for accessing survey data and calculations.
        """
        self.survey_data_analyzer = survey_data_analyzer

    def export_analysis_to_csv(self):
        """
        Export the analysis data to a CSV file in the 'reports' directory.
        Handles directory creation and file writing.

        The method performs the following steps:
        1. Creates the 'reports' directory if it does not exist.
        2. Collects average ratings and total responses from the survey data.
        3. Generates feedback messages based on the average ratings.
        4. Prepares the data for CSV export, including metrics, values, and feedback.
        5. Writes the data to the CSV file with appropriate headers.

        :raises Exception: If an error occurs during file operations, an exception is raised.
        """
        try:
            # Create 'reports' directory if it doesn't exist
            if not os.path.exists('reports'):
                os.makedirs('reports')

            filename = 'reports/analysis_report.csv'  # Path to the CSV file

            # Collect data
            averages = self.survey_data_analyzer.calculate_averages()
            total_responses = len(self.survey_data_analyzer.get_survey_data())

            # Create feedback based on averages
            feedback_provider = SurveyDataAnalyzer.FeedbackProvider()
            feedback = [feedback_provider.get_feedback_message(average) for average in averages]

            # Prepare data for CSV
            headers = ["Metric", "Value", "Feedback"]
            data = [
                ["Total Responses", str(total_responses), "-"],  # Set feedback for Total Responses to a dash
                ["Overall Satisfaction", str(averages[0]), feedback[0]],
                ["Product Quality", str(averages[1]), feedback[1]],
                ["Customer Support", str(averages[2]), feedback[2]],
                ["Recommendation", str(averages[3]), feedback[3]]
            ]

            # Write to CSV
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)  # Write the header row
                writer.writerows(data)    # Write the data rows
            
            print(f"\nExporting data to {filename}...")
            print(f"Analysis data exported to {filename} successfully.")

        except Exception as e:
            print(f"\nAn error occurred while exporting to CSV: {e}")

    def print_csv_contents(self):
        """
        Print the contents of the CSV file to the console.
        Reads and displays the contents of the CSV file.
        """
        filename = 'reports/analysis_report.csv'  # Path to the CSV file

        try:
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    print(', '.join(row))  # Join row elements into a single string separated by commas
        
        except Exception as e:
            print(f"An error occurred while printing CSV contents: {e}")

class Analysis:
    """
    Manages survey analysis, feedback, and reporting functionalities.
    Integrates survey data analysis, feedback provision, and report exporting.
    """
    def __init__(self, google_sheet):
        """
        Initialize with a reference to the GoogleSheet instance.
        Set up components for data analysis, feedback, and reporting.
        """
        self.data_analyzer = SurveyDataAnalyzer(google_sheet.get_worksheet("survey"))
        self.feedback_provider = SurveyDataAnalyzer.FeedbackProvider()
        self.report_exporter = ReportExporter(self.data_analyzer)
        self.google_sheet = google_sheet

    def update_analysis_worksheet(self):
        """
        Update the analysis worksheet with the latest averages.
        Appends a new row with the number of responses and average ratings.
        """
        averages = self.data_analyzer.calculate_averages()
        analysis_sheet = self.google_sheet.get_worksheet("analysis")
        number_of_responses = len(self.data_analyzer.get_survey_data())

        data = [
            number_of_responses,  # Number of responses
            averages[0],  # Overall satisfaction
            averages[1],  # Product quality
            averages[2],  # Customer support
            averages[3],  # Recommendation
        ]
        analysis_sheet.append_row(data)
        print("Analysis worksheet updated successfully.")

    def display_functionality_menu(self):
        """
        Display functionality menu and handle user choices.
        Provides options for printing averages, providing feedback, exporting data, printing CSV contents, and exiting.
        """
        while True:
            print("\nAvailable functionalities:")
            print("1. Print customer rating")
            print("2. Provide feedback based on averages")
            print("3. Export analysis to CSV")
            print("4. Print CSV file contents")
            print("5. Exit menu")

            choice = input("Select a functionality (1-5): \n").strip()

            if choice == '1':
                self.print_survey_averages()

            elif choice == '2':
                averages = self.data_analyzer.calculate_averages()
                self.feedback_provider.provide_feedback(averages)

            elif choice == '3':
                self.handle_export_csv()

            elif choice == '4':
                self.report_exporter.print_csv_contents()

            elif choice == '5':
                # Ask if the user wants to perform another action
                while True:
                    continue_choice = input("Would you like to perform any other actions? (yes/no):\n").strip().lower()
                    if continue_choice == 'yes':
                        print("Returning to the main menu...")
                        return  # Exit the current loop and restart the main menu
                    elif continue_choice == 'no':
                        print("Thank you for using the program. Exiting now.")
                        exit()  # Exit the program
                    else:
                        print("Please enter 'yes' or 'no'.")

            else:
                print("Invalid choice. Please select a number between 1 and 5.")

    def handle_export_csv(self):
        """
        Handle exporting analysis data to CSV with valid input.
        Prompts the user to confirm the export action.
        """
        while True:
            export_choice = input("Do you want to export the analysis data to a CSV file? (yes/no):\n").strip().lower()
            if export_choice == 'yes':
                # Export analysis data to CSV
                self.report_exporter.export_analysis_to_csv()
                
                # Path to the generated CSV file
                csv_file_path = 'reports/analysis_report.csv'  # Ensure this path matches the exported CSV
                
                # Import data from the CSV file to the 'report' worksheet
                self.import_csv_to_report(csv_file_path)
                
                break
            elif export_choice == 'no':
                print("Skipping export to CSV.")
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")

    def import_csv_to_report(self, csv_file_path):
        """
        Import data from a CSV file and write it to the 'report' worksheet.
        
        :param csv_file_path: Path to the CSV file to import.
        """
        try:
            worksheet = self.google_sheet.get_worksheet("report")  # Ensure 'report' worksheet is accessed correctly
            
            # Clear existing data in the 'report' worksheet (optional)
            worksheet.clear()  # Uncomment if you want to clear the existing data before importing new data
            
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    worksheet.append_row(row)  # Append each row from the CSV to the worksheet
            
            print(f"Data from {csv_file_path} has been imported to the 'report' worksheet.")
        
        except Exception as e:
            print(f"An error occurred while importing data to the report worksheet: {e}")

    def print_survey_averages(self):
        """
        Retrieve and print survey averages.
        Displays the average ratings for each survey criterion.
        """
        averages = self.data_analyzer.calculate_averages()
        print("\nAverage Customer Rating List:")
        criteria = [
            "Overall Satisfaction",
            "Product Quality",
            "Customer Support",
            "Recommendation"
        ]
        for average, criterion in zip(averages, criteria):
            print(f"{criterion}: {average}")