from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from models import db
from config import Config
from routes import api as routes_namespace

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)

    api = Api(app, version="1.0", title="uBeers API", description="API REST uBeers")
    api.add_namespace(routes_namespace, path="/api")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
