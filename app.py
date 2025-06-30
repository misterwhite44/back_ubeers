import sentry_sdk
from flask import Flask
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration

from models import db
from routes import api as routes_namespace
import pymysql
import os
from dotenv import load_dotenv
pymysql.install_as_MySQLdb()

load_dotenv()

sentry_sdk.init(
    dsn="https://50b825ff6e0cfee1b611665ae0c76147@o4509332960509952.ingest.de.sentry.io/4509587000655952",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0  # Attention : à réduire en prod si nécessaire
)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://uuw6sv5bvs11qa51:md1HTCoAHEg0s4HbJHGc@bwawmx4ntfjwzxxrotz4-mysql.services.clever-cloud.com:3306/bwawmx4ntfjwzxxrotz4?charset=utf8mb4"
)

CORS(app, origins=[os.getenv("FRONT_URL")])

db.init_app(app)
routes_namespace.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
