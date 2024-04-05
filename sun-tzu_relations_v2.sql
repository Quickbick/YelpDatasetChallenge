-- DDL SQL Statements for Milestone 2, from ER based on Appendix A,
CREATE TABLE Business (
  id CHAR(22),
  name VARCHAR(90),
  street_add VARCHAR(100),
  city VARCHAR(20),
  state VARCHAR(2),
  zipcode CHAR(5),
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
  useful INT,  -- Changed from vote_type VARCHAR(10), added in v3.
  funny INT,   -- Added (v3)
  cool INT,    -- Added (v3)
  PRIMARY KEY (id)
);

CREATE TABLE Rating (
  review CHAR(22),
  business CHAR(22),
  FOREIGN KEY (review) REFERENCES Reviews(id),
  FOREIGN KEY (business) REFERENCES Business(id),
  Primary Key (review)
);

INSERT INTO Rating (review, business) VALUES ('dwQEZBFen2GdihLLfWeexA','ClgrKJ6dqiM7vSKJBJ2w6Q');