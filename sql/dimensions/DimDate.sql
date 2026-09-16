USE USAccidentsDW;
GO

IF OBJECT_ID('DimDate', 'U') IS NOT NULL
    DROP TABLE DimDate;
GO

CREATE TABLE DimDate
(
    DateKey INT PRIMARY KEY,
    FullDate DATE NOT NULL,
    Year INT NOT NULL,
    Quarter INT NOT NULL,
    Month INT NOT NULL,
    MonthName VARCHAR(20) NOT NULL,
    Day INT NOT NULL,
    DayName VARCHAR(20) NOT NULL,
    DayOfWeekNumber INT NOT NULL,
    IsWeekend BIT NOT NULL,
    Season VARCHAR(20) NOT NULL
);
GO