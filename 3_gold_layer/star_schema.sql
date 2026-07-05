-- ==========================================
-- Gold Layer: Star Schema for Airbnb Market
-- ==========================================

-- 1. Create Dimension: Location
CREATE TABLE Dim_Location (
    LocationID INT PRIMARY KEY,
    City VARCHAR(100),
    Country VARCHAR(100),
    Latitude DECIMAL(10, 6),
    Longitude DECIMAL(10, 6)
);

-- 2. Create Dimension: Property
CREATE TABLE Dim_Property (
    PropertyID INT PRIMARY KEY,
    Room_Type VARCHAR(50),
    Property_Type VARCHAR(50),
    Accommodates INT
);

-- 3. Create Dimension: Host
CREATE TABLE Dim_Host (
    HostID INT PRIMARY KEY,
    Host_Name VARCHAR(100),
    Host_Response_Time VARCHAR(50),
    Host_Is_Superhost BOOLEAN
);

-- 4. Create Fact Table: Listings (The Core Data)
CREATE TABLE Fact_Listings (
    ListingID INT PRIMARY KEY,
    LocationID INT,
    PropertyID INT,
    HostID INT,
    Price DECIMAL(10, 2),
    Minimum_Nights INT,
    Number_Of_Reviews INT,
    Review_Scores_Rating DECIMAL(3, 2),
    FOREIGN KEY (LocationID) REFERENCES Dim_Location(LocationID),
    FOREIGN KEY (PropertyID) REFERENCES Dim_Property(PropertyID),
    FOREIGN KEY (HostID) REFERENCES Dim_Host(HostID)
);

-- Note: Data loading commands (e.g., COPY INTO or INSERT) will follow based on the specific RDBMS (like Snowflake or PostgreSQL) used in deployment.