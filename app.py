from flask import Flask
from flask_cors import CORS
from models import db
from routes import api as routes_namespace
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://uuw6sv5bvs11qa51:md1HTCoAHEg0s4HbJHGc@bwawmx4ntfjwzxxrotz4-mysql.services.clever-cloud.com:3306/bwawmx4ntfjwzxxrotz4?charset=utf8mb4"
)

CORS(app, origins=["https://ubeer-jade.vercel.app"])

db.init_app(app)
routes_namespace.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
