from flask import request, current_app
import requests, logging

def main():
    current_app.logger.info(f'Received request: ${request.headers}')
    r = requests.get('https://elasticsearch-master.elastic.svc.cluster.local:9200/bom/_doc/Hope Banks Beacon20240508203000',
        verify=False,
        auth=('elastic', 'elastic'))
    current_app.logger.info(f'Status ES request: {r.status_code}')


    return r.json()
