import os
import pandas as pd
import requests

INDEX_NAME = 'index'


url = 'https://localhost:9200'
headers = {'Content-Type': 'application/json'}
auth = ('elastic', 'elastic')
requests.packages.urllib3.disable_warnings()
verify_ssl = False

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
    if index_name == 'homeless':
        data = process_homeless_data(data_dir)
    else:
        data = merge_data(data_dir)
    index_url = url + '/' + index_name + '/_doc'
    for index, row in data.iterrows():
        payload = row.to_dict()

        for key in payload:
            if pd.isna(payload[key]):
                payload[key] = None
        try:
            response = requests.post(index_url, json=payload, headers=headers, auth=auth, verify=verify_ssl)
            print(f'Status Code: {response.status_code}')
            print(response.json())
        except requests.exceptions.RequestException as error:
            print(f'Error: {error}')
    return True

def main():
    upload_es('homeless', './data')
    upload_es('crime', './data/crime')
    upload_es('population', './data/region population/')
    # upload_es(INDEX_NAME, './data')

if __name__ == '__main__':
    main()
