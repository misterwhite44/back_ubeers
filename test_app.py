import unittest
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_beers(self):
        response = self.app.get('/beers/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_add_beer(self):
        new_beer = {
            "name": "Test Beer",
            "description": "A test beer",
            "price": 5.99,
            "brewery_id": 1,
            "image_url": "http://example.com/image.jpg"
        }
        response = self.app.post('/beers/', json=new_beer)
        self.assertEqual(response.status_code, 201)  # Changer 200 par 201

    def test_get_breweries(self):
        response = self.app.get('/breweries/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_add_brewery(self):
        new_brewery = {
            "name": "Test Brewery",
            "description": "A test brewery",
            "location": "Test Location",
            "image_url": "http://example.com/image.jpg"
        }
        response = self.app.post('/breweries/', json=new_brewery)
        self.assertEqual(response.status_code, 201)  # Changer 200 par 201

    def test_get_users(self):
        response = self.app.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_deliveries(self):
        response = self.app.get('/deliveries/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    
if __name__ == '__main__':
    unittest.main()
