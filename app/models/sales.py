from app.models import db
from datetime import datetime
from .products import Products
from .employees import Employees

class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.Integer)
    total_price = db.Column(db.Integer, nullable=True)
    salesman = db.relationship(Employees, backref='sales')
    products = db.relationship(Products, backref='sales')
    sold_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, customer, total_price):
        self.customer = customer
        self.total_price = total_price

    def __repr__(self):
        return f'<Purchase of {costumer} on {sold_at}>'
