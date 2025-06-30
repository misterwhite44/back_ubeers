from flask_restx import Namespace, Resource, fields
from models import db, Beer
import json
from app import redis_client  # importer le client Redis depuis app.py
from extensions import redis_client


beers_ns = Namespace("beers", description="Beers operations")

beer_model = beers_ns.model("Beer", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True),
    "type": fields.String,
    "degree": fields.Float,
    "brewery_id": fields.Integer,
    "image_url": fields.String  
})

def serialize_beer(beer):
    return {
        "id": beer.id,
        "name": beer.name,
        "type": beer.type,
        "degree": beer.degree,
        "brewery_id": beer.brewery_id,
        "image_url": beer.image_url
    }

@beers_ns.route("/")
class BeerList(Resource):
    @beers_ns.marshal_list_with(beer_model)
    def get(self):
        cached = redis_client.get("beers_all")
        if cached:
            beers = json.loads(cached)
            return beers
        beers = Beer.query.all()
        beers_data = [serialize_beer(b) for b in beers]
        redis_client.set("beers_all", json.dumps(beers_data), ex=300)  # cache 5 min
        return beers_data

    @beers_ns.expect(beer_model)
    @beers_ns.marshal_with(beer_model, code=201)
    def post(self):
        data = beers_ns.payload
        beer = Beer(**data)
        db.session.add(beer)
        db.session.commit()
        redis_client.delete("beers_all")  # invalider cache liste
        return serialize_beer(beer), 201

@beers_ns.route("/<int:id>")
@beers_ns.response(404, "Beer not found")
class BeerResource(Resource):
    @beers_ns.marshal_with(beer_model)
    def get(self, id):
        cached = redis_client.get(f"beer_{id}")
        if cached:
            return json.loads(cached)
        beer = Beer.query.get_or_404(id)
        beer_data = serialize_beer(beer)
        redis_client.set(f"beer_{id}", json.dumps(beer_data), ex=300)  # cache 5 min
        return beer_data

    @beers_ns.expect(beer_model)
    @beers_ns.marshal_with(beer_model)
    def put(self, id):
        beer = Beer.query.get_or_404(id)
        for key, value in beers_ns.payload.items():
            setattr(beer, key, value)
        db.session.commit()
        redis_client.delete(f"beer_{id}")
        redis_client.delete("beers_all")  # invalider cache liste
        return serialize_beer(beer)

    @beers_ns.response(204, "Beer deleted")
    def delete(self, id):
        beer = Beer.query.get_or_404(id)
        db.session.delete(beer)
        db.session.commit()
        redis_client.delete(f"beer_{id}")
        redis_client.delete("beers_all")  # invalider cache liste
        return '', 204
