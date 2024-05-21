'''
Team 77:
Name: Hanchun Pan Student ID: 1266219, Email: hanchunp@student.unimelb.edu.au 
Name: Kaiyuan Cui Student ID: 1266180 , Email: kaicui@student.unimelb.edu.au 
Name: Runyu Yang Student ID: 1118665, Email: runyuy@student.unimelb.edu.au 
Name: Yaotian Wang  Student ID: 1503936, Email: yaotwang@student.unimelb.edu.au 
Name: Zhenghan Zhang Student ID: 1136448, Email: zhenghanz1@student.unimelb.edu.au 
'''

from flask import request, current_app
import requests

def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()
def auth():
    return (config("ES_USERNAME"), config("ES_PASSWORD"))

def search_url():
    return f'{config("ES_URL")}/{config("ES_TEST_DB")}/_search'
    

def main():
    requests.delete(f'{config("ES_URL")}/{config("ES_TEST_DB")}',
        verify=False,
        auth=auth())
    r = requests.put(f'{config("ES_URL")}/{config("ES_TEST_DB")}',
            verify=False,
            auth=auth(),
            headers={'Content-type': 'application/json'},
            #data=config("ES_SCHEMA")
        )

    return r.json(), r.status_code
