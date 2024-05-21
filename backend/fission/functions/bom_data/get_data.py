'''
Team 77:
Name: Hanchun Pan Student ID: 1266219, Email: hanchunp@student.unimelb.edu.au 
Name: Kaiyuan Cui Student ID: 1266180 , Email: kaicui@student.unimelb.edu.au 
Name: Runyu Yang Student ID: 1118665, Email: runyuy@student.unimelb.edu.au 
Name: Yaotian Wang  Student ID: 1503936, Email: yaotwang@student.unimelb.edu.au 
Name: Zhenghan Zhang Student ID: 1136448, Email: zhenghanz1@student.unimelb.edu.au 
'''

import json, requests
from elasticsearch8 import Elasticsearch, helpers
import pandas as pd
import requests
from flask import current_app, request
from pathlib import Path
from io import StringIO

INDEX_NAME = 'bom'
LOCAL_DEV = False
UPLOAD = True
#BASE_PATH = Path(__file__).parent
#STATIONS_LIST = (BASE_PATH /'stations_list.csv').resolve()

ES_URL = 'https://localhost:9200' if LOCAL_DEV else 'https://elasticsearch-master.elastic.svc.cluster.local:9200'
EMPTY_QUERY = {
        "query": {
            "match_all": {}
        }
    }

def config(k):
    if LOCAL_DEV:
        return 'elastic'
   
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

# Establish connection to Elasticsearch
client = Elasticsearch(
    ES_URL,
    verify_certs=False,
    ssl_show_warn=False,
    basic_auth=(config('ES_USERNAME'), config('ES_PASSWORD'))
)


def scan_from_es(index_name, query):
    '''
    return the response from Elastic Search as an Iterable[Dict[str, Any]]
    
    '''
    try:
        # Fetch all documents from the index based on the query
        response = helpers.scan(client, index=index_name, query=query)
        return response
    
    except Exception as e:
        # Handle errors (e.g., index does not exist, connection issues)
        return {"error": str(e)}  # Return an empty DataFrame


def dataframe_from_es(index_name, query):
    '''
    return the response from Elastic Search as a pandas dataframe
    
    '''
    try:
        # Fetch all documents from the index based on the query
        #response = helpers.scan(client, index=index_name, query=query)

        response = scan_from_es(index_name, query)
        docs = list(response)
        
        # Extract the _source field from each document
        data = [doc['_source'] for doc in docs]
        
        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        # Handle errors (e.g., index does not exist, connection issues)

        print(e)
        return pd.DataFrame()  # Return an empty DataFrame


# gets the raw stations list, unused at the moment due to its size
def extract_station_list():
    url = 'https://reg.bom.gov.au/climate/data/lists_by_element/stations.txt'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('utf-8')
    else:
        raise Exception("Data Download Fail, Status Code:" + str(response.status_code))

    lines = data.splitlines()[2:]
    data_rows = []
    for line in lines:
        if line.strip() and not line.startswith('-------'):
            # extract each column data 
            site = line[0:7].strip()
            dist = line[7:13].strip()
            site_name = line[13:57].strip()
            start = line[57:64].strip()
            end = line[64:71].strip()
            lat = line[71:80].strip()
            lon = line[80:89].strip()
            source = line[89:104].strip()
            sta = line[104:108].strip()
            height = line[108:120].strip()
            bar_ht = line[120:129].strip()
            wmo = line[129:135].strip()

            # Add data into column list
            data_rows.append([site, dist, site_name, start, end, lat, lon, source, sta, height, bar_ht, wmo])

    # Create Dataframe
    columns = ["Site", "Dist", "Site name", "Start", "End", "Lat", "Lon", "Source", "STA", "Height (m)", "Bar_ht", "WMO"]
    df = pd.DataFrame(data_rows, columns=columns)

    column_list = ['Site name', 'Lat', 'Lon', 'STA', 'WMO']

    filtered_df = df[df['WMO'].notna()].reset_index(drop=True)
    filtered_df = filtered_df[filtered_df['WMO'].astype(str).str.match(r'^\d{5}$')].reset_index(drop=True)
    filtered_df = filtered_df[~filtered_df['End'].astype(str).str.match(r'^\d{4}$')].reset_index(drop=True)
    final_station_list = filtered_df[column_list]
    return final_station_list

