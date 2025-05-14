import pytest
import logging
from app import app

# Configuration de logging avec un niveau DEBUG pour tout afficher
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    reset_database(client)
    return client

def reset_database(client):
    try:
        logger.info("Resetting the database...")
        res = client.post('/reset/')
        assert res.status_code == 200, "Database reset failed"
        logger.info("Database reset completed.")
    except Exception as e:
        logger.warning(f"Database reset failed: {e}")

# === UTILITAIRES ===

def create_brewery(client, name="Integration Brewery"):
    logger.info(f"Creating brewery: {name}")
    res = client.post('/breweries/', json={
        "name": name,
        "description": "Test brewery",
        "location": "Test City",
        "image_url": "http://example.com/brewery.jpg"
    })
    logger.debug(f"Brewery creation response: {res.status_code}")
    return res

def create_beer(client, brewery_id=1, name="Integration Beer"):
    logger.info(f"Creating beer: {name}, Brewery ID: {brewery_id}")
    res = client.post('/beers/', json={
        "name": name,
        "description": "Test beer",
        "price": 5.0,
        "brewery_id": brewery_id,
        "image_url": "http://example.com/beer.jpg"
    })
    logger.debug(f"Beer creation response: {res.status_code}")
    return res

# === TESTS BEERS ===

def test_create_and_get_beer(client):
    logger.info("Running test_create_and_get_beer...")
    assert create_brewery(client).status_code == 201, "Failed to create brewery"
    res = create_beer(client)
    assert res.status_code == 201, "Failed to create beer"

    res = client.get('/beers/')
    assert res.status_code == 200, "GET /beers/ failed"
    beers = res.get_json()
    assert isinstance(beers, list), "Expected list of beers"
    assert any(b["name"] == "Integration Beer" for b in beers), "Beer not found"

def test_beer_creation_missing_name(client):
    logger.info("Running test_beer_creation_missing_name...")
    create_brewery(client)
    res = client.post('/beers/', json={
        "description": "Missing name",
        "price": 4.5,
        "brewery_id": 1,
        "image_url": "http://example.com/beer.jpg"
    })
    assert res.status_code in [400, 422], f"Expected 400 or 422, got {res.status_code}"

# === TESTS BREWERIES ===

def test_create_and_get_brewery(client):
    logger.info("Running test_create_and_get_brewery...")
    res = create_brewery(client)
    assert res.status_code == 201, "Brewery creation failed"

    res = client.get('/breweries/')
    assert res.status_code == 200, "GET /breweries/ failed"
    breweries = res.get_json()
    assert isinstance(breweries, list), "Expected list of breweries"
    assert any(b["name"] == "Integration Brewery" for b in breweries), "Brewery not found"

def test_duplicate_brewery_name(client):
    logger.info("Running test_duplicate_brewery_name...")
    assert create_brewery(client, name="Dup").status_code == 201
    res = create_brewery(client, name="Dup")
    assert res.status_code in [400, 409], f"Expected 400 or 409, got {res.status_code}"

# === TESTS DELIVERIES ===

def test_get_deliveries(client):
    logger.info("Running test_get_deliveries...")
    res = client.get('/deliveries/')
    assert res.status_code == 200, "GET /deliveries/ failed"
    deliveries = res.get_json()
    assert isinstance(deliveries, list), "Expected list of deliveries"
