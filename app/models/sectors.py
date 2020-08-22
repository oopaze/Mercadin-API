from app.models import db
from .products import Products

sector_product = db.Table(
    'sector_product',
    db.Column('products_id', db.Integer, db.ForeignKey('products.id')),
    db.Column('sectors_id', db.Integer, db.ForeignKey('sectors.id'))
)

class Sectors(db.Model):
    __tablename__ = 'sectors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    slug = db.Column(db.String(30), unique=True)
    products = db.relationship(Products, secondary=sector_product,
                              backref=db.backref('sectors', lazy='dynamic'))

    def __init__(self, name):
        self.name = name
        self.slug = name.replace(' ', '_').lower()

    def __repr__(self):
        return f'< Sector {self.name} >'
