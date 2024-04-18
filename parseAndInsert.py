import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

#complete
def insert2BusinessTable():
    #reading the JSON file
    with open('yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='12345'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            sql_str = "INSERT INTO business (id, name, street_add, city, state, zipcode, num_reviews, num_checkins, review_rating) " \
                      "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(data["name"]) + "','" + cleanStr4SQL(data["address"]) + "','" + \
                      cleanStr4SQL(data["city"]) + "','" + cleanStr4SQL(data["state"]) + "','" + cleanStr4SQL(data["postal_code"]) + "'," + \
                      str(data["review_count"]) + "," + '0' + "," + str(data["stars"]) + ");"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to businessTABLE failed!")
            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

#complete
def insert2CheckinTable():
    #reading the JSON file
    with open('yelp_checkin.JSON','r') as f:
        line = f.readline()
        count_line = 0
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='12345'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            for item in data['time']:
                day = item
                for item2 in data['time'][day]:
                    time = item2
                    count = data['time'][day][time]
                    sql_str = "INSERT INTO Checkins (business, day, time, count) " \
                        "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(day) + "','" +\
                        cleanStr4SQL(time) + "','" + str(count) + "');"
                    try:
                        cur.execute(sql_str)
                    except:
                        print("Insert to CheckinTABLE failed!")
                    conn.commit()
            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

def insert2AttributesTable():
    #reading the JSON file
    with open('yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='12345'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            for item in data['attributes']:
                if (isinstance(data['attributes'][item], dict)):
                    for nestItem in data['attributes'][item]:
                        newItem = item + " " + nestItem
                        value = data['attributes'][item][nestItem]
                        sql_str = "INSERT INTO Attributes (business, attribute_name, attribute_value) " \
                            "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(newItem) + "','" + cleanStr4SQL(str(value)) + "');"
                    try:
                        cur.execute(sql_str)
                    except:
                        print("Insert to attributesTABLE failed!")
                    conn.commit() 
                else:
                    value = data['attributes'][item]
                    sql_str = "INSERT INTO Attributes (business, attribute_name, attribute_value) " \
                            "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(item) + "','" + cleanStr4SQL(str(value)) + "');"
                    try:
                        cur.execute(sql_str)
                    except:
                        print("Insert to attributesTABLE failed!")
                    conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

#complete
def insert2CategoryTable():
    #reading the JSON file
    with open('yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='12345'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            for item in data['categories']:
                sql_str = "INSERT INTO Categories (business, category) " \
                        "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(item) + "');"
                try:
                    cur.execute(sql_str)
                except:
                    print("Insert to CategoryTABLE failed!")
                conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

# [NOTE]: Tried to base it off the complete ones, using 'yelp_review.JSON', but still having trouble connecting to database through here, so can't run tests yet.
def insert2ReviewTable():
    # Reading the JSON file
    with open('yelp_review.JSON', 'r') as f:
        line = f.readline()
        count_line = 0
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='12345'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            sql_str = "INSERT INTO Reviews (id, star_rating, date, useful, funny, cool) " \
                      "VALUES ('" + cleanStr4SQL(data['review_id']) + "'," + str(data["stars"]) + ",'" + \
                      cleanStr4SQL(data["date"]) + "'," + \
                      str(data["useful"]) + "," + str(data["funny"]) + "," + str(data["cool"]) + ");"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to Reviews table failed!")
            conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

def insert2RatingTable():
    #reading the JSON file
    with open('yelp_review.JSON','r') as f:
        line = f.readline()
        count_line = 0
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='12345'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            sql_str = "INSERT INTO Rating (review, business) " \
                "VALUES ('" + cleanStr4SQL(data['review_id']) + "','" + cleanStr4SQL(data['business_id']) + "');"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to RatingTABLE failed!")
            conn.commit()
            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()


# Calls section:
insert2BusinessTable()
insert2CheckinTable()
insert2AttributesTable()
insert2CategoryTable()
insert2ReviewTable()
insert2RatingTable()