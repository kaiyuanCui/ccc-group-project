from flask import request, current_app
import requests, logging
from elasticsearch8 import Elasticsearch
import json

def getindexinfo():
    query = {"query" : {"match_all": {}}}
    return elastic_search(query)



def elastic_search(query):
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )
    print("Attempting to fetch index info...")
  
    try:

        result = client.search(index = "bom", body = query, size = 100)

        return json.dumps(result.body)

    except Exception as e:
        # Handle errors (e.g., index does not exist, connection issues)
        return {"error": str(e)}

def main():
    current_app.logger.info(f'Received request: ${request.headers}')


    return "Request received"