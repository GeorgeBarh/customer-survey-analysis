# Customer Survey Analysis

The Customer Survey Analysis Program is a Python-based application designed to handle, analyze, and report on customer feedback. This project integrates Google Sheets for data storage and employs various Python modules to manage user interactions, process survey responses, and generate insightful reports. Users can interact with the application as either a Customer or Owner. Customers provide feedback through a survey, while owners analyze the collected data and generate reports.

You can access the live version of the application [here](https://customer-survey-analysis-f7747660b229.herokuapp.com/).

![Screenshot of Responsiveness](images/responsive.png)

## Table of Contents

1. [Project Overview](#project-overview)
   1.1 [User Stories](#user-stories)
2. [Design and Architecture](#design-and-architecture)
3. [Data Model](#data-model)
4. [Features](#features)
5. [Deployment](#deployment)
6. [Credits](#credits)

## Project Overview

The Customer Survey Analysis Program aims to facilitate efficient collection and analysis of customer feedback. This project leverages Google Sheets for data storage and uses Python to handle different roles, process survey responses, and generate analytical reports. The application is designed to provide valuable insights into customer satisfaction and identify areas for improvement.

### 1.1 User Stories

#### As a Customer, I want to:

- **Provide Feedback**: Complete a survey to rate various aspects of the service, including overall satisfaction, product quality, customer support, and willingness to recommend the service.
- **Receive Confirmation**: Get a confirmation message after submitting the survey, thanking me for my feedback and letting me know that my responses have been recorded.

#### As an Owner, I want to:

- **Analyze Data**: Access survey responses to analyze overall customer satisfaction, product quality, customer support, and recommendation scores.
- **Generate Reports**: Export the analysis results to a CSV file and view detailed feedback based on average ratings.
- **Update Analysis**: See real-time updates of survey results and feedback in the Google Sheets analysis worksheet.
- **Print and Review**: Print or view the contents of the generated CSV file to review the analysis data.

## Design and Architecture

### Modular Design

The project is structured into separate modules to improve maintainability, readability, and scalability. Each module focuses on a specific aspect of the application:

- **google_sheet.py**: Handles Google Sheets API integration and provides methods to access and manipulate worksheets.
- **survey_module.py**: Manages customer survey responses, including collection, validation, and updating the survey worksheet.
- **analysis_module.py**: Analyzes survey data, calculates averages, provides feedback, and exports analysis reports to CSV.

This modular approach allows for clear separation of concerns, making the codebase easier to manage and extend. Each module encapsulates its functionality, promoting reusability and simplifying testing.

### Object-Oriented Programming (OOP)

The application utilizes object-oriented programming principles to enhance the design and functionality:

- **Classes**: Key components of the application are represented as classes. These classes encapsulate related data and behaviors, making the code more organized and easier to understand.
- **Encapsulation**: Each class encapsulates specific functionality, such as handling survey data or analyzing results, which helps in isolating changes and reducing dependencies.
- **Modularity**: By using classes, the project leverages OOP principles to create modular, self-contained units of functionality that can be independently developed and tested.

This object-oriented design pattern enhances code readability, reusability, and maintainability, aligning with best practices in software development.

## Data Model

The project uses the following data model to structure and store survey responses:

- **Survey Responses**: Each response consists of the following fields:
  - **Customer ID**: A unique identifier for each customer.
  - **Overall Satisfaction**: Rating from 1 to 5.
  - **Product Quality**: Rating from 1 to 5.
  - **Customer Support**: Rating from 1 to 5.
  - **Recommendation**: Rating from 1 to 5.

The data is stored in a Google Sheets document with separate worksheets for survey responses and analysis results.
