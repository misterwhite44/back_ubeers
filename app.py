from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://50b825ff6e0cfee1b611665ae0c76147@o4509332960509952.ingest.de.sentry.io/4509587000655952",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0  # Attention : à réduire en prod si nécessaire
)


app = Flask(__name__)

#CORS(app, resources={r"/*": {"origins": "https://ubeer-jade.vercel.app"}})
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
api = Api(app, version='1.0', title='Ubeers API',
          description='API for managing beers, breweries, deliveries, and users')

ns_beers = api.namespace('beers', description='Beer Operations')
ns_breweries = api.namespace('breweries', description='Brewery Operations')
ns_users = api.namespace('users', description='User Operations')

DB_HOST = "bwawmx4ntfjwzxxrotz4-mysql.services.clever-cloud.com"
DB_PORT = 3306
DB_USER = "uuw6sv5bvs11qa51"
DB_PASSWORD = "md1HTCoAHEg0s4HbJHGc"
DB_NAME = "bwawmx4ntfjwzxxrotz4"
DB_CHARSET = 'utf8mb4'



beer_model = api.model('Beer', {
    'name': fields.String(required=True, description='Name of the beer'),
    'description': fields.String(description='Description of the beer'),
    'price': fields.Float(required=True, description='Price of the beer'),
    'brewery_id': fields.Integer(required=True, description='ID of the brewery'),
    'image_url': fields.String(description='Image URL of the beer')
})


brewery_model = api.model('Brewery', {
    'id': fields.Integer(description='ID of the brewery'),
    'name': fields.String(required=True, description='Name of the brewery'),
    'description': fields.String(description='Description of the brewery'),
    'location': fields.String(description='Location of the brewery'),
    'image_url': fields.String(description='Image URL of the brewery')
})

user_model = api.model('User', {
    'pseudo': fields.String(required=True, description='Pseudo of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'address': fields.String(description='Address of the user'),
    'phone_number': fields.String(description='Phone number of the user'),
})

def get_db_connection():
    """Establish and return a database connection."""
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset=DB_CHARSET
    )


@ns_beers.route('/')
class BeersList(Resource):
    @ns_beers.doc('list_beers')
    def get(self):
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM beers")
            beers = cursor.fetchall()

            for beer in beers:
                if 'image_url' in beer and beer['image_url']:
                    beer['image_url'] = beer['image_url']

            return jsonify(beers)
        except Error as e:
            sentry_sdk.capture_exception(e)# Envoi de l'exception à Sentry
            print(f"Error fetching beers: {e}")
            return {'error': str(e)}, 500
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    @ns_beers.doc('add_beer')
    @ns_beers.expect(beer_model)
    def post(self):
        """
        Add a new beer to the database
        """
        data = request.json
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO beers (name, description, price, brewery_id, image_url)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (data['name'], data['description'], data['price'], data['brewery_id'], data['image_url'])
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
    @ns_beers.doc('get_beer')
    def get(self, beer_id):
        """
        Fetch a beer by its ID
        """
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

    @ns_beers.doc('update_beer')
    @ns_beers.expect(beer_model)
    def put(self, beer_id):
        """
        Update a beer by its ID
        """
        data = request.json
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE beers SET name = %s, description = %s, price = %s, brewery_id = %s, image_url = %s WHERE id = %s",
                (data['name'], data['description'], data['price'], data['brewery_id'], data.get('image_url'), beer_id)
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



    @ns_beers.doc('delete_beer')

    def delete(self, beer_id):
   
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

        # Exécution de la requête DELETE pour supprimer la bière avec l'ID spécifié
            cursor.execute("DELETE FROM beers WHERE id = %s", (beer_id,))

        # Validation des changements dans la base de données
            connection.commit()

        # Vérification si une ligne a été affectée, ce qui signifie que la bière a été supprimée
            if cursor.rowcount > 0:
                return {'message': 'Beer deleted successfully'}, 200
            else:
                return {'message': 'Beer not found'}, 404

        except Error as e:
        # Si une erreur se produit, on la capture et retourne une erreur serveur
            return {'error': str(e)}, 500

        finally:
        # Fermeture de la connexion et du curseur si la connexion est encore ouverte
            if connection.is_connected():
                cursor.close()
                connection.close()


@ns_breweries.route('/')
class BreweriesList(Resource):
    @ns_breweries.doc('list_breweries')
    def get(self):
        """
        Fetch all breweries from the database
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM breweries")
            breweries = cursor.fetchall()
            
            # Vérification que les URLs d'images sont valides
            for brewery in breweries:
                if 'image_url' in brewery and brewery['image_url']:
                    brewery['image_url'] = brewery['image_url']
            
            return jsonify(breweries)
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @ns_breweries.doc('add_brewery')
    @ns_breweries.expect(brewery_model)
    def post(self):
        """
        Add a new brewery to the database
        """
        data = request.json
        
        # Validation des données
        name = data.get('name')
        description = data.get('description')
        location = data.get('location')
        image_url = data.get('image_url')
        
        if not name:
            return {'error': 'The field "name" is required.'}, 400
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO breweries (name, description, location, image_url)
                VALUES (%s, %s, %s, %s)
                """,
                (name, description, location, image_url)
            )
            connection.commit()
            return {'message': 'Brewery added successfully'}, 201
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

