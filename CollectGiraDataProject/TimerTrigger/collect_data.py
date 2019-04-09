import requests
import psycopg2
from datetime import datetime
import pytz
import json


def get_requests(json_requests):
    with open(json_requests) as json_file:  
        dic_xhr = json.load(json_file)
    return dic_xhr


def get_db_credentials(json_db_credentials):
    with open(json_db_credentials) as json_file:  
        dic_db_cred = json.load(json_file)
    return dic_db_cred


def get_connection(credentials):
    conn = psycopg2.connect(dbname=credentials["dbname"], 
                            user=credentials["user"], 
                            host=credentials["host"], 
                            password=credentials["password"])
    return conn
    

def insert_data(new_entries, conn):
    query = "INSERT INTO dev.fact_gira_data (datetime, GIRA_STATION_ID, NUM_BIKES, NUM_DOCKINGS, STATION_STATE) VALUES (%s, %s, %s, %s, %s);"
    cursor = conn.cursor()
    for entry in new_entries:
        cursor.execute(query,(datetime.now(tz=pytz.timezone("Europe/Lisbon")),
                                    entry["station_id"],
                                    entry["num_bicicletas"],
                                    entry["num_docas"],
                                    entry["estado"]))
    conn.commit()

    
def get_data(request):
    response = requests.get(request)
    print(f"Request status code {response.status_code}")
    if response.status_code == 200:
        data = response.json()
    else:
        print("WARNING: Status code not 200 therefore skipping.")
    return data


def process_response(response):
    db_entries = []
    for station_resp in response['features']:
        properties = station_resp['properties']
        new_entry = {'station_id':int(properties['id_expl']),
                    'num_bicicletas':int(properties['num_bicicletas']),
                    'num_docas':int(properties['num_docas']),
                    'estado':properties['estado']}
        db_entries.append(new_entry)
    return db_entries


def run_my_app():
    dic_xhr = get_requests("requests.json")
    dic_db_cred = get_db_credentials("db_credentials.json")
    # get data from GIRA
    data = get_data(dic_xhr["entrecampos"])

    # process result
    db_new_entries = process_response(data)

    # get db connection
    conn = get_connection(dic_db_cred)

    # insert new entries into db
    insert_data(db_new_entries, conn)

    # close connection
    conn.close()

    return 0

run_my_app()