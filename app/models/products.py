from app.models import db

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, default=0)
    weight = db.Column(db.Float, nullable=False)

    def __init__(self, name, price, amount, weight):
        self.name = name
        self.price = price
        self.amount = amount
        self.weight = weight

    def __repr__(self):
        return f'< Product {self.name} >'
