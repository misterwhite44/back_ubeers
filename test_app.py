import pytest
import json
import logging
from app import app  # Assurez-vous que le fichier de votre application s'appelle app.py

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Tests pour les Beer
def test_get_beers(client):
    logger.info("Running test_get_beers...")
    response = client.get('/beers/')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)  # Doit renvoyer une liste
    logger.info("test_get_beers passed.")

def test_add_beer(client):
    logger.info("Running test_add_beer...")
    beer_data = {
        'name': 'Test Beer',
        'description': 'Test Description',
        'price': 10.99,
        'brewery_id': 1,
        'image_url': 'http://example.com/beer.jpg'
    }
    response = client.post('/beers/', data=json.dumps(beer_data), content_type='application/json')
    assert response.status_code == 201
    assert 'Beer added successfully' in str(response.data)
    logger.info("test_add_beer passed.")

def test_get_single_beer(client):
    logger.info("Running test_get_single_beer...")
    response = client.get('/beers/1')
    assert response.status_code == 200
    assert 'name' in json.loads(response.data)  # Vérifie que la bière existe
    logger.info("test_get_single_beer passed.")

def test_update_beer(client):
    logger.info("Running test_update_beer...")
    beer_data = {
        'name': 'Updated Beer',
        'description': 'Updated Description',
        'price': 12.99,
        'brewery_id': 1,
        'image_url': 'http://example.com/updated_beer.jpg'
    }
    response = client.put('/beers/1', data=json.dumps(beer_data), content_type='application/json')
    assert response.status_code == 200
    assert 'Beer updated successfully' in str(response.data)
    logger.info("test_update_beer passed.")

def test_delete_beer(client):
    logger.info("Running test_delete_beer...")
    response = client.delete('/beers/1')
    assert response.status_code == 200
    assert 'Beer deleted successfully' in str(response.data)
    logger.info("test_delete_beer passed.")

# Tests pour les Breweries
def test_get_breweries(client):
    logger.info("Running test_get_breweries...")
    response = client.get('/breweries/')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)
    logger.info("test_get_breweries passed.")

def test_add_brewery(client):
    logger.info("Running test_add_brewery...")
    brewery_data = {
        'name': 'Test Brewery',
        'description': 'Test Brewery Description',
        'location': 'Test Location',
        'image_url': 'http://example.com/brewery.jpg'
    }
    response = client.post('/breweries/', data=json.dumps(brewery_data), content_type='application/json')
    assert response.status_code == 201
    assert 'Brewery added successfully' in str(response.data)
    logger.info("test_add_brewery passed.")

# Tests pour les Users
def test_get_users(client):
    logger.info("Running test_get_users...")
    response = client.get('/users/')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)
    logger.info("test_get_users passed.")

def test_add_user(client):
    logger.info("Running test_add_user...")
    user_data = {
        'pseudo': 'test_user',
        'email': 'testuser@example.com',
        'password': 'testpassword123',
        'address': 'Test Address',
        'phone_number': '1234567890'
    }
    response = client.post('/users/', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == 201
    assert 'User added successfully' in str(response.data)
    logger.info("test_add_user passed.")

# Tests pour les Deliveries
def test_get_deliveries(client):
    logger.info("Running test_get_deliveries...")
    response = client.get('/deliveries/')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)
    logger.info("test_get_deliveries passed.")

def test_add_delivery(client):
    logger.info("Running test_add_delivery...")
    delivery_data = {
        'beer_id': 1,
        'quantity': 10,
        'delivery_address': 'Test Delivery Address',
        'delivery_date': '2025-05-13 12:00:00',
        'status': 'Pending',
        'user_id': 1
    }
    response = client.post('/deliveries/', data=json.dumps(delivery_data), content_type='application/json')
    assert response.status_code == 201
    assert 'Delivery added successfully' in str(response.data)
    logger.info("test_add_delivery passed.")

# Tests d'erreurs
def test_invalid_beer_post(client):
    logger.info("Running test_invalid_beer_post...")
    beer_data = {
        'name': 'Invalid Beer',
        'price': 10.99,
        'brewery_id': 1
    }
    response = client.post('/beers/', data=json.dumps(beer_data), content_type='application/json')
    assert response.status_code == 400
    assert 'error' in str(response.data)
    logger.info("test_invalid_beer_post passed.")

def test_delete_non_existent_beer(client):
    logger.info("Running test_delete_non_existent_beer...")
    response = client.delete('/beers/9999')  # ID de bière qui n'existe pas
    assert response.status_code == 404
    assert 'Beer not found' in str(response.data)
    logger.info("test_delete_non_existent_beer passed.")
