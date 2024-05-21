'''
Team 77:
Name: Hanchun Pan Student ID: 1266219, Email: hanchunp@student.unimelb.edu.au 
Name: Kaiyuan Cui Student ID: 1266180 , Email: kaicui@student.unimelb.edu.au 
Name: Runyu Yang Student ID: 1118665, Email: runyuy@student.unimelb.edu.au 
Name: Yaotian Wang  Student ID: 1503936, Email: yaotwang@student.unimelb.edu.au 
Name: Zhenghan Zhang Student ID: 1136448, Email: zhenghanz1@student.unimelb.edu.au 
'''

import unittest
import requests


class TestEnd2End(unittest.TestCase):

    BASE_URL = 'http://127.0.0.1:9090'

    def send_request(self, endpoint, method='GET', params=None, data=None):
        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.request(method, url, params=params, json=data)
        return response

    def assertResponse(self, response, expected_status_code=200):
        self.assertEqual(response.status_code, expected_status_code, f"Expected status code {expected_status_code}")
        self.assertIsInstance(response.json(), list, "Expected response to be a list")

    def test_get_income_data(self):
        ## year from 2014 and 2017 will have data return, else return 404 because no corresponding year
        year = 2017
        endpoint = f'get-income-data/year/{year}'
        response = self.send_request(endpoint)
        self.assertResponse(response)

    def test_get_crime_data(self):
        endpoint = 'get-crime-data'
        response = self.send_request(endpoint)
        self.assertResponse(response)

    def test_get_pop_data(self):
        endpoint = 'get-pop-data'
        response = self.send_request(endpoint)
        self.assertResponse(response)

    def test_get_geodata(self):
        endpoint = 'get-geodata'
        params = {'from-last': True, 'limit': 1}
        response = self.send_request(endpoint, params=params)
        self.assertResponse(response)

    def test_get_epa_data(self):
        endpoint = 'get-epa-data'
        params = {
            'start': '2023-05-12T06:00:00Z',
            'end': '2024-05-12T07:00:00Z',
            'from-last': True,
            'limit': 1
        }
        response = self.send_request(endpoint, params=params)
        self.assertResponse(response)

    def test_get_bom_data(self):
        endpoint = 'get-bom-data'
        params = {
            'start': '20240516220000',
            'end': '20240517220000'
        }
        response = self.send_request(endpoint, params=params)
        self.assertResponse(response)

    def test_get_homeless_data(self):
        endpoint = 'homeless'
        response = self.send_request(endpoint)
        self.assertResponse(response)
    
    def post_data(self):
        endpoint = 'post-data'
        test_request = self.BASE_URL + '/' + endpoint
        wrapped_payload = {
            'index_name': "test",
            'data': '{"index": {"_id": 0}}\n{"year": 2010})\n{"index": {"_id": 1}}\n{"year": 2011}}\n'
        }
        self.assertEqual(test_request.post('/post-data', wrapped_payload).status_code, 200)

if __name__ == '__main__':
    unittest.main()