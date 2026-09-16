import pandas as pd
import pyodbc
import time

PARQUET_PATH = r"..\..\data\cleaned_500K\US_Accidents_500K_Cleaned.parquet"

SERVER = r".\SQLEXPRESS"
DATABASE = "USAccidentsDW"

BATCH_SIZE = 10000

start_time = time.time()

print("=" * 60)
print("US ACCIDENTS - SQL SERVER LOAD")
print("=" * 60)

print("\nConnecting to SQL Server...")

conn = pyodbc.connect(
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    rf"SERVER={SERVER};"
    rf"DATABASE={DATABASE};"
    r"Trusted_Connection=yes;"
)

cursor = conn.cursor()

print("Connected successfully")

print("\nLoading Parquet...")

df = pd.read_parquet(PARQUET_PATH)

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")

if len(df) != 500000:
    raise ValueError(
        f"ERROR: Expected 500,000 rows but found {len(df):,}"
    )

if df["ID"].duplicated().any():
    raise ValueError("ERROR: Duplicate Accident IDs found!")

print("\nBasic validation passed")

print("\n" + "=" * 60)
print("Cleaning existing warehouse data...")
print("=" * 60)

cursor.execute("DELETE FROM FactAccident;")

cursor.execute("""
    DELETE FROM DimLocation;
""")

cursor.execute("""
    DELETE FROM DimWeatherCondition
    WHERE WeatherConditionKey <> 1;
""")

cursor.execute("""
    DBCC CHECKIDENT ('DimLocation', RESEED, 0);
""")

cursor.execute("""
    DBCC CHECKIDENT ('DimWeatherCondition', RESEED, 1);
""")

conn.commit()

print("Warehouse cleaned successfully")

location_cols = [
    "State",
    "City",
    "County",
    "Street",
    "Zipcode",
    "Timezone"
]

