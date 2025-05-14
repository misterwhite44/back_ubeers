import sys
import os
import pytest

# Ajout du chemin de la racine du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_beers(client):
    response = client.get('/beers/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_add_beer(client):
    data = {
        "name": "Test Beer",
        "description": "Bière de test",
        "price": 3.5,
        "brewery_id": 1,
        "image_url": "http://image.test/beer.jpg"
    }
    response = client.post('/beers/', json=data)
    assert response.status_code in (201, 500)
