-- DDL SQL Statements for Milestone 2, from ER based on Appendix A,

-- COMPLETE:
CREATE TABLE Business (
  id CHAR(22),
  name VARCHAR(90), -- 90 varchar because names of businesses could be long, I believe.
  streetAddress	VARCHAR(40),
  city	VARCHAR(20),
  state	VARCHAR(2), -- Put down as two for AK, AR state abbreviations.
  zipcode, CHAR(5)
  numReviews INT,
  numCheckins INT,
  reviewRating FLOAT,
  businessStars INT,
  CHECK (reviewRating <= 5), -- If you want to check that businesses must be less than or equal to 5 stars.
  PRIMARY KEY (id)
);

CREATE TABLE Checkins (
  business CHAR(22),
  datetime DATETIME,
  count INT,
  PRIMARY KEY (buisness, datetime),
  FOREIGN KEY (buisness) REFERENCES Business(id)
);

CREATE TABLE Attributes (
  business CHAR(22),
  attributeName VARCHAR(50),
  attributeValue BOOLEAN,
  PRIMARY KEY (buisness, attributeName),
  FOREIGN KEY (buisness) REFERENCES Business(id)
);

CREATE TABLE Categories (
  business CHAR(22),
  category VARCHAR(50),
  PRIMARY KEY (buisness, category),
  FOREIGN KEY (buisness) REFERENCES Business(id)
);

CREATE TABLE Reviews (
  id CHAR(22),
  starRating INT,
  date DATE, 
  text VARCHAR(200),
  voteType VARCHAR(10),
  PRIMARY KEY (id)
)

CREATE TABLE Rating (
  review CHAR(22),
  business CHAR(22),
  FOREIGN KEY (review) REFERENCES Reviews(id),
  FOREIGN KEY (business) REFERENCES Business(id),
  Primary Key (review)
);
