from flask_restx import Namespace, Resource, fields
from models import db, Brewery

api = Namespace("breweries", description="Brewery operations")

brewery_model = api.model("Brewery", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True),
    "country": fields.String
})

@api.route("/")
class BreweryList(Resource):
    @api.marshal_list_with(brewery_model)
    def get(self):
        return Brewery.query.all()

    @api.expect(brewery_model)
    @api.marshal_with(brewery_model, code=201)
    def post(self):
        data = api.payload
        brewery = Brewery(**data)
        db.session.add(brewery)
        db.session.commit()
        return brewery, 201

@api.route("/<int:id>")
@api.response(404, "Brewery not found")
class BreweryResource(Resource):
    @api.marshal_with(brewery_model)
    def get(self, id):
        return Brewery.query.get_or_404(id)

    @api.expect(brewery_model)
    @api.marshal_with(brewery_model)
    def put(self, id):
        brewery = Brewery.query.get_or_404(id)
        for key, value in api.payload.items():
            setattr(brewery, key, value)
        db.session.commit()
        return brewery

    @api.response(204, "Brewery deleted")
    def delete(self, id):
        brewery = Brewery.query.get_or_404(id)
        db.session.delete(brewery)
        db.session.commit()
        return '', 204
