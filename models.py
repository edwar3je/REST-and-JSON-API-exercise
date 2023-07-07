"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    __tablename__ = 'baked_goods'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)

    # I couldn't figure out how to set the default on the model, so I set the default on the constructor function
    def __init__(self, flavor, size, rating, image='https://tinyurl.com/demo-cupcake'):
        self.flavor = flavor
        self.size = size
        self.rating = rating
        self.image = image

def serialize(dct):
    return {'id': dct.id, 'flavor': dct.flavor, 'size': dct.size, 'rating': dct.rating, 'image': dct.image}