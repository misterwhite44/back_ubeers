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
    return client

def delete_test_data(client):
    try:
        logger.info("Deleting test data...")

        res = client.get('/breweries/')
        assert res.status_code == 200, f"Failed to fetch breweries: {res.status_code}"
        breweries = res.get_json()
        for brewery in breweries:
            brewery_name = brewery['name']
            if brewery_name == "Integration Brewery":
                brewery_id = brewery['id']
                logger.info(f"Deleting brewery with name: {brewery_name} (ID: {brewery_id})")
                delete_res = client.delete(f'/breweries/{brewery_id}')
                if delete_res.status_code == 200:
                    logger.info(f"Brewery with name {brewery_name} deleted successfully.")
                else:
                    logger.warning(f"Failed to delete brewery {brewery_name}: {delete_res.status_code}")
        
        res = client.get('/beers/')
        assert res.status_code == 200, f"Failed to fetch beers: {res.status_code}"
        beers = res.get_json()
        for beer in beers:
            beer_name = beer['name']
            if beer_name == "Integration Beer":
                beer_id = beer['id']
                logger.info(f"Deleting beer with name: {beer_name} (ID: {beer_id})")
                delete_res = client.delete(f'/beers/{beer_id}')
                if delete_res.status_code == 200:
                    logger.info(f"Beer with name {beer_name} deleted successfully.")
                else:
                    logger.warning(f"Failed to delete beer {beer_name}: {delete_res.status_code}")
        
        logger.info("Test data deletion completed.")
    except Exception as e:
        logger.warning(f"Failed to delete test data: {e}")


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
    logger.info("Test 'test_create_and_get_beer' passed successfully.")
    delete_test_data(client)  # Supprimer les données après le test


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
    logger.info("Test 'test_create_and_get_brewery' passed successfully.")
    delete_test_data(client)  



# === TESTS DELIVERIES ===

def test_get_deliveries(client):
    logger.info("Running test_get_deliveries...")
    res = client.get('/deliveries/')
    assert res.status_code == 200, "GET /deliveries/ failed"
    deliveries = res.get_json()
    assert isinstance(deliveries, list), "Expected list of deliveries"
    logger.info("Test 'test_get_deliveries' passed successfully.")
    delete_test_data(client)  
