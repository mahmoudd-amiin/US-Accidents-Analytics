USE USAccidentsDW;
GO

IF OBJECT_ID('DimWeatherCondition', 'U') IS NOT NULL
    DROP TABLE DimWeatherCondition;
GO

CREATE TABLE DimWeatherCondition
(
    WeatherConditionKey INT IDENTITY(1,1) PRIMARY KEY,
    Weather_Condition VARCHAR(150) NOT NULL,
    Wind_Direction VARCHAR(30) NOT NULL
);
GO

INSERT INTO DimWeatherCondition
(
    Weather_Condition,
    Wind_Direction
)
VALUES
('Unknown', 'Unknown');
GO