for col in location_cols:
    df[col] = (
        df[col]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

print("\n" + "=" * 60)
print("Loading DimLocation...")
print("=" * 60)

locations = (
    df[location_cols]
    .drop_duplicates()
    .reset_index(drop=True)
)

print(f"Unique locations: {len(locations):,}")

location_insert_sql = """
INSERT INTO DimLocation
(
    State,
    City,
    County,
    Street,
    Zipcode,
    Timezone
)
VALUES (?, ?, ?, ?, ?, ?)
"""

location_data = list(
    locations[location_cols].itertuples(
        index=False,
        name=None
    )
)

cursor.fast_executemany = True

cursor.executemany(
    location_insert_sql,
    location_data
)

conn.commit()

print("DimLocation loaded successfully")

print("\nCreating LocationKey mapping...")

locations["LocationKey"] = range(
    1,
    len(locations) + 1
)

def create_location_join_key(dataframe):
    return (
        dataframe["State"].astype(str) + "|" +
        dataframe["City"].astype(str) + "|" +
        dataframe["County"].astype(str) + "|" +
        dataframe["Street"].astype(str) + "|" +
        dataframe["Zipcode"].astype(str) + "|" +
        dataframe["Timezone"].astype(str)
    )

df["LocationJoinKey"] = create_location_join_key(df)

locations["LocationJoinKey"] = create_location_join_key(
    locations
)

location_mapping = dict(
    zip(
        locations["LocationJoinKey"],
        locations["LocationKey"]
    )
)

df["LocationKey"] = (
    df["LocationJoinKey"]
    .map(location_mapping)
)

missing_location = df["LocationKey"].isna().sum()

print(f"Missing LocationKey: {missing_location}")

if missing_location > 0:
    print("\nMissing Location Examples:")

    print(
        df.loc[
            df["LocationKey"].isna(),
            location_cols
        ]
        .head(20)
        .to_string(index=False)
    )

    raise ValueError(
        f"ERROR: {missing_location} LocationKeys are missing!"
    )

print("LocationKey mapping completed successfully")

print("\n" + "=" * 60)
print("Loading DimWeatherCondition...")
print("=" * 60)

df["Weather_Condition"] = (
    df["Weather_Condition"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

df["Wind_Direction"] = (
    df["Wind_Direction"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

wind_mapping = {
    "CALM": "Calm",
    "Calm": "Calm",
    "S": "South",
    "South": "South",
    "W": "West",
    "West": "West",
    "N": "North",
    "North": "North",
    "E": "East",
    "East": "East",
    "VAR": "Variable",
    "Variable": "Variable"
}

df["Wind_Direction"] = (
    df["Wind_Direction"]
    .replace(wind_mapping)
)

weather = (
    df[
        [
            "Weather_Condition",
            "Wind_Direction"
        ]
    ]
    .drop_duplicates()
    .reset_index(drop=True)
)

weather = weather[
    ~(
        (weather["Weather_Condition"] == "Unknown") &
        (weather["Wind_Direction"] == "Unknown")
    )
].reset_index(drop=True)

print(f"Unique weather conditions: {len(weather):,}")

weather_insert_sql = """
INSERT INTO DimWeatherCondition
(
    Weather_Condition,
    Wind_Direction
)
VALUES (?, ?)
"""

weather_data = list(
    weather[
        [
            "Weather_Condition",
            "Wind_Direction"
        ]
    ].itertuples(
        index=False,
        name=None
    )
)

cursor.fast_executemany = True

if weather_data:
    cursor.executemany(
        weather_insert_sql,
        weather_data
    )

    conn.commit()

print("DimWeatherCondition loaded successfully")

print("\nCreating WeatherConditionKey mapping...")

weather["WeatherConditionKey"] = range(
    2,
    len(weather) + 2
)

def create_weather_join_key(dataframe):
    return (
        dataframe["Weather_Condition"].astype(str)
        + "|"
        + dataframe["Wind_Direction"].astype(str)
    )

df["WeatherJoinKey"] = create_weather_join_key(df)

weather["WeatherJoinKey"] = create_weather_join_key(
    weather
)

weather_mapping = dict(
    zip(
        weather["WeatherJoinKey"],
        weather["WeatherConditionKey"]
    )
)

weather_mapping["Unknown|Unknown"] = 1

df["WeatherConditionKey"] = (
    df["WeatherJoinKey"]
    .map(weather_mapping)
)

missing_weather = (
    df["WeatherConditionKey"]
    .isna()
    .sum()
)

print(
    f"Missing WeatherConditionKey: "
    f"{missing_weather}"
)

if missing_weather > 0:
    print("\nMissing Weather Examples:")

    print(
        df.loc[
            df["WeatherConditionKey"].isna(),
            [
                "Weather_Condition",
                "Wind_Direction"
            ]
        ]
        .head(20)
        .to_string(index=False)
    )

    raise ValueError(
        f"ERROR: {missing_weather} "
        f"WeatherConditionKeys are missing!"
    )

print(
    "WeatherConditionKey mapping completed successfully"
)

print("\n" + "=" * 60)
print("Creating SeverityKey mapping...")
print("=" * 60)

severity_mapping = {
    1: 1,
    2: 2,
    3: 3,
    4: 4
}

df["SeverityKey"] = (
    df["Severity"]
    .map(severity_mapping)
)

missing_severity = (
    df["SeverityKey"]
    .isna()
    .sum()
)

print(
    f"Missing SeverityKey: "
    f"{missing_severity}"
)

if missing_severity > 0:
    raise ValueError(
        f"ERROR: {missing_severity} "
        f"SeverityKeys are missing!"
    )

print("SeverityKey mapping completed successfully")

print("\n" + "=" * 60)
print("Creating DateKey...")
print("=" * 60)

df["Start_Time"] = pd.to_datetime(
    df["Start_Time"],
    errors="coerce"
)

df["DateKey"] = (
    df["Start_Time"]
    .dt.strftime("%Y%m%d")
    .astype("Int64")
)

min_date = df["Start_Time"].min()
max_date = df["Start_Time"].max()

print(f"Start Date: {min_date}")
print(f"End Date  : {max_date}")

date_keys = pd.read_sql_query(
    """
    SELECT DateKey
    FROM DimDate
    """,
    conn
)

valid_date_keys = set(
    date_keys["DateKey"].astype(int)
)

invalid_dates = (
    ~df["DateKey"]
    .astype(int)
    .isin(valid_date_keys)
).sum()

print(
    f"Invalid DateKeys: {invalid_dates}"
)

if invalid_dates > 0:
    raise ValueError(
        f"ERROR: {invalid_dates} invalid DateKeys found!"
    )

print("DateKey validation passed successfully")

print("\n" + "=" * 60)
print("Preparing FactAccident...")
print("=" * 60)

fact = df[
    [
        "ID",
        "DateKey",
        "LocationKey",
        "WeatherConditionKey",
        "SeverityKey",
        "Start_Time",
        "End_Time",
        "Start_Lat",
        "Start_Lng",
        "End_Lat",
        "End_Lng",
        "Distance(mi)",
        "Accident_Duration_Minutes",
        "Temperature(F)",
        "Wind_Chill(F)",
        "Humidity(%)",
        "Pressure(in)",
        "Visibility(mi)",
        "Wind_Speed(mph)",
        "Precipitation(in)",
        "Is_Weekend",
        "Is_Daytime",
        "Has_End_Location",
        "Has_Weather_Data",
        "Infrastructure_Feature_Count",
        "Duration_Category"
    ]
].copy()

fact.rename(
    columns={
        "ID": "AccidentID",
        "Distance(mi)": "Distance_mi",
        "Temperature(F)": "Temperature_F",
        "Wind_Chill(F)": "Wind_Chill_F",
        "Humidity(%)": "Humidity_Percent",
        "Pressure(in)": "Pressure_in",
        "Visibility(mi)": "Visibility_mi",
        "Wind_Speed(mph)": "Wind_Speed_mph",
        "Precipitation(in)": "Precipitation_in"
    },
    inplace=True
)

integer_columns = [
    "DateKey",
    "LocationKey",
    "WeatherConditionKey",
    "SeverityKey",
    "Infrastructure_Feature_Count"
]

for col in integer_columns:
    fact[col] = (
        pd.to_numeric(
            fact[col],
            errors="coerce"
        )
        .astype("Int64")
    )

fact["Start_Time"] = pd.to_datetime(
    fact["Start_Time"],
    errors="coerce"
)

fact["End_Time"] = pd.to_datetime(
    fact["End_Time"],
    errors="coerce"
)

boolean_columns = [
    "Is_Weekend",
    "Is_Daytime",
    "Has_End_Location",
    "Has_Weather_Data"
]

for col in boolean_columns:
    fact[col] = (
        fact[col]
        .fillna(False)
        .astype(bool)
    )

fact = fact.where(
    pd.notnull(fact),
    None
)

fact_data = []

for row in fact.itertuples(
    index=False,
    name=None
):
    converted_row = []

    for value in row:
        if pd.isna(value):
            converted_row.append(None)

        elif hasattr(value, "to_pydatetime"):
            converted_row.append(
                value.to_pydatetime()
            )

        elif hasattr(value, "item"):
            converted_row.append(
                value.item()
            )

        else:
            converted_row.append(value)

    fact_data.append(
        tuple(converted_row)
    )

print("\n" + "=" * 60)
print("Loading FactAccident...")
print("=" * 60)

fact_insert_sql = """
INSERT INTO FactAccident
(
    AccidentID,
    DateKey,
    LocationKey,
    WeatherConditionKey,
    SeverityKey,
    Start_Time,
    End_Time,
    Start_Lat,
    Start_Lng,
    End_Lat,
    End_Lng,
    Distance_mi,
    Accident_Duration_Minutes,
    Temperature_F,
    Wind_Chill_F,
    Humidity_Percent,
    Pressure_in,
    Visibility_mi,
    Wind_Speed_mph,
    Precipitation_in,
    Is_Weekend,
    Is_Daytime,
    Has_End_Location,
    Has_Weather_Data,
    Infrastructure_Feature_Count,
    Duration_Category
)
VALUES
(
    ?, ?, ?, ?, ?,
    ?, ?,
    ?, ?, ?, ?,
    ?,
    ?,
    ?, ?, ?, ?, ?, ?, ?,
    ?, ?,
    ?, ?,
    ?,
    ?
)
"""

cursor.fast_executemany = True

total_rows = len(fact_data)

for start in range(
    0,
    total_rows,
    BATCH_SIZE
):
    end = min(
        start + BATCH_SIZE,
        total_rows
    )

    batch = fact_data[start:end]

    cursor.executemany(
        fact_insert_sql,
        batch
    )

    conn.commit()

    print(
        f"Loaded {end:,} / {total_rows:,}"
    )

print("\nFactAccident loaded successfully")

print("\n" + "=" * 60)
print("FINAL VALIDATION")
print("=" * 60)

tables = [
    "FactAccident",
    "DimLocation",
    "DimWeatherCondition",
    "DimSeverity",
    "DimDate"
]

for table in tables:
    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(
        f"{table:<25} : {count:,}"
    )

cursor.execute(
    "SELECT COUNT(*) FROM FactAccident"
)

fact_count = cursor.fetchone()[0]

if fact_count != 500000:
    raise ValueError(
        f"ERROR: FactAccident contains "
        f"{fact_count:,} rows instead of 500,000!"
    )

print("\nYear Distribution:")

year_query = """
SELECT
    YEAR(Start_Time) AS AccidentYear,
    COUNT(*) AS AccidentCount
FROM FactAccident
GROUP BY YEAR(Start_Time)
ORDER BY AccidentYear
"""

year_result = pd.read_sql_query(
    year_query,
    conn
)

print(
    year_result.to_string(index=False)
)

print("\nSeverity Distribution:")

severity_query = """
SELECT
    DS.Severity,
    COUNT(*) AS AccidentCount
FROM FactAccident FA
INNER JOIN DimSeverity DS
    ON FA.SeverityKey = DS.SeverityKey
GROUP BY DS.Severity
ORDER BY DS.Severity
"""

severity_result = pd.read_sql_query(
    severity_query,
    conn
)

print(
    severity_result.to_string(index=False)
)

print("\nForeign Key Validation:")

fk_checks = {
    "Missing DateKey": """
        SELECT COUNT(*)
        FROM FactAccident FA
        LEFT JOIN DimDate DD
            ON FA.DateKey = DD.DateKey
        WHERE DD.DateKey IS NULL
    """,

    "Missing LocationKey": """
        SELECT COUNT(*)
        FROM FactAccident FA
        LEFT JOIN DimLocation DL
            ON FA.LocationKey = DL.LocationKey
        WHERE DL.LocationKey IS NULL
    """,

    "Missing WeatherConditionKey": """
        SELECT COUNT(*)
        FROM FactAccident FA
        LEFT JOIN DimWeatherCondition DW
            ON FA.WeatherConditionKey =
               DW.WeatherConditionKey
        WHERE DW.WeatherConditionKey IS NULL
    """,

    "Missing SeverityKey": """
        SELECT COUNT(*)
        FROM FactAccident FA
        LEFT JOIN DimSeverity DS
            ON FA.SeverityKey = DS.SeverityKey
        WHERE DS.SeverityKey IS NULL
    """
}

for name, query in fk_checks.items():
    cursor.execute(query)

    count = cursor.fetchone()[0]

    print(
        f"{name:<30} : {count}"
    )

    if count != 0:
        raise ValueError(
            f"ERROR: {name} = {count}"
        )

elapsed = time.time() - start_time

print("\n" + "=" * 60)
print("SQL SERVER LOAD COMPLETED SUCCESSFULLY")
print("=" * 60)

print(
    f"FactAccident rows : {fact_count:,}"
)

print(
    f"Execution time    : {elapsed / 60:.2f} minutes"
)

print("\nAll validations passed successfully")

cursor.close()
conn.close()

print("\nSQL Server connection closed.")