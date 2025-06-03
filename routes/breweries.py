from flask import request, jsonify
from flask_restx import Resource

def register_brewery_routes(api, ns_breweries, r, brewery_model, get_next_id, get_all_items):
    @ns_breweries.route('/')
    class BreweriesList(Resource):
        def get(self):
            breweries = get_all_items(r, "brewery")
            return jsonify(breweries)

        @ns_breweries.expect(brewery_model)
        def post(self):
            data = request.json
            brewery_id = get_next_id(r, "brewery")
            brewery_key = f"brewery:{brewery_id}"
            r.hset(brewery_key, mapping={
                "id": brewery_id,
                "name": data['name'],
                "description": data.get('description', ''),
                "location": data.get('location', ''),
                "image_url": data.get('image_url', '')
            })
            return {'message': 'Brewery added successfully', 'id': brewery_id}, 201

    @ns_breweries.route('/<int:brewery_id>')
    class Brewery(Resource):
        def get(self, brewery_id):
            brewery_key = f"brewery:{brewery_id}"
            if not r.exists(brewery_key):
                return {'message': 'Brewery not found'}, 404
            brewery = r.hgetall(brewery_key)
            brewery['id'] = int(brewery['id'])
            return jsonify(brewery)

        @ns_breweries.expect(brewery_model)
        def put(self, brewery_id):
            brewery_key = f"brewery:{brewery_id}"
            if not r.exists(brewery_key):
                return {'message': 'Brewery not found'}, 404
            data = request.json
            r.hset(brewery_key, mapping={
                "name": data['name'],
                "description": data.get('description', ''),
                "location": data.get('location', ''),
                "image_url": data.get('image_url', '')
            })
            return {'message': 'Brewery updated successfully'}, 200

        def delete(self, brewery_id):
            brewery_key = f"brewery:{brewery_id}"
            if r.delete(brewery_key):
                return {'message': 'Brewery deleted successfully'}, 200
            else:
                return {'message': 'Brewery not found'}, 404