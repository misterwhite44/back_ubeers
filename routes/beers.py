from flask_restx import Namespace, Resource, fields
from models import db, Beer
from extensions import redis_client
import redis

beers_ns = Namespace("beers", description="Beers operations")

beer_model = beers_ns.model("Beer", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True),
    "type": fields.String,
    "degree": fields.Float,
    "brewery_id": fields.Integer,
    "image_url": fields.String  
})

@beers_ns.route("/test")
class BeerTest(Resource):
    def get(self):
        # Exemple : incrémente un compteur de tests
        redis_client.incr("beers_test_count")
        # Ou ajoute un log avec timestamp
        import time
        redis_client.lpush("beers_test_logs", f"Test at {time.time()}")
        return {"message": "Test enregistré dans Redis"}, 200
    
@beers_ns.route("/test/logs")
class BeerTestLogs(Resource):
    def get(self):
        count = redis_client.get("beers_test_count") or "0"
        logs = redis_client.lrange("beers_test_logs", 0, 9)  # derniers 10 logs
        return {
            "test_count": int(count),
            "recent_logs": logs
        }, 200


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
