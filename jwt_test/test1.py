# 测试app.py中的login和protected函数

import unittest
import json
from app import app
import logging


class FlaskJWTTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.client.testing = True

    def test_login(self):
        """
        Tests login.
        """
        response = self.client.post('/login', data=json.dumps(dict(
            username='test',
            password='test'
        )), content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('access_token', data)
        #logging.info('login response: %s', data['access_token'])  # 输出login接口响应数据

    def test_protected(self):
        """
        Tests protected endpoint.
        """
        # login first
        response = self.client.post('/login', data=json.dumps(dict(
            username='test',
            password='test'
        )), content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('access_token', data)

        # access protected endpoint
        response = self.client.get('/protected', headers=dict(
            Authorization='Bearer ' + data['access_token']
        ))
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('logged_in_as', data)
        #logging.info('login response: %s', data)  # 输出login接口响应数据


if __name__ == '__main__':
    unittest.main()