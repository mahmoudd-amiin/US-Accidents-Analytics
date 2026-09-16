Objectives

The main objectives of this project are:

Analyze accident trends over time
Identify peak accident hours and days
Analyze accident severity
Investigate seasonal accident patterns
Analyze weather conditions associated with accidents
Study visibility and temperature patterns
Analyze road infrastructure indicators
Identify accident hotspots by state, city, and county
Build a structured SQL Server data warehouse
Create an interactive Power BI dashboard
Provide a reusable analytical workflow for road-safety data
Dataset

The project uses the:

US Accidents (2016–2023) dataset.

The original dataset contains approximately 7.7 million accident records across the United States.

Because of the size of the original dataset, this project uses a 500,000-record sample.

Dataset Statistics
Metric	Value
Original Records	7,728,394
Project Records	500,000
Original Columns	46
Processed Columns	59
Years	2016–2023
States	49
Duplicate IDs	0

The raw dataset is not included in this repository because of its large size.

Data Processing

Python was used to clean and transform the dataset before loading it into SQL Server.

Main ETL Operations
Datetime parsing
Missing-value handling
Duplicate validation
Weather data validation
Wind direction standardization
Accident duration calculation
Duration categorization
Year/month/day/hour extraction
Day-of-week calculation
Weekend identification
Season classification
Daytime identification
Weather availability calculation
End-location availability
Infrastructure feature counting
Data type conversion

The final processed dataset contains:

500,000 rows
59 columns
0 duplicate accident IDs
Data Warehouse

The project uses Microsoft SQL Server to create a dimensional data warehouse.

Database:

USAccidentsDW

The warehouse follows a Star Schema.

                    DimDate
                       |
                       |
DimLocation ---- FactAccident ---- DimWeatherCondition
                       |
                       |
                  DimSeverity
Fact Table

FactAccident

Contains accident-level measurements and foreign keys.

Dimension Tables
DimDate
DimLocation
DimSeverity
DimWeatherCondition
Warehouse Statistics
Table	Records
FactAccident	500,000
DimLocation	203,634
DimWeatherCondition	1,115
DimSeverity	4
DimDate	2,647
Data Integrity
Validation	Result
Fact Records	500,000
Missing Date Keys	0
Missing Location Keys	0
Missing Weather Keys	0
Missing Severity Keys	0
Duplicate Accident IDs	0
Power BI Dashboard

The final analysis was developed in Microsoft Power BI.

The dashboard contains four analytical pages.

1. US ACCIDENTS
Emergency & Road Safety Intelligence

The overview page provides a high-level view of accident patterns.

Main analysis:

Accidents by Year
Accidents by Severity
Accidents by Month
Weekend vs Daytime
Accident decomposition by multiple dimensions
State-level accident comparison
2. TIME & SEVERITY ANALYSIS
Accident Patterns Across Time & Severity

This page focuses on temporal patterns and accident severity.

Main analysis:

Accidents by Hour of Day
Accidents by Day of Week
Accidents by Season and Severity
Severity Trends Over Years
Average Accident Duration by Severity
Accident Hotspots by Day and Hour

Key indicators include:

Peak Accident Hour
Peak Accident Day
Average Accident Duration
Severe Accident Rate
3. WEATHER & ROAD ANALYSIS
Weather Conditions & Road Risk Patterns

This page investigates the relationship between accidents, weather, and road infrastructure.

Main analysis:

Top Weather Conditions
Severity by Weather Condition
Accidents by Visibility Range
Accidents by Temperature Range
Severity Ranking by Visibility
Infrastructure Feature Distribution

Key weather indicators include:

Average Temperature
Average Visibility
Average Wind Speed
4. GEOGRAPHIC RISK ANALYSIS
Accident Hotspots & Regional Risk Patterns

This page focuses on geographic accident distribution.

Main analysis:

Accidents by State
Top 10 States
Top 10 Cities
Top 15 Counties
State Risk Summary
Geographic accident hotspots
Dashboard Interactivity

The Power BI dashboard includes synchronized filters across the analytical pages.

Available Slicers

Year

2016 → 2023

Severity

Low
Moderate
High
Severe

The slicers are synchronized across the dashboard pages to provide consistent filtering.

Key Metrics

The dashboard includes several analytical measures such as:

Total Accidents
Severe Accidents
High Severity Accidents
Weekend Accidents
Daytime Accidents
Accidents with Weather Data
Average Accident Distance
Average Accident Duration
Average Severity
Severe Accident Rate
Peak Accident Hour
Peak Accident Day
Average Temperature
Average Visibility
Average Wind Speed
Total States
Total Cities
Top Accident State
Top Accident City
Technologies Used
Programming & Data Processing
Python
Pandas
NumPy
Database
Microsoft SQL Server
SQL
SQL Server Express
Business Intelligence
Microsoft Power BI
DAX
Data Format
CSV
Parquet
Development Tools
Visual Studio Code
SQL Server Management Studio
Power BI Desktop
Project Structure
US-Accidents-Analytics/
│
├── data/
│   ├── README.md
│   └── sample/
│
├── python/
│   ├── etl/
│   └── notebooks/
│
├── sql/
│   ├── database/
│   ├── dimensions/
│   └── fact/
│
├── powerbi/
│   ├── US_Accidents_Dashboard.pbix
│   └── screenshots/
│
├── documentation/
│   ├── data_dictionary.md
│   ├── data_warehouse.md
│   └── project_documentation.md
│
└── README.md
Project Architecture
                  US Accidents Dataset
                          │
                          ▼
                  ┌───────────────┐
                  │    Python     │
                  │      ETL      │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │    Parquet    │
                  │ Clean Dataset │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  SQL Server   │
                  │ Data Warehouse│
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │   Power BI    │
                  │   Dashboard   │
                  └───────────────┘
Data Quality

Several validation checks were performed during the ETL and warehouse loading processes.

Duplicate Validation
Duplicate Accident IDs = 0
Foreign Key Validation
Missing Date Keys = 0
Missing Location Keys = 0
Missing Weather Keys = 0
Missing Severity Keys = 0
Final Dataset
Rows    = 500,000
Columns = 59
Repository Notes

The original dataset and large processed files are not included in the repository because of their size.

The repository contains:

SQL database scripts
Dimension table scripts
Fact table script
Python ETL/load scripts
Documentation
Power BI dashboard
Dashboard screenshots

The dataset can be placed locally following the instructions in:

data/README.md
Author

Mahmoud Amin

Computer & Communications Engineering Student