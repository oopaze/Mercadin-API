from app.models import db
from .carts import Carts

class Employees(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    position = db.Column(db.String)
    cart = db.relationship(Carts, backref='employees')

    def __init__(self, name, position):
        self.name = name
        self.position = position

    def __repr__(self):
        return f'<Employee {self.name}>'
