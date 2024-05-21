'''
Name: Hanchun Pan Student ID: 1266219, Email: hanchunp@student.unimelb.edu.au 
Name: Kaiyuan Cui Student ID: 1266180 , Email: kaicui@student.unimelb.edu.au 
Name: Runyu Yang Student ID: 1118665, Email: runyuy@student.unimelb.edu.au 
Name: Yaotian Wang  Student ID: 1503936, Email: yaotwang@student.unimelb.edu.au 
Name: Zhenghan Zhang Student ID: 1136448, Email: zhenghanz1@student.unimelb.edu.au 
'''

import unittest, requests, json, time

class HTTPSession:
    def __init__(self, protocol, hostname, port):
        self.session = requests.session()
        self.base_url = f'{protocol}://{hostname}:{port}'

    def get(self, path):
        return self.session.get(f'{self.base_url}{path}')

    def post(self, path, data):
        return self.session.post(f'{self.base_url}{path}', headers = {'Content-Type': 'application/json'}, json=data)

    def put(self, path, data):
        return self.session.put(f'{self.base_url}{path}', json=data)

    def delete(self, path):
        return self.session.delete(f'{self.base_url}{path}')

class TestEnd2End(unittest.TestCase):
    def setUp(self):
        self.assertEqual(test_request.delete('/wipedatabase').status_code, 200)
        time.sleep(1)

    def test_income(self):
        self.assertEqual(test_request.get('/get-income-data/year/2010').status_code, 404)
        wrapped_payload = {
            'index_name': "test",
            'data': json.dumps({'index': {'_id': 0}, 'year': 2010}) + '\n'
        }
        self.assertEqual(test_request.post('/post-data', wrapped_payload).status_code, 200)
        self.assertEqual(test_request.get('/get-income-data/year/2010/').status_code, 201)

    
    


#self.assertEqual(test_request.put('/students/1', {'name': 'John Doe', 'courses': '90024'}).status_code, 201)
if __name__ == '__main__':
    test_request = HTTPSession('http', 'localhost', 9090)
    unittest.main()

