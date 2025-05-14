import unittest
from app import app

class TestIntegrationAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_full_beer_workflow(self):
        print("\n--- Test: Full Beer Workflow ---")
        new_beer = {
            "name": "Integration Beer",
            "description": "A beer for integration testing",
            "price": 6.99,
            "brewery_id": 1,
            "image_url": "http://example.com/integration_beer.jpg"
        }
        add_response = self.app.post('/beers/', json=new_beer)
        print(f"POST /beers/ status: {add_response.status_code}")
        self.assertEqual(add_response.status_code, 201)

        get_response = self.app.get('/beers/')
        print(f"GET /beers/ status: {get_response.status_code}")
        self.assertEqual(get_response.status_code, 200)
        self.assertIsInstance(get_response.json, list)

        if any(beer['name'] == "Integration Beer" for beer in get_response.json):
            print("Beer added and retrieved successfully.")
        else:
            print("Beer not found in list.")
        self.assertTrue(any(beer['name'] == "Integration Beer" for beer in get_response.json))

    def test_full_brewery_workflow(self):
        print("\n--- Test: Full Brewery Workflow ---")
        new_brewery = {
            "name": "Integration Brewery",
            "description": "A brewery for integration testing",
            "location": "Integration Location",
            "image_url": "http://example.com/integration_brewery.jpg"
        }
        add_response = self.app.post('/breweries/', json=new_brewery)
        print(f"POST /breweries/ status: {add_response.status_code}")
        self.assertEqual(add_response.status_code, 201)

        get_response = self.app.get('/breweries/')
        print(f"GET /breweries/ status: {get_response.status_code}")
        self.assertEqual(get_response.status_code, 200)
        self.assertIsInstance(get_response.json, list)

        if any(brewery['name'] == "Integration Brewery" for brewery in get_response.json):
            print("Brewery added and retrieved successfully.")
        else:
            print("Brewery not found in list.")
        self.assertTrue(any(brewery['name'] == "Integration Brewery" for brewery in get_response.json))

    def test_full_delivery_workflow(self):
        print("\n--- Test: Full Delivery Workflow ---")
        get_response = self.app.get('/deliveries/')
        print(f"GET /deliveries/ status: {get_response.status_code}")
        self.assertEqual(get_response.status_code, 200)
        self.assertIsInstance(get_response.json, list)
        print("Deliveries retrieved successfully.")

if __name__ == '__main__':
    unittest.main()
