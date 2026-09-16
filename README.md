#  US Accidents Analytics

### Emergency & Road Safety Intelligence

An end-to-end **Data Analytics & Business Intelligence** project built using the **US Accidents (2016–2023)** dataset.

The project transforms raw accident data into a structured **SQL Server Data Warehouse** and an interactive **Power BI Dashboard** to analyze accident patterns across time, severity, weather, road infrastructure, and geographic locations.

---

##  Project Overview

This project follows a complete data analytics pipeline:

```text
Raw CSV
   ↓
Python ETL
   ↓
Data Cleaning & Feature Engineering
   ↓
Cleaned Parquet
   ↓
SQL Server Data Warehouse
   ↓
Power BI Dashboard
```

The main goal is to transform large-scale accident data into meaningful insights that can support **road-safety analysis and risk identification**.

---

#  Objectives

The project focuses on:

*  Analyzing accident trends over time
*  Identifying peak accident hours and days
*  Analyzing accident severity
*  Investigating weather-related accident patterns
*  Studying temperature and visibility conditions
*  Analyzing road infrastructure indicators
*  Identifying accident hotspots
*  Comparing accident patterns across states, cities, and counties
*  Building a dimensional SQL Server Data Warehouse
*  Creating an interactive Power BI dashboard
*  Developing a reusable end-to-end analytics workflow

---

#  Dataset

The project uses the:

**US Accidents (2016–2023)** dataset.

The original dataset contains approximately **7.7 million accident records** across the United States.

Due to the large size of the original dataset, this project uses a representative sample of:

**500,000 accident records**

## Dataset Statistics

| Metric            |     Value |
| ----------------- | --------: |
| Original Records  | 7,728,394 |
| Project Records   |   500,000 |
| Original Columns  |        46 |
| Processed Columns |        59 |
| Years Covered     | 2016–2023 |
| States Covered    |        49 |
| Duplicate IDs     |         0 |

> The original raw dataset is not included in this repository because of its large file size.

---

#  Data Processing

Python was used to clean, validate, and transform the dataset before loading it into SQL Server.

## ETL Operations

The ETL process includes:

* Datetime parsing
* Missing-value handling
* Duplicate validation
* Weather data validation
* Wind direction standardization
* Accident duration calculation
* Duration categorization
* Year extraction
* Month extraction
* Day extraction
* Hour extraction
* Day-of-week calculation
* Weekend identification
* Season classification
* Daytime identification
* Weather availability calculation
* End-location availability
* Infrastructure feature counting
* Data type conversion

### Final Processed Dataset

```text
Rows       : 500,000
Columns    : 59
Duplicates : 0
Years      : 2016–2023
States     : 49
```

---

#  Data Warehouse

The project uses **Microsoft SQL Server** to build a dimensional Data Warehouse.

### Database

```text
USAccidentsDW
```

##  Star Schema

```text
                         ┌───────────────┐
                         │    DimDate    │
                         └───────┬───────┘
                                 │
                                 │
┌────────────────┐       ┌───────▼────────┐       ┌────────────────────────┐
│  DimLocation   │──────▶│  FactAccident  │◀──────│ DimWeatherCondition    │
└────────────────┘       └───────▲────────┘       └────────────────────────┘
                                 │
                                 │
                         ┌───────┴───────┐
                         │  DimSeverity  │
                         └───────────────┘
```

## Fact Table

### `FactAccident`

The central fact table contains accident-level measurements and foreign keys.

It includes:

* Accident ID
* Date and time
* Geographic coordinates
* Accident distance
* Accident duration
* Weather measurements
* Weekend/daytime indicators
* Weather availability
* Infrastructure feature count
* Dimension foreign keys

## Dimension Tables

| Table                 | Purpose                |
| --------------------- | ---------------------- |
| `DimDate`             | Date and time analysis |
| `DimLocation`         | Geographic analysis    |
| `DimSeverity`         | Accident severity      |
| `DimWeatherCondition` | Weather categories     |

---

#  Warehouse Statistics

| Table               | Records |
| ------------------- | ------: |
| FactAccident        | 500,000 |
| DimLocation         | 203,634 |
| DimWeatherCondition |   1,115 |
| DimSeverity         |       4 |
| DimDate             |   2,647 |

---

#  Data Integrity

Validation was performed after the warehouse loading process.

| Validation             |  Result |
| ---------------------- | ------: |
| Fact Records           | 500,000 |
| Duplicate Accident IDs |       0 |
| Missing Date Keys      |       0 |
| Missing Location Keys  |       0 |
| Missing Weather Keys   |       0 |
| Missing Severity Keys  |       0 |

---

#  Power BI Dashboard

The final analytical layer was developed using **Microsoft Power BI**.

The dashboard contains **four analytical pages**.

---

##  US ACCIDENTS

### Emergency & Road Safety Intelligence

The overview page provides a high-level view of accident patterns.

### Analysis

* Accidents by Year
* Accidents by Severity
* Accidents by Month
* Weekend vs Daytime
* Accident decomposition by multiple dimensions
* State-level accident comparison

---

##  TIME & SEVERITY ANALYSIS

### Accident Patterns Across Time & Severity

This page focuses on temporal patterns and accident severity.

### Analysis

* Accidents by Hour of Day
* Accidents by Day of Week
* Accidents by Season and Severity
* Severity Trends Over Years
* Average Accident Duration by Severity
* Accident Hotspots by Day and Hour

