from app.models import db
from .products import Products


class Cart_Product(db.Model):
    __tablename__ = 'cart_product'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship("Products")

    def __init__(self, product):
        self.product = product


class Carts(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, default=0)
    products = db.relationship("Cart_Product")
    owner = db.Column(db.Integer, db.ForeignKey('employees.id'))


    def calculate_total_price(self):
        if self.products:
            products = [cart_product.product for cart_product in self.products]
            for product in products:
                self.total_price += product.price
            self.total_price = round(self.total_price, 2)
            return {'Message':'Total price updated sucessfuly!'}
        return {'Message':'Total price is already up-to-date!'}
