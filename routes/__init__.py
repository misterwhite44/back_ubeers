from flask_restx import Namespace

from .beers import api as beers_ns
from .breweries import api as breweries_ns
from .users import api as users_ns

api = Namespace("ubeers", description="uBeers related operations")
api.add_namespace(beers_ns, path="/beers")
api.add_namespace(breweries_ns, path="/breweries")
api.add_namespace(users_ns, path="/users")
