from flask import request, jsonify
from flask_restx import Resource

def register_delivery_routes(api, ns_deliveries, r, delivery_model, get_next_id, get_all_items):
    @ns_deliveries.route('/')
    class DeliveriesList(Resource):
        def get(self):
            deliveries = get_all_items(r, "delivery")
            return jsonify(deliveries)

        @ns_deliveries.expect(delivery_model)
        def post(self):
            data = request.json
            delivery_id = get_next_id(r, "delivery")
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

    @ns_deliveries.route('/<int:delivery_id>')
    class Delivery(Resource):
        def get(self, delivery_id):
            delivery_key = f"delivery:{delivery_id}"
            if not r.exists(delivery_key):
                return {'message': 'Delivery not found'}, 404
            delivery = r.hgetall(delivery_key)
            delivery['id'] = int(delivery['id'])
            delivery['beer_id'] = int(delivery['beer_id'])
            delivery['quantity'] = int(delivery['quantity'])
            delivery['user_id'] = int(delivery['user_id'])
            return jsonify(delivery)

        @ns_deliveries.expect(delivery_model)
        def put(self, delivery_id):
            delivery_key = f"delivery:{delivery_id}"
            if not r.exists(delivery_key):
                return {'message': 'Delivery not found'}, 404
            data = request.json
            r.hset(delivery_key, mapping={
                "beer_id": data['beer_id'],
                "quantity": data['quantity'],
                "delivery_address": data['delivery_address'],
                "delivery_date": data['delivery_date'],
                "status": data.get('status', 'Pending'),
                "user_id": data['user_id']
            })
            return {'message': 'Delivery updated successfully'}, 200

        def delete(self, delivery_id):
            delivery_key = f"delivery:{delivery_id}"
            if r.delete(delivery_key):
                return {'message': 'Delivery deleted successfully'}, 200
            else:
                return {'message': 'Delivery not found'}, 404