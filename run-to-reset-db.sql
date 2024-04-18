psql -U postgres
12345
\c milestone2db

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE Business (
  id CHAR(22),
  name VARCHAR(90),
  street_add VARCHAR(100),
  city VARCHAR(20),
  state VARCHAR(2),
  zipcode CHAR(5),
  stars FLOAT,
  num_reviews INT,
  num_checkins INT,
  review_rating FLOAT,
  CHECK (review_rating <= 5),
  PRIMARY KEY (id)
);

CREATE TABLE Checkins (
  business CHAR(22),
  time TIME,
  day VARCHAR(9),
  count INT,
  PRIMARY KEY (business, day, time),
  FOREIGN KEY (business) REFERENCES Business(id)
);

CREATE TABLE Attributes (
  business CHAR(22),
  attribute_name VARCHAR(50),
  attribute_value VARCHAR(20),
  PRIMARY KEY (business, attribute_name),
  FOREIGN KEY (business) REFERENCES Business(id)
);

CREATE TABLE Categories (
  business CHAR(22),
  category VARCHAR(50),
  PRIMARY KEY (business, category),
  FOREIGN KEY (business) REFERENCES Business(id)
);

CREATE TABLE Reviews (
  id CHAR(22),
  star_rating INT,
  date DATE, 
  useful INT,
  funny INT,
  cool INT,
  PRIMARY KEY (id)
);

CREATE TABLE Rating (
  review CHAR(22),
  business CHAR(22),
  FOREIGN KEY (review) REFERENCES Reviews(id),
  FOREIGN KEY (business) REFERENCES Business(id),
  Primary Key (review)
);


--PAUSE HERE TO RUN PARSER

CREATE TEMP TABLE BusinessAggregates AS
SELECT
    b.id AS BusinessID,
    COALESCE(SUM(c.count), 0) AS numCheckins,
    COUNT(r.id) AS reviewCount,
    COALESCE(ROUND(AVG(r.star_rating), 1), 0) AS reviewrating
FROM
    Business b
LEFT JOIN Checkins c ON b.id = c.business
LEFT JOIN Rating ra ON b.id = ra.business
LEFT JOIN Reviews r ON ra.review = r.id
GROUP BY
    b.id;

UPDATE Business
SET
    num_checkins = bagg.numCheckins,
    num_reviews = bagg.reviewCount,
    review_rating = bagg.reviewrating
FROM
    BusinessAggregates bagg
WHERE
    Business.id = bagg.BusinessID;

DROP TABLE IF EXISTS BusinessAggregates;