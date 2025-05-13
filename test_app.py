import unittest
import json
from app import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_all_beers(self):
        response = self.app.get('/beers/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        print("GET /beers/ OK")

    def test_get_beer_by_id(self):
        response = self.app.get('/beers/1')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            self.assertIn('name', response.json)
            self.assertIn('description', response.json)
        print(f"GET /beers/1 status: {response.status_code}")

    def test_get_all_breweries(self):
        response = self.app.get('/breweries/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        print("GET /breweries/ OK")


    def test_get_brewery_by_id(self):
        response = self.app.get('/breweries/1')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            self.assertIn('name', response.json)
            self.assertIn('description', response.json)
        print(f"GET /breweries/1 status: {response.status_code}")

    def test_get_all_users(self):
        response = self.app.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        print("GET /users/ OK")

    def test_get_user_by_id(self):
        response = self.app.get('/users/1')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            self.assertIn('pseudo', response.json)
            self.assertIn('email', response.json)
        print(f"GET /users/1 status: {response.status_code}")

    def test_get_all_deliveries(self):
        response = self.app.get('/deliveries/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        print("GET /deliveries/ OK")

    def test_get_delivery_by_id(self):
        response = self.app.get('/deliveries/1')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            self.assertIn('status', response.json)
            self.assertIn('delivery_address', response.json)
        print(f"GET /deliveries/1 status: {response.status_code}")

if __name__ == '__main__':
    unittest.main()