# Uplaod to Elastic Search
def upload_es(index_name:str, data:pd.DataFrame) -> bool:
    # request settings:
    url =''
    if LOCAL_DEV:
        url = 'https://localhost:9200'
    else:
        url = 'https://elasticsearch-master.elastic.svc.cluster.local:9200'


    headers = {'Content-Type': 'application/json'}
    auth = ('elastic', 'elastic')
    requests.packages.urllib3.disable_warnings()
    verify_ssl = False
    index_url = url + '/' + index_name + '/_bulk'

    actions = []
    for index, row in data.iterrows():
        doc_id = row['name'] + row['local_date_time_full'] # assume unique
        # print(doc_id)
        # print("________________")
        # doc_id = doc_id[:20]
        
        payload = row.to_dict()

        for key, value in payload.items():
            if pd.isna(value):
                payload[key] = None
        action = {'index': {'_id': doc_id}}
        actions.append(json.dumps(action))
        actions.append(json.dumps(payload))

    try:
        response = requests.post(index_url, data='\n'.join(actions) + '\n', headers=headers, auth=auth, verify=verify_ssl)
        if LOCAL_DEV:
            print(f'Status Code: {response.status_code}')
            print(response.json())
        else:
            current_app.logger.info(f'Status Code: {response.status_code}')
            current_app.logger.info(response.json())
    except requests.RequestException as error:
        print(f'Error: {error}')
        current_app.logger.info(f'Error: {error}')
        return False

    return True

# get latest data from BOM, return as pandas dataframe
def get_latest_data() -> pd.DataFrame:

    stations_info = dataframe_from_es('bom-station-list', EMPTY_QUERY)

    df = pd.DataFrame()
    # ok_stations = pd.DataFrame(columns=stations_info.columns)

    print(stations_info.head)

    for index, station in stations_info.iterrows():
       # print(station)
        state = station['STA'][0] # first letter in state
        station_wmo = station['WMO']
        
        # assume all are 60901
        url = f'http://reg.bom.gov.au/fwo/ID{state}60901/ID{state}60901.{station_wmo}.json' # example: 'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json'
        # api refs: http://www.bom.gov.au/catalogue/data-feeds.shtml


        try:
            if LOCAL_DEV:
                print(url)
            else:
                current_app.logger.info(url)
            response = requests.get(url)
            if LOCAL_DEV:
                print(response)
                print("STATUS CODE:")
                print(response.status_code)
                print(type(response))
            else:
                current_app.logger.info(response)
                current_app.logger.info("STATUS CODE:")
                current_app.logger.info(response.status_code)
              

            if response:
                data=response.json()
                
                
                new_df = pd.DataFrame.from_dict(data['observations']['data'])
                df = pd.concat([df, new_df])

            # save the stations that have data to new csv
        #     ok_stations = pd.concat([
        #         ok_stations, 
        #         pd.DataFrame([station])]
        #    )
            

        except Exception as error:
            if LOCAL_DEV:
                print(f'Error: {error}')
                print(station)
                file1 = open("log.txt", "a")  # append mode
                file1.write(f'Error: {error}\n')
                file1.write(f'Station: {station}\n\n\n')
                file1.close()
            else:
                current_app.logger.info(f'Error: {error}')
    # ok_stations.to_csv('successes.csv', index=False)
    return df
    #print(df.head(15))
    #print(df)


   

def main():
    print("1")
    if LOCAL_DEV:
        file1 = open("log.txt", "w")
        L = ["Error LOG"]
        file1.writelines(L)
        file1.close()

    # print("Getting new data")
    data = get_latest_data()
    print(data)
    if UPLOAD:
        status = upload_es(INDEX_NAME, data)
        if status:
            print("UPLOAD SUCCESS")
            if not LOCAL_DEV:
                current_app.logger.info("UPLOAD SUCCESS")

            return "UPLOAD SUCCESS"
        else:
            print("FAILED")
            if not LOCAL_DEV:
                current_app.logger.info("UPLOAD FAILED")

            return "UPLOAD FAILED"
        

main()