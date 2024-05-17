import json
from elasticsearch8 import Elasticsearch, helpers
import pandas as pd
from flask import Flask, request, jsonify, current_app
import requests
from requests.exceptions import HTTPError, RequestException
import re

import warnings
warnings.filterwarnings('ignore')
requests.packages.urllib3.disable_warnings()

'''
GLOBAL API SETTINGS:

'''
LOCAL_DEV = False
ES_URL = 'https://localhost:9200' if LOCAL_DEV else 'https://elasticsearch-master.elastic.svc.cluster.local:9200'
EMPTY_QUERY = {
        "query": {
            "match_all": {}
        }
    }

def config(k):
   
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

# Establish connection to Elasticsearch
client = Elasticsearch(
    ES_URL,
    verify_certs=False,
    ssl_show_warn=False,
    basic_auth=(config('ES_USERNAME'), config('ES_PASSWORD'))
)



'''

Elastic Search helper functions

'''

def hits_from_es(index_name, query):
    '''
    return the 'hits' section of the raw response from Elastic Search
    
    '''
    try:
        # Fetch all documents from the index based on the query
        response = client.search(index=index_name, body=query)
        if LOCAL_DEV:
            print("")
        return response['hits']['hits']
    
    except Exception as e:
        # Handle errors (e.g., index does not exist, connection issues)
        return {"error": str(e)}  # Return an empty DataFrame
    

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
    

'''

General helper functions

'''

def clean_crime_data(dataframe):
    choose_col = [ ' reference_period', ' lga_code11', ' lga_name11', ' total_division_a_offences', ' total_division_b_offences', ' total_division_c_offences', ' total_division_d_offences', ' total_division_e_offences', ' total_division_f_offences']
    crime_total = dataframe[choose_col]
    crime_total.rename(columns={
        ' reference_period': 'year',
        ' lga_code11': 'lga_code',
        ' lga_name11': 'lga_name',
        ' total_division_a_offences': 'a_offences_num',
        ' total_division_b_offences': 'b_offences_num',
        ' total_division_c_offences': 'c_offences_num',
        ' total_division_d_offences': 'd_offences_num',
        ' total_division_e_offences': 'e_offences_num',
        ' total_division_f_offences': 'f_offences_num'
    }, inplace=True)
    return crime_total

def clean_population_data(dataframe):
    filtered_columns = dataframe.filter(regex='14|15|16|17|18|19').columns.tolist()
    pop_df = dataframe[filtered_columns]
    #print(pop_df)
    long_format = pd.DataFrame()


    key_columns = [' state_name_2021', ' lga_name_2021', ' lga_code_2021']
    use_col = [col.strip() for col in key_columns]
    pop_df.columns = pop_df.columns.str.strip()
    feature_columns = [col for col in pop_df.columns if col not in key_columns]

    for col in feature_columns:
        match = re.match(r'([a-zA-Z_]+)_(20\d{2})(?:_\d{2})?', col.strip())
        if match:
            type_name = match.group(1)
            year = match.group(2)
            temp_df = dataframe[key_columns].copy()  
            temp_df['variable'] = type_name
            temp_df['value'] = pop_df[col]
            temp_df['year'] = int(year)
            long_format = pd.concat([long_format, temp_df], ignore_index=True)

    #print(long_format.head())
    long_format.columns = long_format.columns.str.strip()
    #print(long_format.columns)
    wide_format = long_format.pivot_table(index=use_col + ['year'], columns='variable', values='value').reset_index()
    
    wide_format.rename(columns={
        'lga_code_2021': 'lga_code',
        'lga_name_2021': 'lga_name',
        'state_name_2021': 'state_name'
    }, inplace=True)
    #print(wide_format.head())
    return wide_format
    

'''

API ENDPOINTS

'''


def get_homeless_data_from_api():
    url = 'http://router.fission.svc.cluster.local:80/homeless'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        
        try:
            data = response.json()
            return pd.DataFrame(data)
        except ValueError as json_error:
            
            return pd.DataFrame()  

    except HTTPError as http_err: # For local testing
        print(f"HTTP error occurred: {http_err}")  
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  
    except Exception as err:
        print(f"An error occurred: {err}") 

    return pd.DataFrame()  

def get_income_data():
    year = request.headers.get('X-Fission-Params-Year')
    query_income = {
        "query": {
            "match_all": {}
        }
    }

    # Add year filter to the queries if year is specified
    if year:
        query_income = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"year": year}}
                    ]
                }
            }
        }
    
    # Fetch data from Elasticsearch based on the queries
    data_homeless = get_homeless_data_from_api()
 
    data_income = dataframe_from_es('income', query_income)
   
    
    if year and data_income.empty:
        return jsonify({"message": f"No records found for the year {year}."}), 404
    
    try:
        
        data_homeless.columns = data_homeless.columns.str.strip()
        data_income.columns = data_income.columns.str.strip()

        # Ensure the columns are the same type
        data_homeless['year'] = data_homeless['year'].astype(str)
        data_income['year'] = data_income['year'].astype(str)
        
        # Merge the DataFrames
        df_merged = pd.merge(data_homeless, data_income, left_on=['lga_code', 'year'], right_on=['lga_code', 'year'], how='inner')

        # Convert the DataFrame to JSON
        df_json = df_merged.to_json(orient='records')
        
        return df_json
    
    except Exception as e:
        # Handle errors (e.g., index does not exist, connection issues)
        return {"error": str(e)}



