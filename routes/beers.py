from flask_restx import Namespace, Resource, fields
from models import db, Beer

api = Namespace("beers", description="Beers operations")

beer_model = api.model("Beer", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True),
    "type": fields.String,
    "degree": fields.Float,
    "brewery_id": fields.Integer
})

@api.route("/")
class BeerList(Resource):
    @api.marshal_list_with(beer_model)
    def get(self):
        return Beer.query.all()

    @api.expect(beer_model)
    @api.marshal_with(beer_model, code=201)
    def post(self):
        data = api.payload
        beer = Beer(**data)
        db.session.add(beer)
        db.session.commit()
        return beer, 201

@api.route("/<int:id>")
@api.response(404, "Beer not found")
class BeerResource(Resource):
    @api.marshal_with(beer_model)
    def get(self, id):
        beer = Beer.query.get_or_404(id)
        return beer

    @api.expect(beer_model)
    @api.marshal_with(beer_model)
    def put(self, id):
        beer = Beer.query.get_or_404(id)
        for key, value in api.payload.items():
            setattr(beer, key, value)
        db.session.commit()
        return beer

    @api.response(204, "Beer deleted")
    def delete(self, id):
        beer = Beer.query.get_or_404(id)
        db.session.delete(beer)
        db.session.commit()
        return '', 204
