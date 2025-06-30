from flask import Flask
from flask_cors import CORS
from models import db
from routes import api as routes_namespace
import pymysql
import os
from dotenv import load_dotenv

pymysql.install_as_MySQLdb()

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app, origins=[os.getenv("FRONT_URL")])

db.init_app(app)
routes_namespace.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
