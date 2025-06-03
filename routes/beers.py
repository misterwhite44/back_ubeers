from flask import request, jsonify
from flask_restx import Resource

def register_beer_routes(api, ns_beers, r, beer_model, get_next_id, get_all_items):
    @ns_beers.route('/')
    class BeersList(Resource):
        @ns_beers.doc('list_beers')
        def get(self):
            beers = get_all_items(r, "beer")
            return jsonify(beers)

        @ns_beers.doc('add_beer')
        @ns_beers.expect(beer_model)
        def post(self):
            data = request.json
            beer_id = get_next_id(r, "beer")
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