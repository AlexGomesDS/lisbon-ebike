import requests
import psycopg2
import datetime
import json

dbname = "postgres"
user = "admin_2"
password = "123QWEasd"
host = "lx-ebikes-db.cd38uezioab8.eu-west-1.rds.amazonaws.com"


def get_connection():
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password)
    return conn
    

def insert_data(json_data, conn):
    query = "INSERT INTO dev.bike_data (data, created_date) VALUES (%s, %s);"
    bd_data = (json.dumps(data), datetime.datetime.now())

    cursor = conn.cursor()
    cursor.execute(query, bd_data)
    conn.commit()


def get_data():
    url = "http://www.findabike.de/api?lat=38.731410&lon=-9.146416"
    url = "http://www.google.com"
    #response = requests.get(url, headers={"X-Authorization-Token":"GfOE30DAJ0IVFa6a4I0kZ6iZolB7M6di"})
    response = requests.get(url)
    print(response.status_code)
	#data = response.json()
    return data
    

def lambda_handler(event, context):
    #test_connection()
    get_data()
    return 0
