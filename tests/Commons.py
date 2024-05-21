'''
Name: Hanchun Pan Student ID: 1266219, Email: hanchunp@student.unimelb.edu.au 
Name: Kaiyuan Cui Student ID: 1266180 , Email: kaicui@student.unimelb.edu.au 
Name: Runyu Yang Student ID: 1118665, Email: runyuy@student.unimelb.edu.au 
Name: Yaotian Wang  Student ID: 1503936, Email: yaotwang@student.unimelb.edu.au 
Name: Zhenghan Zhang Student ID: 1136448, Email: zhenghanz1@student.unimelb.edu.au 
'''
class Commons:
    @staticmethod
    def config(k):
        with open(f'/configs/default/parameters/{k}', 'r') as f:
            return f.read()
    @staticmethod
    def auth():
        return (Commons.config("ES_USERNAME"), Commons.config("ES_PASSWORD"))
    @staticmethod
    def search_url():
        return f'{Commons.config("ES_URL")}/{Commons.config("ES_TEST_DB")}/_search'