def get_bom_data():
     # Get query parameters from the request

    if not LOCAL_DEV:
        params = request.args

        start_date = params.get('start')
        end_date = params.get('end')
    else: 
        start_date, end_date = (None, None)
        
        # some test dates
        # start_date = '20240516220000'
        # end_date = '20240517220000'

        
        
    # Construct Elasticsearch query based on parameters
    query = {
        "_source": ['name', 'local_date_time', 'local_date_time_full', 'lat', 'lon', 'apparent_t', 'air_temp'],
        "query": {
            "match_all": {}
        }
    }

    if start_date or end_date:
        query["query"]=  {
                "bool": {
                    "must": 
                        [
                            {
                                "range": 
                                {
                                    "local_date_time_full":
                                        {}
                                }
                                
                            }
                        ]
                    }
            }

        if start_date:
            query["query"]["bool"]["must"][0]["range"]["local_date_time_full"]["gte"] =  start_date
        if end_date:
            query["query"]["bool"]["must"][0]["range"]["local_date_time_full"]["lte"] =  end_date

    try:
        #print(query)
        data = dataframe_from_es('bom', query)
        #print(data)
    except Exception as e:
        return {"error": str(e)}

    json_data = data.to_json(orient='records')
    if not LOCAL_DEV:
        current_app.logger.info(f'{data.head()}')
    else: 
        print(data.head())
    return json_data


def get_geodata():
    hits = hits_from_es('geodata', EMPTY_QUERY)
   
    data = [hit['_source'] for hit in hits]
    json_str = json.dumps(data)
    return json_str

def get_epa_data():
    if not LOCAL_DEV:
        params = request.args

        start_date = params.get('start')
        end_date = params.get('end')
    else: 
        start_date, end_date = (None, None)
        
        # some test dates
        start_date = '2024-05-12T06:00:00Z'
        end_date = '2024-05-12T07:00:00Z'

        
        
    # Construct Elasticsearch query based on parameters
    query = {
       # "_source": ["siteName", 'parameters.timeSeriesReadings', 'geometry', ],
        "query": {
            "match_all": {}
        }
    }

    if start_date or end_date:
        query["query"]=  {
           
             "bool": {
                    "must": [
                       {
                            "range": {
                                "parameters.timeSeriesReadings.readings.since": {
                                    
                                }
                            }
                        }
                    ]
             }
        
        }

        if start_date:
            query["query"]["bool"]["must"][0]["range"]["parameters.timeSeriesReadings.readings.since"]["gte"] =  start_date
        if end_date:
            query["query"]["bool"]["must"][0]["range"]["parameters.timeSeriesReadings.readings.since"]["lte"] =  end_date
    try:
        #print(query)
        hits = hits_from_es('epa', query)
        hits_json = json.dumps(hits)
        print(hits_json)
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500

  
    if not LOCAL_DEV:
        current_app.logger.info(f'{hits}')
    else: 
        print("")
    return hits_json




def get_processed_pop():
    try:
        data = dataframe_from_es('population', EMPTY_QUERY)
        #print(data.head())
        json = clean_population_data(data).to_json(orient='records')
        #print(json)
    except Exception as e:
         return jsonify({"error": f"{e}"}), 500
    
    return json

def get_processed_crime():
    try:
        data = dataframe_from_es('crime', EMPTY_QUERY)
        #print(data.head())
        json = clean_crime_data(data).to_json(orient='records')
        #print(json)
    except Exception as e:
         return jsonify({"error": f"{e}"}), 500
    
    return json
    

'''

POST REQUESTS:

'''

def post_data():
    data = None
    if not LOCAL_DEV:
        data = request.json
    else:
        # local test data
        data = {
            'index_name': 'economy',
            'data': {}
        }

    
    print(data)
    if not LOCAL_DEV:
        current_app.logger.info(f'{data}')
    try:
        index_name = data['index_name']
        payload = data['data']
        index_url = ES_URL + '/' + index_name + '/_doc'
        headers = {'Content-Type': 'application/json'}
        auth = (config('ES_USERNAME'), config('ES_PASSWORD'))
        verify_ssl = False
        try:
            response = requests.post(index_url, json=payload, headers=headers, auth=auth, verify=verify_ssl)
            print(f'Status Code: {response.status_code}')
            print(response.json())
            if not LOCAL_DEV:
                current_app.logger.info(f'{response.json()}')
            return jsonify({"OK": f"OK"}), 200
        except requests.exceptions.RequestException as error:
            return jsonify({"error": f"{error}"}), 400
       
    except Exception as e:
        return jsonify({"error": f"{e}"}), 400



# def main():
#     data = get_income_data()
#     return data

if __name__ == '__main__':
    get_epa_data()


'''

curl -X 'POST' \
  "http://127.0.0.1:9090/post-data"  \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "index": 'economy', 
  "data": {}
}'
'''