'''
Name: Hanchun Pan Student ID: 1266219, Email: hanchunp@student.unimelb.edu.au 
Name: Kaiyuan Cui Student ID: 1266180 , Email: kaicui@student.unimelb.edu.au 
Name: Runyu Yang Student ID: 1118665, Email: runyuy@student.unimelb.edu.au 
Name: Yaotian Wang  Student ID: 1503936, Email: yaotwang@student.unimelb.edu.au 
Name: Zhenghan Zhang Student ID: 1136448, Email: zhenghanz1@student.unimelb.edu.au 
'''

import pandas as pd
import requests
import json
# from flask import current_app


INDEX_NAME = 'bom-station-list'
IS_LOCAL = False
UPLOAD = True


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

def get_ok_stations() -> pd.DataFrame:
    stations_info = extract_station_list()
    df = pd.DataFrame()
    ok_stations = pd.DataFrame(columns=stations_info.columns)

    for index, station in stations_info.iterrows():
        state = station['STA'][0] # first letter in state
        station_wmo = station['WMO']
        
        # assume all are 60901
        url = f'http://reg.bom.gov.au/fwo/ID{state}60901/ID{state}60901.{station_wmo}.json' # example: 'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json'
        # api refs: http://www.bom.gov.au/catalogue/data-feeds.shtml
        try:
            if IS_LOCAL:
                print(url)
            else:
                print(url)
            response = requests.get(url)
            if IS_LOCAL:
                print(response)
                print("STATUS CODE:")
                print(response.status_code)
            else:
                print(response)
            data=response.json()
            new_df = pd.DataFrame.from_dict(data['observations']['data'])
            df = pd.concat([df, new_df])

            # save the stations that have data to new csv
            ok_stations = pd.concat([
                ok_stations, 
                pd.DataFrame([station])]
        )
        except requests.RequestException as error:
            if IS_LOCAL:
                print(f'Error: {error}')
                print(station)
                file1 = open("log.txt", "a")  # append mode
                file1.write(f'Error: {error}\n')
                file1.write(f'Station: {station}\n\n\n')
                file1.close()
            else:
                print(f'Error: {error}')
    # ok_stations.to_csv('successes.csv', index=False)
    print(ok_stations.head())
    return ok_stations

def upload_es(index_name:str, data:pd.DataFrame) -> bool:
    # request settings:
    headers = {'Content-Type': 'application/json'}
    URL = 'http://127.0.0.1:9090/post-data'
    actions = []
    for index, row in data.iterrows():
        doc_id = row['WMO']
        payload = row.to_dict()
        for key, value in payload.items():
            if pd.isna(value):
                payload[key] = None
        action = {'index': {'_id': doc_id}}
        actions.append(json.dumps(action))
        actions.append(json.dumps(payload))

    wrapped_payload = {
        'index_name': index_name,
        'data': '\n'.join(actions) + '\n'
    }
    print(wrapped_payload)
    try:
        response = requests.post(URL, json=wrapped_payload, headers=headers)
        print(f'Status Code: {response.status_code}')
        print(response.json())
    except requests.exceptions.RequestException as error:
        print(f'Error: {error}')
    return True


def main():
    if IS_LOCAL:
        file1 = open("log.txt", "w")
        L = ["Error LOG"]
        file1.writelines(L)
        file1.close()
    print('get_stations')
    data = get_ok_stations()
    if UPLOAD:
        status = upload_es(INDEX_NAME, data)
        if status:
            print("UPLOAD SUCCESS")
            if not IS_LOCAL:
                print("UPLOAD SUCCESS")

            return "UPLOAD SUCCESS"
        else:
            print("FAILED")
            if not IS_LOCAL:
                print("UPLOAD FAILED")

            return "UPLOAD FAILED"
        
main()