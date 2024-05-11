from elasticsearch8 import Elasticsearch
import json

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

def main():
    # Get crime index information
    crime_index_info = getindexinfo()
  
    return crime_index_info

if __name__ == "__main__":
    main()
