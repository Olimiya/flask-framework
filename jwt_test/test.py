# 单元测试，测试jwt
# $ python test.py

import unittest
import json
from app import app

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

if __name__ == '__main__':
    unittest.main()