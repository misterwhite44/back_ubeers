from flask_restx import fields

def register_models(api):
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

    return beer_model, brewery_model, user_model, delivery_model