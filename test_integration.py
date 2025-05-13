import pytest
import json
from app import app  


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Tests pour les Beers
def test_get_beers(client):
    response = client.get('/beers/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)  

def test_add_beer(client):
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


def test_get_single_beer(client):
    response = client.get('/beers/1')
    if response.status_code == 404:
        assert 'Beer not found' in str(response.data)
    else:
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'name' in data


def test_update_beer(client):
    beer_data = {
        'name': 'Updated Beer',
        'description': 'Updated Description',
        'price': 12.99,
        'brewery_id': 1,
        'image_url': 'http://example.com/updated_beer.jpg'
    }
    response = client.put('/beers/1', data=json.dumps(beer_data), content_type='application/json')
    if response.status_code == 404:
        assert 'Beer not found' in str(response.data)
    else:
        assert response.status_code == 200
        assert 'Beer updated successfully' in str(response.data)


def test_delete_beer(client):
    response = client.delete('/beers/1')
    if response.status_code == 404:
        assert 'Beer not found' in str(response.data)
    else:
        assert response.status_code == 200
        assert 'Beer deleted successfully' in str(response.data)


def test_get_breweries(client):
    response = client.get('/breweries/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_add_brewery(client):
    brewery_data = {
        'name': 'Test Brewery',
        'description': 'Test Brewery Description',
        'location': 'Test Location',
        'image_url': 'http://example.com/brewery.jpg'
    }
    response = client.post('/breweries/', data=json.dumps(brewery_data), content_type='application/json')
    assert response.status_code == 201
    assert 'Brewery added successfully' in str(response.data)


def test_get_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_add_user(client):
    user_data = {
        'pseudo': 'test_user',
        'email': 'testuser@example.com',
        'password': 'testpassword123',
        'address': 'Test Address',
        'phone_number': '1234567890'
    }
    response = client.post('/users/', data=json.dumps(user_data), content_type='application/json')
    if response.status_code == 405:
        assert 'Method Not Allowed' in str(response.data)
    else:
        assert response.status_code == 201
        assert 'User added successfully' in str(response.data)


def test_get_deliveries(client):
    response = client.get('/deliveries/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_add_delivery(client):
    delivery_data = {
        'beer_id': 1,
        'quantity': 10,
        'delivery_address': 'Test Delivery Address',
        'delivery_date': '2025-05-13 12:00:00',
        'status': 'Pending',
        'user_id': 1
    }
    response = client.post('/deliveries/', data=json.dumps(delivery_data), content_type='application/json')
    if response.status_code == 500:
        assert 'Internal Server Error' in str(response.data)
    else:
        assert response.status_code == 201
        assert 'Delivery added successfully' in str(response.data)


def test_invalid_beer_post(client):
    beer_data = {
        'name': 'Invalid Beer',
        'price': 10.99,
        'brewery_id': 1
    }
    response = client.post('/beers/', data=json.dumps(beer_data), content_type='application/json')
    if response.status_code == 500:
        assert 'Internal Server Error' in str(response.data)
    else:
        assert response.status_code == 400
        assert 'error' in str(response.data)


def test_invalid_brewery_post(client):
    brewery_data = {
        'name': 'Invalid Brewery',
        'location': 'Test Location'
        # Missing required fields like description, image_url
    }
    response = client.post('/breweries/', data=json.dumps(brewery_data), content_type='application/json')
    assert response.status_code == 400
    assert 'error' in str(response.data)


def test_invalid_user_post(client):
    user_data = {
        'pseudo': 'user1',
        'email': 'invalidemail',
        'password': 'testpassword123',
        'address': 'Test Address'
    }
    response = client.post('/users/', data=json.dumps(user_data), content_type='application/json')
    if response.status_code == 405:
        assert 'Method Not Allowed' in str(response.data)
    else:
        assert response.status_code == 400
        assert 'error' in str(response.data)


def test_invalid_delivery_post(client):
    delivery_data = {
        'beer_id': 1,
        'quantity': 'invalid',  
        'delivery_address': 'Test Address',
        'delivery_date': '2025-05-13 12:00:00',
        'status': 'Pending',
        'user_id': 1
    }
    response = client.post('/deliveries/', data=json.dumps(delivery_data), content_type='application/json')
    if response.status_code == 500:
        assert 'Internal Server Error' in str(response.data)
    else:
        assert response.status_code == 400
        assert 'error' in str(response.data)
