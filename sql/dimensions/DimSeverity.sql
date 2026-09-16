USE USAccidentsDW;
GO

IF OBJECT_ID('DimSeverity', 'U') IS NOT NULL
    DROP TABLE DimSeverity;
GO

CREATE TABLE DimSeverity
(
    SeverityKey INT IDENTITY(1,1) PRIMARY KEY,
    Severity INT NOT NULL,
    SeverityDescription VARCHAR(50) NOT NULL
);
GO

INSERT INTO DimSeverity
(
    Severity,
    SeverityDescription
)
VALUES
(1, 'Low'),
(2, 'Moderate'),
(3, 'High'),
(4, 'Severe');
GO