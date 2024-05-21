import requests
from elasticsearch8 import Elasticsearch
import time

def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

def main():
    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        ssl_show_warn= False,
        basic_auth=(config('ES_USERNAME'), config('ES_PASSWORD'))
    )

    url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/parameters?environmentalSegment=air"
    hdr ={
        # Request headers
        'Cache-Control': 'no-cache',
        'X-API-Key': config('EPA_API_KEY'),
        'User-Agent': "Carlyly"
    }

    try:
        response = requests.get(url, headers=hdr)
    except Exception as e:
        print(e)
        return

    for record in response.json()['records']:
        client.index(
            index='epa',
            id=f'{record["siteID"]}-{time.time()}',
            body=record
        )

    return 'ok'