import json
from elasticsearch8 import Elasticsearch, helpers
import pandas as pd
from flask import Flask, request, jsonify
import requests
from requests.exceptions import HTTPError, RequestException

# Establish connection to Elasticsearch
client = Elasticsearch(
    'https://elasticsearch-master.elastic.svc.cluster.local:9200',
    verify_certs=False,
    ssl_show_warn=False,
    basic_auth=('elastic', 'elastic')
)

def fetch_data_from_es(index_name, query):
    try:
        # Fetch all documents from the index based on the query
        response = helpers.scan(client, index=index_name, query=query)
        docs = list(response)
        
        # Extract the _source field from each document
        data = [doc['_source'] for doc in docs]
        
        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        # Handle errors (e.g., index does not exist, connection issues)
        return pd.DataFrame()  # Return an empty DataFrame

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
 
    data_income = fetch_data_from_es('income', query_income)
   
    
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



def main():
    data = get_income_data()
    return data

if __name__ == '__main__':
    main()

