import unittest
from app import app

class TestIntegrationAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_full_beer_workflow(self):
        new_beer = {
            "name": "Integration Beer",
            "description": "A beer for integration testing",
            "price": 6.99,
            "brewery_id": 1,
            "image_url": "http://example.com/integration_beer.jpg"
        }
        add_response = self.app.post('/beers/', json=new_beer)
        self.assertEqual(add_response.status_code, 201)  

        get_response = self.app.get('/beers/')
        self.assertEqual(get_response.status_code, 200)
        self.assertIsInstance(get_response.json, list)
        self.assertTrue(any(beer['name'] == "Integration Beer" for beer in get_response.json))

    def test_full_brewery_workflow(self):
        new_brewery = {
            "name": "Integration Brewery",
            "description": "A brewery for integration testing",
            "location": "Integration Location",
            "image_url": "http://example.com/integration_brewery.jpg"
        }
        add_response = self.app.post('/breweries/', json=new_brewery)
        self.assertEqual(add_response.status_code, 201)  

        get_response = self.app.get('/breweries/')
        self.assertEqual(get_response.status_code, 200)
        self.assertIsInstance(get_response.json, list)
        self.assertTrue(any(brewery['name'] == "Integration Brewery" for brewery in get_response.json))

    def test_full_delivery_workflow(self):
        
        get_response = self.app.get('/deliveries/')
        self.assertEqual(get_response.status_code, 200)
        self.assertIsInstance(get_response.json, list)

if __name__ == '__main__':
    unittest.main()
