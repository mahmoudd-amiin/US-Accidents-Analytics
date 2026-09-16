# Data Dictionary

This document describes the main fields used in the US Accidents Analytics project .

The project starts with the original US Accidents dataset , applies Python-based cleaning and feature engineering , and loads the processed data into a SQL Server data warehouse for Power BI analysis.

---

## 1. Accident Information

| Column | Data Type | Description |
| ID | String | Unique identifier for each accident |
| Source | String | Source of the accident record |
| Severity | Integer | Accident severity level from 1 to 4 |
| Description | String | Textual description of the accident |
| Distance(mi) | Numeric | Estimated length of the road segment affected by the accident |
| Start_Time | Datetime | Date and time when the accident started |
| End_Time | Datetime | Date and time when the accident ended |

### Severity Levels

| Severity | Project Label |
| 1 | Low |
| 2 | Moderate |
| 3 | High |
| 4 | Severe |

These labels are analytical labels used by this project to simplify Power BI reporting.

---

## 2. Geographic Information

| Column | Data Type | Description |
|---|---|---|
| Start_Lat | Numeric | Latitude of the accident starting location |
| Start_Lng | Numeric | Longitude of the accident starting location |
| End_Lat | Numeric | Latitude of the accident ending location |
| End_Lng | Numeric | Longitude of the accident ending location |
| Street | String | Street where the accident occurred |
| City | String | City where the accident occurred |
| County | String | County where the accident occurred |
| State | String | US state where the accident occurred |
| Zipcode | String | ZIP code of the accident location |
| Country | String | Country |
| Timezone | String | Local timezone |

---

## 3. Weather Information

| Column | Data Type | Description |
|---|---|---|
| Weather_Timestamp | Datetime | Timestamp of the available weather observation |
| Temperature(F) | Numeric | Temperature in Fahrenheit |
| Wind_Chill(F) | Numeric | Wind chill temperature in Fahrenheit |
| Humidity(%) | Numeric | Relative humidity percentage |
| Pressure(in) | Numeric | Atmospheric pressure |
| Visibility(mi) | Numeric | Visibility distance in miles |
| Wind_Direction | String | Wind direction |
| Wind_Speed(mph) | Numeric | Wind speed in miles per hour |
| Precipitation(in) | Numeric | Precipitation amount in inches |
| Weather_Condition | String | Reported weather condition |

---

## 4. Road & Infrastructure Information

The original dataset contains several road infrastructure indicators.

| Column | Data Type | Description |
| Amenity | Boolean | Indicates whether an amenity was present |
| Bump | Boolean | Indicates whether a bump was present |
| Crossing | Boolean | Indicates whether a crossing was present |
| Give_Way | Boolean | Indicates whether a give-way sign was present |
| Junction | Boolean | Indicates whether a junction was present |
| No_Exit | Boolean | Indicates whether a no-exit feature was present |
| Railway | Boolean | Indicates whether a railway crossing was present |
| Roundabout | Boolean | Indicates whether a roundabout was present |
| Station | Boolean | Indicates whether a station was present |
| Stop | Boolean | Indicates whether a stop sign was present |
| Traffic_Calming | Boolean | Indicates whether traffic-calming infrastructure was present |
| Traffic_Signal | Boolean | Indicates whether a traffic signal was present |
| Turning_Loop | Boolean | Indicates whether a turning loop was present |

For the SQL Data Warehouse , these individual infrastructure indicators are aggregated into : Infrastructure_Feature_Count