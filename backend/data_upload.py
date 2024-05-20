import os
import pandas as pd
import json
import numpy as np
import requests

headers = {'Content-Type': 'application/json'}

# Process Homeless Data
def merge_data(data_dir):
    all_data_df = None
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.csv'):
            # Read each CSV file into a DataFrame
            file_path = os.path.join(data_dir, file_name)
            df = pd.read_csv(file_path)
            # Concatenate to the main DataFrame by appending rows
            all_data_df = pd.concat([all_data_df, df], ignore_index=True)

    if ' fin_yr' in all_data_df:      
        all_data_df[' fin_yr'] = all_data_df[' fin_yr'].str[:4]
    if ' lga_name' in all_data_df:
        all_data_df[' lga_name'] = all_data_df[' lga_name'].astype(str)
    return all_data_df

def process_homeless_data(data_dir):
    dataframe = merge_data(data_dir)
    dataframe[' fin_yr'] = dataframe[' fin_yr'].str[:4]
    dataframe[' lga_name'] = dataframe[' lga_name'].astype(str)
    return process_homeless_data

# Uplaod to Elastic Search
def upload_es(index_name, data_dir):
    actions = []
    URL = 'http://127.0.0.1:9090/post-data'
    if index_name == 'homeless':
        data = process_homeless_data(data_dir)
    elif index_name == 'income':
        data = process_homeless_data(data_dir)
        data.replace([np.inf, -np.inf, np.nan], None, inplace=True)
    else:
        data = merge_data(data_dir)
    for index, row in data.iterrows():
        if index_name == 'homeless':
            doc_id = f'{row[" lga_name"]}{row[" fin_yr"]}'
        elif index_name == 'population':
            doc_id = f'{row[" lga_name_2021"]}'
        elif index_name == 'crime':
            doc_id = f'{row[" lga_name11"]}'
        elif index_name == 'income':
            doc_id = f'{row[" lga_name"]}'
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
    try:
        response = requests.post(URL, json=wrapped_payload, headers=headers)
        print(f'Status Code: {response.status_code}')
        print(response.json())
    except requests.exceptions.RequestException as error:
        print(f'Error: {error}')
    return True

def main():
    upload_es('homeless', './data')
    upload_es('crime', './data/crime')
    upload_es('population', './data/region population/')
    upload_es('income','~/Downloads/incomedata.csv')

if __name__ == '__main__':
    main()
