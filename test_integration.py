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
        # Assurez-vous que la route /reset est définie dans votre app Flask.
        res = client.post('/reset/')
        assert res.status_code == 200  # Vérifiez que le reset renvoie un code de succès
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
    create_brewery(client)  # Créer une brasserie
    res = create_beer(client)  # Créer une bière
    assert res.status_code == 201  # Vérifier que la création de la bière a réussi
    logger.info("Beer creation successful with status code 201")

    res = client.get('/beers/')
    assert res.status_code == 200
    logger.info("GET /beers/ successful with status code 200")
    beers = res.get_json()
    assert any(b["name"] == "Integration Beer" for b in beers)  # Vérifier que la bière est présente
    logger.info("Beer found in GET /beers/ response")


# === TESTS BREWERIES ===

def test_create_and_get_brewery(client):
    logger.info("Running test_create_and_get_brewery...")
    res = create_brewery(client)
    assert res.status_code == 201
    logger.info("Brewery creation successful with status code 201")

    res = client.get('/breweries/')
    assert res.status_code == 200
    logger.info("GET /breweries/ successful with status code 200")
    breweries = res.get_json()
    assert any(b["name"] == "Integration Brewery" for b in breweries)  # Vérifier que la brasserie est présente
    logger.info("Brewery found in GET /breweries/ response")


# === TESTS DELIVERIES ===

def test_get_deliveries(client):
    logger.info("Running test_get_deliveries...")
    res = client.get('/deliveries/')
    assert res.status_code == 200  # Vérifier que la récupération des livraisons est réussie
    logger.info("GET /deliveries/ successful with status code 200")
    deliveries = res.get_json()
    assert isinstance(deliveries, list)  # Vérifier que la réponse est une liste
    logger.info("GET /deliveries/ response is a list")
