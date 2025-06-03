from flask import request, jsonify
from flask_restx import Resource

def register_user_routes(api, ns_users, r, user_model, get_next_id, get_all_items):
    @ns_users.route('/')
    class UsersList(Resource):
        def get(self):
            users = get_all_items(r, "user")
            return jsonify(users)

        @ns_users.expect(user_model)
        def post(self):
            data = request.json
            user_id = get_next_id(r, "user")
            user_key = f"user:{user_id}"
            r.hset(user_key, mapping={
                "id": user_id,
                "pseudo": data['pseudo'],
                "email": data['email'],
                "password": data['password'],
                "address": data.get('address', ''),
                "phone_number": data.get('phone_number', '')
            })
            return {'message': 'User added successfully', 'id': user_id}, 201

    @ns_users.route('/<int:user_id>')
    class User(Resource):
        def get(self, user_id):
            user_key = f"user:{user_id}"
            if not r.exists(user_key):
                return {'message': 'User not found'}, 404
            user = r.hgetall(user_key)
            user['id'] = int(user['id'])
            return jsonify(user)

        @ns_users.expect(user_model)
        def put(self, user_id):
            user_key = f"user:{user_id}"
            if not r.exists(user_key):
                return {'message': 'User not found'}, 404
            data = request.json
            r.hset(user_key, mapping={
                "pseudo": data['pseudo'],
                "email": data['email'],
                "password": data['password'],
                "address": data.get('address', ''),
                "phone_number": data.get('phone_number', '')
            })
            return {'message': 'User updated successfully'}, 200

        def delete(self, user_id):
            user_key = f"user:{user_id}"
            if r.delete(user_key):
                return {'message': 'User deleted successfully'}, 200
            else:
                return {'message': 'User not found'}, 404