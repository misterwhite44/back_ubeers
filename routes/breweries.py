from flask_restx import Namespace, Resource, fields
from models import db, Brewery

breweries_ns = Namespace("breweries", description="Brewery operations")

brewery_model = breweries_ns.model("Brewery", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True),
    "description": fields.String,
    "location": fields.String,
    "image_url": fields.String
})

@breweries_ns.route("/")
class BreweryList(Resource):
    @breweries_ns.marshal_list_with(brewery_model)
    def get(self):
        return Brewery.query.all()

    @breweries_ns.expect(brewery_model)
    @breweries_ns.marshal_with(brewery_model, code=201)
    def post(self):
        data = breweries_ns.payload
        brewery = Brewery(**data)
        db.session.add(brewery)
        db.session.commit()
        return brewery, 201

@breweries_ns.route("/<int:id>")
@breweries_ns.response(404, "Brewery not found")
class BreweryResource(Resource):
    @breweries_ns.marshal_with(brewery_model)
    def get(self, id):
        return Brewery.query.get_or_404(id)

    @breweries_ns.expect(brewery_model)
    @breweries_ns.marshal_with(brewery_model)
    def put(self, id):
        brewery = Brewery.query.get_or_404(id)
        for key, value in breweries_ns.payload.items():
            setattr(brewery, key, value)
        db.session.commit()
        return brewery

    @breweries_ns.response(204, "Brewery deleted")
    def delete(self, id):
        brewery = Brewery.query.get_or_404(id)
        db.session.delete(brewery)
        db.session.commit()
        return '', 204
