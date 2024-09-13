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
        print("Updating analysis worksheet with averages...\n")
        number_of_responses = len(self.get_survey_data())  # Total number of responses

        data = [
            number_of_responses,  # Number of responses
            averages[0],  # overal satisfaction
            averages[1],  # product quality
            averages[2],  # customer support
            averages[3],  # recommendation
        ]
        self.analysis_sheet.append_row(data)
        print("Analysis worksheet updated successfully.\n")

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

        print("\nSurvey Averages:")
        for header, value in zip(headers, latest_data):
            print(f"{header} {value}")

            #Second function of analysis

    def export_analysis_to_csv(self):
        """
        Export the analysis data to a CSV file with a fixed path.
        """
        fixed_filename = 'analysis_report.csv'  # Fixed path and filename
        try:
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
            with open(fixed_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)
                
            print(f"Analysis data exported to {fixed_filename} successfully.")

        except Exception as e:
            print(f"An error occurred while exporting to CSV: {e}")