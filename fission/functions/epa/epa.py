import requests
from elasticsearch8 import Elasticsearch
import time

def main():
    client = Elasticsearch (
        'https://localhost:9200',
        verify_certs= False,
        ssl_show_warn= False,
        basic_auth=('elastic', 'elastic')
    )

    url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/parameters?environmentalSegment=air"
    hdr ={
        # Request headers
        'Cache-Control': 'no-cache',
        'X-API-Key': 'b3eecb57fa9046c090964ca6691113a0',
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

if __name__ == '__main__':
    main()