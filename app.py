from flask import Flask
from flask_restx import Api
from flask_cors import CORS
import redis
import os

from models import register_models
from utils import get_next_id, get_all_items

from routes.beers import register_beer_routes
from routes.breweries import register_brewery_routes
from routes.users import register_user_routes
from routes.deliveries import register_delivery_routes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://ubeer-jade.vercel.app"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://ubeer-jade.vercel.app')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

api = Api(app, version='1.0', title='Ubeers API',
          description='API for managing beers, breweries, deliveries, and users')

ns_beers = api.namespace('beers', description='Beer Operations')
ns_breweries = api.namespace('breweries', description='Brewery Operations')
ns_users = api.namespace('users', description='User Operations')
ns_deliveries = api.namespace('deliveries', description='Delivery Operations')

redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url, decode_responses=True)

beer_model, brewery_model, user_model, delivery_model = register_models(api)

register_beer_routes(api, ns_beers, r, beer_model, get_next_id, get_all_items)
register_brewery_routes(api, ns_breweries, r, brewery_model, get_next_id, get_all_items)
register_user_routes(api, ns_users, r, user_model, get_next_id, get_all_items)
register_delivery_routes(api, ns_deliveries, r, delivery_model, get_next_id, get_all_items)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
