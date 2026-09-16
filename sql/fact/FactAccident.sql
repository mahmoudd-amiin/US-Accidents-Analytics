USE USAccidentsDW;
GO

IF OBJECT_ID('FactAccident', 'U') IS NOT NULL
    DROP TABLE FactAccident;
GO

CREATE TABLE FactAccident
(
    AccidentKey BIGINT IDENTITY(1,1) NOT NULL,
    AccidentID VARCHAR(50) NOT NULL,

    DateKey INT NOT NULL,
    LocationKey BIGINT NOT NULL,
    WeatherConditionKey INT NOT NULL,
    SeverityKey INT NOT NULL,

    Start_Time DATETIME2 NULL,
    End_Time DATETIME2 NULL,

    Start_Lat DECIMAL(10,7) NULL,
    Start_Lng DECIMAL(10,7) NULL,
    End_Lat DECIMAL(10,7) NULL,
    End_Lng DECIMAL(10,7) NULL,

    Distance_mi DECIMAL(10,3) NULL,
    Accident_Duration_Minutes DECIMAL(12,2) NULL,

    Temperature_F DECIMAL(7,2) NULL,
    Wind_Chill_F DECIMAL(7,2) NULL,
    Humidity_Percent DECIMAL(6,2) NULL,
    Pressure_in DECIMAL(8,3) NULL,
    Visibility_mi DECIMAL(8,2) NULL,
    Wind_Speed_mph DECIMAL(8,2) NULL,
    Precipitation_in DECIMAL(8,3) NULL,

    Is_Weekend BIT NULL,
    Is_Daytime BIT NULL,
    Has_End_Location BIT NULL,
    Has_Weather_Data BIT NULL,

    Infrastructure_Feature_Count INT NULL,

    Duration_Category VARCHAR(30) NULL,

    CONSTRAINT PK_FactAccident
        PRIMARY KEY CLUSTERED (AccidentKey),

    CONSTRAINT FK_FactAccident_DimDate
        FOREIGN KEY (DateKey)
        REFERENCES DimDate(DateKey),

    CONSTRAINT FK_FactAccident_DimLocation
        FOREIGN KEY (LocationKey)
        REFERENCES DimLocation(LocationKey),

    CONSTRAINT FK_FactAccident_DimWeather
        FOREIGN KEY (WeatherConditionKey)
        REFERENCES DimWeatherCondition(WeatherConditionKey),

    CONSTRAINT FK_FactAccident_DimSeverity
        FOREIGN KEY (SeverityKey)
        REFERENCES DimSeverity(SeverityKey)
);
GO