### Key Indicators

* Peak Accident Hour
* Peak Accident Day
* Average Accident Duration
* Severe Accident Rate

---

##  WEATHER & ROAD ANALYSIS

### Weather Conditions & Road Risk Patterns

This page investigates accident patterns related to weather and road infrastructure.

### Analysis

* Top Weather Conditions
* Severity by Weather Condition
* Accidents by Visibility Range
* Accidents by Temperature Range
* Severity Ranking by Visibility
* Infrastructure Feature Distribution

### Key Indicators

* Average Temperature
* Average Visibility
* Average Wind Speed

---

##  GEOGRAPHIC RISK ANALYSIS

### Accident Hotspots & Regional Risk Patterns

This page focuses on geographic accident distribution.

### Analysis

* Accidents by State
* Top 10 States
* Top 10 Cities
* Top 15 Counties
* State Risk Summary
* Geographic Accident Hotspots

---

#  Dashboard Interactivity

The dashboard includes synchronized filters across all analytical pages.

### Year Filter

```text
2016 → 2023
```

### Severity Filter

```text
Low
Moderate
High
Severe
```

The filters are synchronized across the four dashboard pages to maintain consistent analysis.

---

#  Key Metrics

The Power BI model includes analytical measures such as:

| Metric                      |
| --------------------------- |
| Total Accidents             |
| Severe Accidents            |
| High Severity Accidents     |
| Weekend Accidents           |
| Daytime Accidents           |
| Accidents with Weather Data |
| Average Accident Distance   |
| Average Accident Duration   |
| Average Severity            |
| Severe Accident Rate        |
| Peak Accident Hour          |
| Peak Accident Day           |
| Average Temperature         |
| Average Visibility          |
| Average Wind Speed          |
| Total States                |
| Total Cities                |
| Top Accident State          |
| Top Accident City           |

---

#  Technologies Used

## Programming & Data Processing

* Python
* Pandas
* NumPy

## Database

* Microsoft SQL Server
* SQL
* SQL Server Express

## Business Intelligence

* Microsoft Power BI
* DAX

## Data Formats

* CSV
* Parquet

## Development Tools

* Visual Studio Code
* SQL Server Management Studio
* Power BI Desktop

---

#  Project Structure

```text
US-Accidents-Analytics/
│
├── data/
│   ├── README.md
│   └── sample/
│
├── python/
│   ├── etl/
│   │   └── us_accidents_etl.py
│   └── notebooks/
│
├── sql/
│   ├── database/
│   │   └── create_database.sql
│   │
│   ├── dimensions/
│   │   ├── DimDate.sql
│   │   ├── DimLocation.sql
│   │   ├── DimSeverity.sql
│   │   └── DimWeatherCondition.sql
│   │
│   └── fact/
│       └── FactAccident.sql
│
├── powerbi/
│   ├── US_Accidents_Dashboard.pbix
│   └── screenshots/
│       ├── 01_overview.png
│       ├── 02_time_severity.png
│       ├── 03_weather_road.png
│       ├── 04_geographic_risk.png
│       └── traffic.png
│
├── documentation/
│   ├── data_dictionary.md
│   ├── data_warehouse.md
│   └── project_documentation.md
│
├── .gitignore
└── README.md
```

---

#  Project Architecture

```text
┌───────────────────────────────┐
│       US Accidents CSV        │
│       500K Records            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│          Python ETL           │
│                               │
│ Cleaning                      │
│ Validation                    │
│ Feature Engineering           │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Cleaned Parquet          │
│        500K × 59              │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      SQL Server DW            │
│                               │
│       USAccidentsDW           │
│                               │
│ Fact + Dimensions             │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│          Power BI             │
│                               │
│ Interactive Dashboard         │
│ 4 Analytical Pages            │
└───────────────────────────────┘
```

---

#  Data Quality

The project applies multiple data-quality checks throughout the pipeline.

### Duplicate Check

```text
Duplicate Accident IDs = 0
```

### Foreign Key Validation

```text
Missing Date Keys     = 0
Missing Location Keys = 0
Missing Weather Keys = 0
Missing Severity Keys = 0
```

### Final Dataset

```text
Rows    = 500,000
Columns = 59
```

---

#  Dashboard Preview

Dashboard screenshots are available in:

```text
powerbi/screenshots/
```

The Power BI project file is available at:

```text
powerbi/US_Accidents_Dashboard.pbix
```

---

#  Documentation

Additional project documentation:

* [`data_dictionary.md`](documentation/data_dictionary.md)
* [`data_warehouse.md`](documentation/data_warehouse.md)
* [`project_documentation.md`](documentation/project_documentation.md)

---

#  Repository Notes

The original US Accidents dataset and large processed data files are **not included** in the repository because of their size.

The repository contains the project's:

* Python ETL code
* SQL Server scripts
* Data Warehouse schema
* Power BI dashboard
* Dashboard screenshots
* Documentation

See:

```text
data/README.md
```

for dataset information and local setup instructions.

---

#  Author

## Mahmoud Amin

**Computer & Communications Engineering Student**

### Areas of Interest

* Cybersecurity
* Data Analytics
* Networking
* Cloud Technologies

---

# Disclaimer

This project is intended for **educational, analytical, and portfolio purposes**.

The analysis identifies patterns within the selected dataset and should not be interpreted as a direct causal assessment of accident risk.
