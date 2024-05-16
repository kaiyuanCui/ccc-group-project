import json
from elasticsearch8 import Elasticsearch, helpers
import pandas as pd
from flask import Flask, request, jsonify



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


def get_income_data():
    year = request.headers.get('X-Fission-Params-Year')
   
    # Base query
    query_homeless = {
        "query": {
            "match_all": {}
        }
    }
    
    query_income = {
        "query": {
            "match_all": {}
        }
    }

    # Add year filter to the queries if year is specified
    if year:
        query_homeless = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {" fin_yr": year}}
                    ]
                }
            }
        }
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
    data_homeless = fetch_data_from_es('homeless', query_homeless)
    data_income = fetch_data_from_es('income', query_income)

    if year and data_homeless.empty and data_income.empty:
        return jsonify({"message": f"No records found for the year {year}."}), 404
    
    try:
        
        data_homeless.columns = data_homeless.columns.str.strip()
        data_income.columns = data_income.columns.str.strip()

        # Ensure the columns are the same type
        data_homeless['fin_yr'] = data_homeless['fin_yr'].astype(str)
        data_income['year'] = data_income['year'].astype(str)
        
        # Merge the DataFrames
        df_merged = pd.merge(data_homeless, data_income, left_on=['lga_code', 'fin_yr'], right_on=['lga_code', 'year'], how='inner')

        df_merged.columns = df_merged.columns.str.strip()
        # Convert the DataFrame to JSON
        
        df_json = df_merged.to_json(orient='records')
        
        return jsonify(json.loads(df_json))
    
    except Exception as e:
        # Handle errors (e.g., index does not exist, connection issues)
        return jsonify({"error": str(e)})

def main():
    return get_income_data()


