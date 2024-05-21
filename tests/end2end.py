'''
Team 77:
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
        return self.session.post(f'{self.base_url}{path}', json=data)

    def put(self, path, data):
        return self.session.put(f'{self.base_url}{path}', json=data)

    def delete(self, path):
        return self.session.delete(f'{self.base_url}{path}')

class TestEnd2End(unittest.TestCase):
    def setUp(self):
        self.assertEqual(test_request.delete('/wipedatabase').status_code, 200)
        time.sleep(1)

if __name__ == '__main__':
    test_request = HTTPSession('http', 'localhost', 9090)
    unittest.main()

