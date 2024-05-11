import pandas as pd
import numpy as np
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
import json

# Load the CSV file into a DataFrame
data = pd.read_csv('~/Downloads/incomedata.csv')

# Replace infinite and NaN values with None
data.replace([np.inf, -np.inf, np.nan], None, inplace=True)

# Set up the requests session to accept self-signed certificates
session = requests.Session()
session.verify = False

# Define the Elasticsearch endpoint and authentication for BULK API
url = 'https://localhost:9200/income/_bulk'
auth = HTTPBasicAuth('elastic', 'elastic')
headers = {'Content-Type': 'application/json'}

actions = []
for index, row in data.iterrows():
    doc_id = f'{row[" lga_name"]}'
    payload = row.to_dict()
    for key, value in payload.items():
        if pd.isna(value):
            payload[key] = None
    action = {'index': {'_id': doc_id}}
    actions.append(json.dumps(action))
    actions.append(json.dumps(payload))


try:
    response = requests.post(url, data='\n'.join(actions) + '\n', headers=headers, auth=auth, verify=session.verify)
    print(f'Status Code: {response.status_code}')
except RequestException as error:
    print(f'Error: {error}')




 
