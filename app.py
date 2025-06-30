from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

from config import SQLALCHEMY_DATABASE_URI

from routes.beers import register_beer_routes
from routes.breweries import register_brewery_routes
from routes.users import register_user_routes
from routes.deliveries import register_delivery_routes

app = Flask(__name__)
front_url = os.getenv("FRONT_URL")
CORS(app, resources={r"/*": {"origins": front_url}})

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', front_url)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

api = Api(app, version='1.0', title='Ubeers API',
          description='API for managing beers, breweries, deliveries, and users')

ns_beers = api.namespace('beers', description='Beer Operations')
ns_breweries = api.namespace('breweries', description='Brewery Operations')
ns_users = api.namespace('users', description='User Operations')
ns_deliveries = api.namespace('deliveries', description='Delivery Operations')

# Import models and register routes
from models import Beer, Brewery, User, Delivery

register_beer_routes(api, ns_beers, db, Beer)
register_brewery_routes(api, ns_breweries, db, Brewery)
register_user_routes(api, ns_users, db, User)
register_delivery_routes(api, ns_deliveries, db, Delivery)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
