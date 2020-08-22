from flask import Blueprint
from app.models.carts import Carts

cart = Blueprint('carts', __name__)

@cart.route('/', methods=['GET'])
def show_carts():
    ...

@cart.route('/', methods=['POST'])
def insert_cart():
    ...

@cart.route('/<int:id>', methods=['PUT'])
def update_cart(id):
    ...

@cart.route('/<int:id>', methods=['DELETE'])
def delete_cart(id):
    ...
