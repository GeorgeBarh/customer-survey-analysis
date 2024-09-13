import csv
import os

class Analysis:
    """
    Handles survey data analysis.
    """
    def __init__(self, google_sheet):
        self.survey_sheet = google_sheet.get_worksheet("survey")
        self.analysis_sheet = google_sheet.get_worksheet("analysis")

    def get_survey_data(self):
        """
        Retrieve all survey responses.
        """
        data = self.survey_sheet.get_all_values()  
        return data[1:]  # Exclude the header row

    def calculate_averages(self):
        """
        Calculate average ratings for each survey question.
        """
        data = self.get_survey_data()
        total_sums = [0, 0, 0, 0]  # There are 4 questions in the survey
        count = len(data)  # Number of responses (rows)

        for row in data:
            total_sums[0] += int(row[1])  # Overal satisfaction
            total_sums[1] += int(row[2])  # Product quality
            total_sums[2] += int(row[3])  # Customer support
            total_sums[3] += int(row[4])  # recomendation

        averages = [round(total / count) for total in total_sums]
        return averages

    def update_analysis_worksheet(self, averages):
        """
        Update the analysis worksheet with the latest averages.
        """
        print("Updating analysis worksheet with averages...")
        number_of_responses = len(self.get_survey_data())  # Total number of responses

        data = [
            number_of_responses,  # Number of responses
            averages[0],  # overal satisfaction
            averages[1],  # product quality
            averages[2],  # customer support
            averages[3],  # recommendation
        ]
        self.analysis_sheet.append_row(data)
        print("Analysis worksheet updated successfully.")

    def print_survey_averages(self):
        """
        Retrieve and print survey averages with descriptive messages.
        """
        rows = self.analysis_sheet.get_all_values()

        if len(rows) < 2:
            print("No data available in the analysis worksheet.")
            return

        headers = rows[0]  # Headers are in the first row
        latest_data = rows[-1]  # Latest data is in the last row

        print("\nSurvey Averages List:")
        for header, value in zip(headers, latest_data):
            print(f"{header} {value}")

            #Second function of analysis
    def get_feedback_message(self, score, criterion):
        """
        Return feedback message based on the score for a given criterion.
        """
        # Feedback messages for different score levels
        feedback_messages = {
            1: f"{criterion} is {score}. Extremely poor. Immediate action is required to address the issues.",
            2: f"{criterion} is {score}. Below expectations. Significant improvements are needed.",
            3: f"{criterion} is {score}. Average. Consider making improvements to enhance satisfaction.",
            4: f"{criterion} is {score}. Good. Keep up the good work, but look for areas to enhance further.",
            5: f"{criterion} is {score}. Excellent. Continue with the current practices to maintain high standards."
        }

        # Return the feedback message for the score or a default message if invalid
        return feedback_messages.get(score, f"{criterion} has an invalid score: {score}.")

    def provide_feedback(self):
        """
        Provide feedback based on survey averages.
        """
        averages = self.calculate_averages()  # Calculate survey averages

        print("\nFeedback Based on Averages:")
    
        # List of criteria corresponding to each average value
        criteria = [
        "Overall Satisfaction",
        "Product Quality",
        "Customer Support",
        "Recommendation"
        ]

        # Loop through each average score and its corresponding criterion
        for average, criterion in zip(averages, criteria):
            # Convert average to an integer score (assuming score is rounded to the nearest whole number)
            rounded_score = round(average)
        
            # Print feedback for the criterion based on the rounded score
            print(self.get_feedback_message(rounded_score, criterion))



            #Third function of analysis

    def export_analysis_to_csv(self):
        """
        Export the analysis data to a CSV file in the 'reports' directory.
        """
        try:
            # Define the path for the CSV file
            if not os.path.exists('reports'):
                os.makedirs('reports')  # Create the 'reports' directory if it doesn't exist

            filename = 'reports/analysis_report.csv'  # Path to the CSV file

            # Collect data
            averages = self.calculate_averages()
            total_responses = len(self.get_survey_data())

            # Prepare data for CSV
            headers = [
                "Metric", "Value"
            ]
            data = [
                ["Total Responses", total_responses],
                ["Average Overall Satisfaction", averages[0]],
                ["Average Product Quality", averages[1]],
                ["Average Customer Support", averages[2]],
                ["Average Recommendation", averages[3]]
            ]

            # Write to CSV
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file,)
                writer.writerow(headers)
                writer.writerows(data)
                
            print(f"\nAnalysis data exported to {filename} successfully.")

        except Exception as e:
            print(f"\nAn error occurred while exporting to CSV: {e}")