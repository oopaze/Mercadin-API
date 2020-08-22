from app.models import db
from .products import Products

class Carts(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Integer, default=0)
    products = db.relationship(Products, backref='carts')
