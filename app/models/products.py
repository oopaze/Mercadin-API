from app.models import db
from .sectors import Sectors

sector_product = db.Table(
    'Sector-Product',
    db.Column('products_id', db.Integer, db.ForeignKey('products.id')),
    db.Column('sectors_id', db.Integer, db.ForeignKey('sectors.id'))
)

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, default=0)
    weight = db.Column(db.Float, nullable=False)
    sectors = db.relationship(Sectors, secondary=sector_product,
                              backref=db.backref('products', lazy='dynamic'))

    def __init__(self, name, price, amount, weight):
        self.name = name
        self.price = price
        self.amount = amount
        self.weight = weight

    def __repr__(self):
        return f'< Product {self.name} >'
