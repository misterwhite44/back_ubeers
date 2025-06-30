from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Beer(db.Model):
    __tablename__ = 'beers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    brewery_id = db.Column(db.Integer, db.ForeignKey('breweries.id'), nullable=False)
    image_url = db.Column(db.String(255))

class Brewery(db.Model):
    __tablename__ = 'breweries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    beers = db.relationship('Beer', backref='brewery', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

class Delivery(db.Model):
    __tablename__ = 'deliveries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    beer_id = db.Column(db.Integer, db.ForeignKey('beers.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    delivery_date = db.Column(db.DateTime)
