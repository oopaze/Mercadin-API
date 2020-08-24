from app.models import db, bp
from .sales import Sales
from .carts import Carts

class Employees(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registration = db.Column(db.Integer, unique=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)

    sales = db.relationship(Sales, backref='employees')
    carts = db.relationship(Carts, backref='employees')

    def __init__(self, name, password, admin: bool = None):
        self.name = name
        self.password = self.generate_hash_password(password)

        if admin:
            self.admin = admin

    def __repr__(self):
        return f'<Employee {self.name}>'

    def generate_hash_password(self, password):
        return bp.generate_password_hash(password)

    def verify_password(self, password):
        return bp.check_password_hash(self.password, password)
