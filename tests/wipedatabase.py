'''
Name: Hanchun Pan Student ID: 1266219, Email: hanchunp@student.unimelb.edu.au 
Name: Kaiyuan Cui Student ID: 1266180 , Email: kaicui@student.unimelb.edu.au 
Name: Runyu Yang Student ID: 1118665, Email: runyuy@student.unimelb.edu.au 
Name: Yaotian Wang  Student ID: 1503936, Email: yaotwang@student.unimelb.edu.au 
Name: Zhenghan Zhang Student ID: 1136448, Email: zhenghanz1@student.unimelb.edu.au 
'''

from flask import request, current_app
import requests
from Commons import Commons

def main():
    r = requests.delete(f'{Commons.config("ES_URL")}/{Commons.config("ES_TEST_DB")}',
            verify=False,
            auth=Commons.auth())
    r = requests.put(f'{Commons.config("ES_URL")}/{Commons.config("ES_TEST_DB")}',
            verify=False,
            auth=Commons.auth(),
            headers={'Content-type': 'application/json'},
            #data=Commons.config("ES_SCHEMA")
        )

    return r.json(), r.status_code
