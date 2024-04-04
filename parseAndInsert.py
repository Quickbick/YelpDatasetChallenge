import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def insert2BusinessTable():
    #reading the JSON file
    with open('yelp_business.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
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
                      str(data["review_count"]) + "," + "0" + "," + str(data["stars"]) + ");"
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
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()


insert2BusinessTable()