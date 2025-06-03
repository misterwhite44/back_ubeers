from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import os
from dotenv import load_dotenv
import redis
import json

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

api = Api(app, version='1.0', title='Ubeers API',
          description='API for managing beers, breweries, deliveries, and users')

ns_beers = api.namespace('beers', description='Beer Operations')
ns_breweries = api.namespace('breweries', description='Brewery Operations')
ns_users = api.namespace('users', description='User Operations')
ns_deliveries = api.namespace('deliveries', description='Delivery Operations')

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

# Modèles Flask-RESTx (inchangés)
beer_model = api.model('Beer', {
    'name': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'brewery_id': fields.Integer(required=True),
    'image_url': fields.String
})

brewery_model = api.model('Brewery', {
    'id': fields.Integer,
    'name': fields.String(required=True),
    'description': fields.String,
    'location': fields.String,
    'image_url': fields.String
})

user_model = api.model('User', {
    'pseudo': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'address': fields.String,
    'phone_number': fields.String,
})

delivery_model = api.model('Delivery', {
    'beer_id': fields.Integer(required=True),
    'quantity': fields.Integer(required=True),
    'delivery_address': fields.String(required=True),
    'delivery_date': fields.String(required=True),
    'status': fields.String(enum=['Pending', 'Delivered', 'Cancelled'], default='Pending'),
    'user_id': fields.Integer(required=True)
})

def get_next_id(key):
    return r.incr(f"id:{key}")

def get_all_items(prefix):
    keys = r.keys(f"{prefix}:*")
    items = []
    for key in keys:
        item = r.hgetall(key)
        # Convert types (ex: price as float, ids as int)
        for k, v in item.items():
            if k.endswith('_id') or k == 'id' or k == 'quantity' or k == 'user_id' or k == 'brewery_id' or k == 'beer_id':
                item[k] = int(v)
            elif k == 'price':
                item[k] = float(v)
        items.append(item)
    return items

@ns_beers.route('/')
class BeersList(Resource):
    @ns_beers.doc('list_beers')
    def get(self):
        beers = get_all_items("beer")
        return jsonify(beers)

    @ns_beers.doc('add_beer')
    @ns_beers.expect(beer_model)
    def post(self):
        data = request.json
        beer_id = get_next_id("beer")
        beer_key = f"beer:{beer_id}"
        r.hset(beer_key, mapping={
            "id": beer_id,
            "name": data['name'],
            "description": data.get('description', ''),
            "price": data['price'],
            "brewery_id": data['brewery_id'],
            "image_url": data.get('image_url', '')
        })
        return {'message': 'Beer added successfully', 'id': beer_id}, 201

@ns_beers.route('/<int:beer_id>')
class Beer(Resource):
    @ns_beers.doc('get_beer')
    def get(self, beer_id):
        beer_key = f"beer:{beer_id}"
        if not r.exists(beer_key):
            return {'message': 'Beer not found'}, 404
        beer = r.hgetall(beer_key)
        # Convert types
        beer['id'] = int(beer['id'])
        beer['brewery_id'] = int(beer['brewery_id'])
        beer['price'] = float(beer['price'])
        return jsonify(beer)

    @ns_beers.doc('update_beer')
    @ns_beers.expect(beer_model)
    def put(self, beer_id):
        beer_key = f"beer:{beer_id}"
        if not r.exists(beer_key):
            return {'message': 'Beer not found'}, 404
        data = request.json
        r.hset(beer_key, mapping={
            "name": data['name'],
            "description": data.get('description', ''),
            "price": data['price'],
            "brewery_id": data['brewery_id'],
            "image_url": data.get('image_url', '')
        })
        return {'message': 'Beer updated successfully'}, 200

    @ns_beers.doc('delete_beer')
    def delete(self, beer_id):
        beer_key = f"beer:{beer_id}"
        if r.delete(beer_key):
            return {'message': 'Beer deleted successfully'}, 200
        else:
            return {'message': 'Beer not found'}, 404

@ns_breweries.route('/')
class BreweriesList(Resource):
    @ns_breweries.doc('list_breweries')
    def get(self):
        breweries = get_all_items("brewery")
        return jsonify(breweries)

    @ns_breweries.doc('add_brewery')
    @ns_breweries.expect(brewery_model)
    def post(self):
        data = request.json
        name = data.get('name')
        if not name:
            return {'error': 'The field "name" is required.'}, 400
        brewery_id = get_next_id("brewery")
        brewery_key = f"brewery:{brewery_id}"
        r.hset(brewery_key, mapping={
            "id": brewery_id,
            "name": name,
            "description": data.get('description', ''),
            "location": data.get('location', ''),
            "image_url": data.get('image_url', '')
        })
        return {'message': 'Brewery added successfully', 'id': brewery_id}, 201

@ns_breweries.route('/<int:brewery_id>')
class Brewery(Resource):
    @ns_breweries.doc('get_brewery')
    def get(self, brewery_id):
        brewery_key = f"brewery:{brewery_id}"
        if not r.exists(brewery_key):
            return {'message': 'Brewery not found'}, 404
        brewery = r.hgetall(brewery_key)
        brewery['id'] = int(brewery['id'])
        return jsonify(brewery)

    @ns_breweries.doc('delete_brewery')
    def delete(self, brewery_id):
        brewery_key = f"brewery:{brewery_id}"
        if r.delete(brewery_key):
            return {'message': 'Brewery deleted successfully'}, 200
        else:
            return {'message': 'Brewery not found'}, 404

@ns_users.route('/')
class UsersList(Resource):
    @ns_users.doc('list_users')
    def get(self):
        users = get_all_items("user")
        return jsonify(users)

    @ns_users.route('/<int:user_id>')
    class User(Resource):
        @ns_users.doc('get_user')
        def get(self, user_id):
            user_key = f"user:{user_id}"
            if not r.exists(user_key):
                return {'message': 'User not found'}, 404
            user = r.hgetall(user_key)
            user['id'] = int(user['id'])
            return jsonify(user)

@ns_users.route('/<int:user_id>')
class User(Resource):
    @ns_users.doc('get_user')
    def get(self, user_id):
        user_key = f"user:{user_id}"
        if not r.exists(user_key):
            return {'message': 'User not found'}, 404
        user = r.hgetall(user_key)
        user['id'] = int(user['id'])
        return jsonify(user)

@ns_deliveries.route('/')
class DeliveriesList(Resource):
    @ns_deliveries.doc('list_deliveries')
    def get(self):
        deliveries = get_all_items("delivery")
        return jsonify(deliveries)

    @ns_deliveries.doc('add_delivery')
    @ns_deliveries.expect(delivery_model)
    def post(self):
        data = request.json
        delivery_id = get_next_id("delivery")
        delivery_key = f"delivery:{delivery_id}"
        r.hset(delivery_key, mapping={
            "id": delivery_id,
            "beer_id": data['beer_id'],
            "quantity": data['quantity'],
            "delivery_address": data['delivery_address'],
            "delivery_date": data['delivery_date'],
            "status": data.get('status', 'Pending'),
            "user_id": data['user_id']
        })
        return {'message': 'Delivery added successfully', 'id': delivery_id}, 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
