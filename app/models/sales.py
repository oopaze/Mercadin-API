from app.models import db
from datetime import datetime
from .products import Products

Sales_product = db.Table(
    'sales_product',
    db.Column('sales_id', db.Integer, db.ForeignKey('sales.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
)

class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.Integer)
    total_price = db.Column(db.Integer, nullable=True)
    products = db.relationship(Products, secondary=Sales_product,
                               backref=db.backref('sales', lazy='dynamic'))

    salesman = db.Column(db.Integer, db.ForeignKey('employees.id'))
    sold_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, customer, total_price):
        if costumer:
            self.customer = customer
        self.total_price = total_price

    def __repr__(self):
        return f'<Purchase of {costumer} on {sold_at}>'
