import logging, json, requests, socket
import os
import pandas as pd
import requests
from pandas.util import hash_pandas_object

INDEX_NAME = 'bom'
IS_LOCAL = True
UPLOAD = True
STATIONS_LIST = './successes.csv'




# Uplaod to Elastic Search
def upload_es(index_name:str, data:pd.DataFrame) -> bool:
    # request settings:
    url =''
    if IS_LOCAL:
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
        print(f'Status Code: {response.status_code}')
        print(response.json())
    except requests.RequestException as error:
        print(f'Error: {error}')
        return False

    return True

# get latest data from BOM, return as pandas dataframe
def get_latest_data() -> pd.DataFrame:

    stations_info = pd.read_csv(STATIONS_LIST)

    

    df = pd.DataFrame()
    ok_stations = pd.DataFrame(columns=stations_info.columns)
    print(stations_info.head)

    for index, station in stations_info.iterrows():
       # print(station)
        state = station['STA'][0] # first letter in state
        station_wmo = station['WMO']
        
        # assume all are 60901
        url = f'http://reg.bom.gov.au/fwo/ID{state}60901/ID{state}60901.{station_wmo}.json' # example: 'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json'
        # api refs: http://www.bom.gov.au/catalogue/data-feeds.shtml


        try:
            print(url)
            response = requests.get(url)
            print(response)
            print("STATUS CODE:")
            print(response.status_code)
            data=response.json()
            
            
            new_df = pd.DataFrame.from_dict(data['observations']['data'])
            df = pd.concat([df, new_df])

            # save the stations that have data to new csv
            ok_stations = pd.concat([
                ok_stations, 
                pd.DataFrame([station])]
           )
            

        except requests.RequestException as error:
            print(f'Error: {error}')
            print(station)
            file1 = open("log.txt", "a")  # append mode
            file1.write(f'Error: {error}\n')
            file1.write(f'Station: {station}\n\n\n')
            file1.close()
    
    ok_stations.to_csv('successes.csv', index=False)
    return df
    #print(df.head(15))
    #print(df)

    


def main():
    file1 = open("log.txt", "w")
    L = ["Error LOG"]
    file1.writelines(L)
    file1.close()



    print("Getting new data")
    data = get_latest_data()
    print(data)
    if UPLOAD:
        status = upload_es(INDEX_NAME, data)
        if status:
            print("UPLOAD SUCCESS")
        else:
            print("FAILED")
main()