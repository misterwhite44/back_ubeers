from flask_restx import Api
from .beers import beers_ns
from .breweries import breweries_ns
from .users import users_ns

api = Api()

api.add_namespace(beers_ns, path="/beers")
api.add_namespace(breweries_ns, path="/breweries")
api.add_namespace(users_ns, path="/users")
