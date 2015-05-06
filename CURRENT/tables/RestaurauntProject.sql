CREATE TABLE Raters (
UserId     INTEGER      PRIMARY KEY,
Email      VARCHAR(60)  UNIQUE, 
Password   VARCHAR(30),
RName      VARCHAR(35)  ,   
Join_Date  DATE         DEFAULT NOW(),  --Added timestamp
Type       CHAR(20),
Reputation INTEGER      DEFAULT 1,
Thumbnail  VARCHAR(300),
CONSTRAINT Reputation   CHECK (Reputation > 0 AND Reputation <= 5)
);



CREATE TABLE Restaurants (
RestaurantId INTEGER     PRIMARY KEY,
Name         VARCHAR(120) NOT NULL, 
Cost         INTEGER,
FoodRating   INTEGER,
PriceRating  INTEGER, 
MoodRating   INTEGER, 
StaffRating  INTEGER, 
URL          VARCHAR(200),

CONSTRAINT valid_ratingf CHECK (0 <= FoodRating  AND FoodRating  <= 100), 
CONSTRAINT valid_ratingp CHECK (0 <= PriceRating AND PriceRating <= 100), 
CONSTRAINT valid_ratingm CHECK (0 <= MoodRating  AND MoodRating  <= 100), 
CONSTRAINT valid_ratings CHECK (0 <= StaffRating AND StaffRating <= 100), 
CONSTRAINT valid_cost    CHECK (0 <= Cost   AND Cost   <= 4  ) 
);


CREATE TABLE Cuisines (
Cuisine       VARCHAR(50),
RestaurantId  INTEGER   REFERENCES Restaurants
);

CREATE TABLE Features (
FeatureName   VARCHAR(50),
RestaurantId  INTEGER   REFERENCES Restaurants
);


CREATE TABLE Ratings (
UserId       INTEGER        REFERENCES Raters, 
Rating_Date  DATE           DEFAULT    NOW(),   --Added timestamp
Food         INTEGER,
Price        INTEGER, 
Mood         INTEGER, 
Staff        INTEGER, 
Title        VARCHAR(500),
Comment      VARCHAR(10000),
RestaurantId INTEGER   REFERENCES   Restaurants, 
-- CONSTRAINT Rating_pkey PRIMARY KEY (UserId, Rating_Date, RestaurantId),  
CONSTRAINT FInterval   CHECK (Food  >= 0 AND Food  <= 100),  -- changed equalities
CONSTRAINT PInterval   CHECK (Price >= 0 AND Price <= 100),  -- changed equalities
CONSTRAINT MInterval   CHECK (Mood  >= 0 AND Mood  <= 100),  -- changed equalities
CONSTRAINT SInterval   CHECK (Staff >= 0 AND Staff <= 100)   -- changed equalities
);



CREATE TABLE Locations (
LocationId       INTEGER,
First_open_date  DATE, 
Manager_name     VARCHAR(70), 
Phone            VARCHAR(14), 
Street_address   VARCHAR(80), 
Thumbnail        VARCHAR(300),

Monday           VARCHAR(50),
Tuesday          VARCHAR(50),
Wednesday        VARCHAR(50),
Thursday         VARCHAR(50),
Friday           VARCHAR(50),
Saturday         VARCHAR(50),
Sunday           VARCHAR(50),

RestaurantId     INTEGER  REFERENCES Restaurants,
Neighbourhood    VARCHAR(60),
CONSTRAINT Location_pkey PRIMARY KEY (LocationId, RestaurantId)
);



CREATE TABLE MenuItems (
RestaurantId   INTEGER       REFERENCES Restaurants,
Thumbnail      VARCHAR(200),
Name           VARCHAR(140)  NOT NULL
--CONSTRAINT menu_pkey PRIMARY KEY (RestaurantID, Name)
);


/*
CREATE TABLE RatingItems (
UserId     INTEGER         REFERENCES Raters,
RI_Date    DATE, 
ItemId     INTEGER         REFERENCES MenuItems,
Rating     INTEGER, 
Comment    VARCHAR(700),
CONSTRAINT RatingItem_pkey PRIMARY KEY (UserId, RI_Date, ItemId),
CONSTRAINT Rat             CHECK       (Rating > 0 AND Rating <= 5)  -- changed equalities
);
*/


/*
CREATE TABLE Images (
ImgName VARCHAR(200)   PRIMARY KEY,
Img     VARCHAR()
);
*/
