from elasticsearch8 import Elasticsearch, helpers
import json
import pandas as pd 
def getindexinfo():
    # Establish connection to Elasticsearch
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )
    print("Attempting to fetch index info...")
    query = {"query" : {"match_all": {}}}
    try:
        
        result = client.search(index = "income", body = query, size = 100)

        return json.dumps(result.body)
        
    except Exception as e:
        # Handle errors (e.g., index does not exist, connection issues)
        return {"error": str(e)}
    

def fetch_data_from_es(index_name, client):
    query = {
        "query": {
            "match_all": {}
        }
    }
    
    try:
    # Fetch all documents from the index
        response = helpers.scan(client, index=index_name, query=query)
        docs = list(response)
        
        # Extract the _source field from each document
        data = [doc['_source'] for doc in docs]
        
        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        # Handle errors (e.g., index does not exist, connection issues)
        return {"error": str(e)}

def main():
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )
   
    
    data_homeless = fetch_data_from_es('homeless', client)
 
    data_income = fetch_data_from_es('income', client)
    try:

        data_homeless['fin_yr'] = data_homeless[' fin_yr'].astype(str)
        data_income['year'] = data_income['year'].astype(str)
        df_merged = pd.merge(data_homeless, data_income, left_on=[' lga_code', ' fin_yr'], right_on=['lga_code', 'year'], how='inner')
        df_merged = df_merged.to_json(orient= 'records')

    except Exception as e:
        # Handle errors (e.g., index does not exist, connection issues)
        return {"error": str(e)}
    return df_merged

if __name__ == "__main__":
    main()
