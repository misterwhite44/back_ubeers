from flask import Flask
from flask_cors import CORS
from models import db
from routes import api as routes_namespace
import pymysql
import os
from dotenv import load_dotenv
import redis

pymysql.install_as_MySQLdb()

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://uuw6sv5bvs11qa51:md1HTCoAHEg0s4HbJHGc@bwawmx4ntfjwzxxrotz4-mysql.services.clever-cloud.com:3306/bwawmx4ntfjwzxxrotz4?charset=utf8mb4"
)

CORS(app, origins=[os.getenv("FRONT_URL")])

# Connexion Redis
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB")),
    decode_responses=True  
)

db.init_app(app)
routes_namespace.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
