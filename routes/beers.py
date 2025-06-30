from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from mysql.connector import Error
from app import get_db_connection  # importe la fonction de connexion depuis app.py

ns_beers = Namespace('beers', description='Beer Operations')

beer_model = ns_beers.model('Beer', {
    'name': fields.String(required=True, description='Name of the beer'),
    'description': fields.String(description='Description of the beer'),
    'price': fields.Float(required=True, description='Price of the beer'),
    'brewery_id': fields.Integer(required=True, description='ID of the brewery'),
    'image_url': fields.String(description='Image URL of the beer')
})

@ns_beers.route('/')
class BeersList(Resource):
    def get(self):
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM beers")
            beers = cursor.fetchall()
            return jsonify(beers)
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @ns_beers.expect(beer_model)
    def post(self):
        data = request.json
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO beers (name, description, price, brewery_id, image_url) VALUES (%s, %s, %s, %s, %s)",
                (data['name'], data.get('description'), data['price'], data['brewery_id'], data.get('image_url'))
            )
            connection.commit()
            return {'message': 'Beer added successfully'}, 201
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

@ns_beers.route('/<int:beer_id>')
class Beer(Resource):
    def get(self, beer_id):
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM beers WHERE id = %s", (beer_id,))
            beer = cursor.fetchone()
            if beer:
                return jsonify(beer)
            else:
                return {'message': 'Beer not found'}, 404
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @ns_beers.expect(beer_model)
    def put(self, beer_id):
        data = request.json
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE beers SET name = %s, description = %s, price = %s, brewery_id = %s, image_url = %s WHERE id = %s",
                (data['name'], data.get('description'), data['price'], data['brewery_id'], data.get('image_url'), beer_id)
            )
            connection.commit()
            if cursor.rowcount:
                return {'message': 'Beer updated successfully'}, 200
            else:
                return {'message': 'Beer not found'}, 404
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete(self, beer_id):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM beers WHERE id = %s", (beer_id,))
            connection.commit()
            if cursor.rowcount:
                return {'message': 'Beer deleted successfully'}, 200
            else:
                return {'message': 'Beer not found'}, 404
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
