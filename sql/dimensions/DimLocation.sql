USE USAccidentsDW;
GO

IF OBJECT_ID('DimLocation', 'U') IS NOT NULL
    DROP TABLE DimLocation;
GO

CREATE TABLE DimLocation
(
    LocationKey BIGINT IDENTITY(1,1) PRIMARY KEY,
    State VARCHAR(10) NULL,
    City VARCHAR(100) NULL,
    County VARCHAR(100) NULL,
    Street VARCHAR(200) NULL,
    Zipcode VARCHAR(20) NULL,
    Timezone VARCHAR(50) NULL
);
GO