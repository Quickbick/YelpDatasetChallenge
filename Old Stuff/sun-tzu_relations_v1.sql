-- DDL SQL Statements for Milestone 1, from ER based on Appendix A,

-- COMPLETE:
CREATE TABLE Business (
  business_name	varchar(90), -- 90 varchar because names of businesses could be long, I believe.
  star_rating		FLOAT, -- OR, INT if its supposted to be like 0, 1, 2, 3, 4, or 5 and no other (4.5) decimal options.
  address	varchar(70), -- If we want this to be a string that represents all of address, then this could be used. We'll decide nearer Milestone 2.
  street	varchar(40),
  city		varchar(20),
  state		varchar(2), -- Put down as two for AK, AR state abbreviations.
  reviews_count	int,
  checkins_count int,
  CHECK (star_rating <= 5), -- If you want to check that businesses must be less than or equal to 5 stars.
  Primary Key (business_name, street, city)
);

-- COMPLETE:
CREATE TABLE Determines_Rating_Of ( -- Many-to-one so we're going to keep star rating as primary key
  star_rating	FLOAT, -- Could be int if 3.5 and 4.2 are not allowed, and 0, 1, 2, 3, 4, 5 are wanted only.
  average_star_rating	FLOAT,
  business_name VARCHAR(90), -- To keep from giving "error:  unknown column "business_name" in foreign key definition"
  -- content varchar(300) ( If there's supposted to be review content like a description of the review speech, then have this here. If not, and we're only worried about ratings from Appendix A, then star rating will do.
  FOREIGN KEY (business_name) REFERENCES Business(business_name),
  Primary Key (star_rating)
);

-- COMPLETE:
CREATE TABLE Displayed_As ( -- Many-to-one as well here
  business_name VARCHAR(90),
  businesses_in_category_list VARCHAR(90), -- The names of the businesses fit into a list. Each business has a name of max 90 length.
  FOREIGN KEY (business_name) REFERENCES Business(business_name),
  FOREIGN KEY (businesses_in_category_list) REFERENCES Search_Result(businesses_in_category_list),
  PRIMARY KEY (business_name)
);

-- COMPLETE:
CREATE TABLE Search_Result (
  businesses_in_category_list VARCHAR(90), -- Assuming businesses are listed by name, max 90 characters..... This is NO LONGER a set to hopefully hold multiple businesses at once. 
  Primary Key (businesses_in_category_list)
);

-- COMPLETE:
CREATE TABLE Search_By_Selected (
  business_category varchar(25), -- Category of business, so like a small string.
  business_name VARCHAR(90), -- The name of the business selected
  name_login_id VARCHAR(100), -- Assuming user login ID
  state VARCHAR(2), -- State abbreviation
  city VARCHAR(35), -- City name
  businesses_in_category_list VARCHAR(90), -- Assuming a list of businesses
  FOREIGN KEY (businesses_in_category_list) REFERENCES Search_Result(businesses_in_category_list),
  FOREIGN KEY (name_login_id) REFERENCES User(name_login_id), -- Name/login/id is a holder for what the primary key of the User class would be. This hasn't been gone into depth in Milestone 1, so name-login-id is kind of a holder for that until later.
  FOREIGN KEY (state, city) REFERENCES Selected_Location(state, city),
  Primary Key (businesses_in_category_list, name_login_id, state, city, business_category)
);

-- COMPLETE:
CREATE TABLE Populates (
  state VARCHAR(2),
  city VARCHAR(35),
  zipcode VARCHAR(5),
  FOREIGN KEY (state, city) REFERENCES Selected_Location(state, city),
  FOREIGN KEY (zipcode) REFERENCES Zipcode(zipcode)
);

-- COMPLETE:
CREATE TABLE User (
  name_login_id VARCHAR(100), -- Generic attribute for holding primary key of User. It isn't specified in Milestone 1, so name/login/id can be assumed as what's being used from our User class, which interacts with Refreshing and Displaying relationship elements.  
  -- (Here we are assuming the data type is VARCHAR with a maximum length of 100 characters, subject to change in upcoming Milestones)
  Primary Key (name_login_id)
);

-- COMPLETE:
CREATE TABLE Selected_Location (
  state varchar(2),
  city varchar(35),
  Primary Key (state, city)
);

-- COMPLETE:
CREATE TABLE Zipcode (
  zipcode INT, -- See below for deviding if zip should be an int or varchar + why.
  -- WAS: zipcode varchar(5), -- I put as varchar 5 so it can be 5-digit strings as zips. If I'm misunderstanding zips from beyond my local area, and they can be beyond 5 chars, just make it an int. However, if things like 98074, varchar(5) could work... OR, an int and a CHECK clause at the end of the length of the numbers could work either if that's found to be better to implement in Milestone 2
  PRIMARY KEY (zipcode)
);

-- COMPLETE:
CREATE TABLE Displays_On_Select (
  average_income FLOAT, -- Provided
  total_population int, -- Provided
  businesses_within_zipcode int, -- Search in a future milestone, I believe.
  name_login_id VARCHAR(100), -- Assuming user login ID
  zipcode INT,
  FOREIGN KEY (name_login_id) REFERENCES User(name_login_id),
  FOREIGN KEY (zipcode) REFERENCES Zipcode(zipcode),
  Primary Key (name_login_id, zipcode)
);

-- COMPLETE:
CREATE TABLE Refreshes (
  business_name VARCHAR(90),
  name_login_id VARCHAR(100),
  business_list VARCHAR(90), -- Assuming the datatype of business_list is SET, but postgre doesn't have SET so column of varchars representing lists of buisnesses is fine I believe.
  FOREIGN KEY (business_name) REFERENCES Business(business_name),
  FOREIGN KEY (name_login_id) REFERENCES User(name_login_id),
  PRIMARY KEY (business_name)
);

-- ALL DDL SQLs CHECKED+COMPILE. GOOD FOR REVIEW NOW.
CREATE TABLE Zipcode_List (
  business_list VARCHAR(90), -- Holds all possible businesses as a set, not just successful or popularly-ranked ones
  popular_businesses_set VARCHAR(90),
  successful_businesses_set VARCHAR(90),
  -- Below, I put foreign keys to these because this is an ISA
  FOREIGN KEY (popular_businesses_set) REFERENCES Zipcode_List(business_list), -- This one gets a little weird. Trying to do subclass/superclass structure ER Model -> Relational for an ISA relationship.....
  FOREIGN KEY (successful_businesses_set) REFERENCES Zipcode_List(business_list),
  Primary Key (business_list)
  -- Note: does not represent a total constraint because ER Approach with partial participation.
);