@ns_breweries.route('/<int:brewery_id>')
class Brewery(Resource):
    @ns_breweries.doc('get_brewery')
    def get(self, brewery_id):
        """
        Fetch a brewery by its ID
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM breweries WHERE id = %s", (brewery_id,))
            brewery = cursor.fetchone()
            if brewery:
                # Vérification que l'URL de l'image est valide
                if 'image_url' in brewery and brewery['image_url']:
                    brewery['image_url'] = brewery['image_url']
                return jsonify(brewery)
            else:
                return {'message': 'Brewery not found'}, 404
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    #delete
    @ns_breweries.doc('delete_brewery')
    def delete(self, brewery_id):
        """
        Delete a brewery by its ID
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM breweries WHERE id = %s", (brewery_id,))
            connection.commit()
            if cursor.rowcount:
                return {'message': 'Brewery deleted successfully'}, 200
            else:
                return {'message': 'Brewery not found'}, 404
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                

@ns_users.route('/')
class UsersList(Resource):
    @ns_users.doc('list_users')
    def get(self):
        """
        Fetch all users from the database
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            
            # Ajout du log pour vérifier les utilisateurs récupérés
            print("Utilisateurs récupérés:", users)  # Affiche les utilisateurs dans les logs du serveur
            
            return jsonify(users)
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


@ns_users.route('/<int:user_id>')
class User(Resource):
    @ns_users.doc('get_user')
    def get(self, user_id):
        """
        Fetch a user by its ID
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            
            if user:
                return jsonify(user)
            else:
                return {'message': 'User not found'}, 404
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

#deliveries

delivery_model = api.model('Delivery', {
    'beer_id': fields.Integer(required=True, description='ID of the beer being delivered'),
    'quantity': fields.Integer(required=True, description='Quantity of the beer being delivered'),
    'delivery_address': fields.String(required=True, description='Delivery address'),
    'delivery_date': fields.String(required=True, description='Date and time of delivery'),
    'status': fields.String(enum=['Pending', 'Delivered', 'Cancelled'], default='Pending', description='Delivery status'),
    'user_id': fields.Integer(required=True, description='ID of the user receiving the delivery')
})

ns_deliveries = api.namespace('deliveries', description='Delivery Operations')

@ns_deliveries.route('/')
class DeliveriesList(Resource):
    @ns_deliveries.doc('list_deliveries')
    def get(self):
        """
        Fetch all deliveries from the database
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM deliveries")
            deliveries = cursor.fetchall()
            return jsonify(deliveries)
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @ns_deliveries.doc('add_delivery')
    @ns_deliveries.expect(delivery_model)
    def post(self):
        """
        Add a new delivery to the database
        """
        data = request.json
        
        # Extraction des données de la livraison
        beer_id = data.get('beer_id')
        quantity = data.get('quantity')
        delivery_address = data.get('delivery_address')
        delivery_date = data.get('delivery_date')
        status = data.get('status', 'Pending')  # Défaut à "Pending" si non précisé
        user_id = data.get('user_id')
        
        if not beer_id or not quantity or not delivery_address or not delivery_date or not user_id:
            return {'error': 'Tous les champs sont requis'}, 400
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO deliveries (beer_id, quantity, delivery_address, delivery_date, status, user_id) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (beer_id, quantity, delivery_address, delivery_date, status, user_id)
            )
            connection.commit()
            return {'message': 'Delivery added successfully'}, 201
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

@ns_deliveries.route('/<int:delivery_id>')
class Delivery(Resource):
    @ns_deliveries.doc('get_delivery')
    def get(self, delivery_id):
        """
        Fetch a delivery by its ID
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM deliveries WHERE id = %s", (delivery_id,))
            delivery = cursor.fetchone()
            if delivery:
                return jsonify(delivery)
            else:
                return {'message': 'Delivery not found'}, 404
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @ns_deliveries.doc('update_delivery')
    @ns_deliveries.expect(delivery_model)
    def put(self, delivery_id):
        """
        Update a delivery by its ID
        """
        data = request.json
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE deliveries SET beer_id = %s, quantity = %s, delivery_address = %s, "
                "delivery_date = %s, status = %s, user_id = %s WHERE id = %s",
                (data['beer_id'], data['quantity'], data['delivery_address'], data['delivery_date'], 
                 data['status'], data['user_id'], delivery_id)
            )
            connection.commit()
            if cursor.rowcount:
                return {'message': 'Delivery updated successfully'}, 200
            else:
                return {'message': 'Delivery not found'}, 404
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @ns_deliveries.doc('delete_delivery')
    def delete(self, delivery_id):
        """
        Delete a delivery by its ID
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM deliveries WHERE id = %s", (delivery_id,))
            connection.commit()
            if cursor.rowcount:
                return {'message': 'Delivery deleted successfully'}, 200
            else:
                return {'message': 'Delivery not found'}, 404
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()



if __name__ == '__main__':
    app.run(debug=False)

