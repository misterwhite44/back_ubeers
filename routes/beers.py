from flask_restx import Namespace, Resource, fields
from models import db, Beer

beers_ns = Namespace("beers", description="Beers operations")

beer_model = beers_ns.model("Beer", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True),
    "type": fields.String,
    "degree": fields.Float,
    "brewery_id": fields.Integer,
    "image_url": fields.String  
})


@beers_ns.route("/")
class BeerList(Resource):
    @beers_ns.marshal_list_with(beer_model)
    def get(self):
        return Beer.query.all()

    @beers_ns.expect(beer_model)
    @beers_ns.marshal_with(beer_model, code=201)
    def post(self):
        data = beers_ns.payload
        beer = Beer(**data)
        db.session.add(beer)
        db.session.commit()
        return beer, 201

@beers_ns.route("/<int:id>")
@beers_ns.response(404, "Beer not found")
class BeerResource(Resource):
    @beers_ns.marshal_with(beer_model)
    def get(self, id):
        beer = Beer.query.get_or_404(id)
        return beer

    @beers_ns.expect(beer_model)
    @beers_ns.marshal_with(beer_model)
    def put(self, id):
        beer = Beer.query.get_or_404(id)
        for key, value in beers_ns.payload.items():
            setattr(beer, key, value)
        db.session.commit()
        return beer

    @beers_ns.response(204, "Beer deleted")
    def delete(self, id):
        beer = Beer.query.get_or_404(id)
        db.session.delete(beer)
        db.session.commit()
        return '', 204
