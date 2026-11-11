import unittest
import requests

class TestServer(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://localhost:8000'

    def test_get(self):
        r = requests.get(self.base_url + '/hello')
        assert 200 == r.status_code

    def test_post(self):
        r = requests.post(self.base_url + '/post_data',json={
            'name' : 'Sid',
            'price' : 2000
        })
        assert 201 == r.status_code
    
    def test_post_data(self):
        r = requests.post(self.base_url + '/post_data',json={
            'name' : 'Sid',
            'price' : 2000
        })

        data = r.json()

        assert 'Sid' == data.get('name')
        assert 2000 == data.get('price')
