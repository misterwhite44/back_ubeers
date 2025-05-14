import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    reset_database(client)
    return client

def reset_database(client):
    try:
        client.post('/reset/')
    except:
        pass  # Pas grave si pas implémenté

# === UTILITAIRES ===

def create_brewery(client, name="Integration Brewery"):
    return client.post('/breweries/', json={
        "name": name,
        "description": "Test brewery",
        "location": "Test City",
        "image_url": "http://example.com/brewery.jpg"
    })

def create_beer(client, brewery_id=1, name="Integration Beer"):
    return client.post('/beers/', json={
        "name": name,
        "description": "Test beer",
        "price": 5.0,
        "brewery_id": brewery_id,
        "image_url": "http://example.com/beer.jpg"
    })

# === TESTS BEERS ===

def test_create_and_get_beer(client):
    create_brewery(client)
    res = create_beer(client)
    assert res.status_code == 201

    res = client.get('/beers/')
    assert res.status_code == 200
    beers = res.get_json()
    assert any(b["name"] == "Integration Beer" for b in beers)

def test_beer_creation_missing_name(client):
    create_brewery(client)
    res = client.post('/beers/', json={
        "description": "Missing name",
        "price": 4.5,
        "brewery_id": 1,
        "image_url": "http://example.com/beer.jpg"
    })
    assert res.status_code in [400, 422]

# === TESTS BREWERIES ===

def test_create_and_get_brewery(client):
    res = create_brewery(client)
    assert res.status_code == 201

    res = client.get('/breweries/')
    assert res.status_code == 200
    breweries = res.get_json()
    assert any(b["name"] == "Integration Brewery" for b in breweries)

def test_duplicate_brewery_name(client):
    create_brewery(client, name="Dup")
    res = create_brewery(client, name="Dup")
    assert res.status_code in [400, 409]

# === TESTS DELIVERIES ===

def test_get_deliveries(client):
    res = client.get('/deliveries/')
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
