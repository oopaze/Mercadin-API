from app.models import db
from .products import Products
from .employees import Employees


Cart_Product = db.Table(
    'cart_product',
    db.Column('cart_id', db.Integer, db.ForeignKey('carts.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'))
)

class Carts(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Integer, default=0)
    products = db.relationship(Products, secondary=Cart_Product,
                               backref=db.backref('carts', lazy='dynamic'))

    owner = db.relationship(Employees, backref='carts')

    def calculate_total_price(self):
        if products:
            prices = [product.price for product in self.products]
            for price in prices:
                self.total_price += price
            return {'Message':'Total price updated sucessfuly!'}
        return {'Message':'Total price is already up-to-date!'}
