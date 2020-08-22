from app.models.schemas import CartSchema
from app.models.products import Products
from flask import Blueprint, request
from app.models.carts import Carts

cart = Blueprint('carts', __name__)

@cart.route('/<int:id>', methods=['GET'])
@cart.route('/', methods=['GET'])
def show_carts(id = None):
    cs = CartSchema(many=True)

    carts = Carts.query.all()

    if id:
        cs.many=False
        carts. Carts.query.get(id)

    return cs.jsonify(carts), 200

@cart.route('/', methods=['POST'])
def insert_cart():
    cs = CartSchema()
    cart = Cart()

    db.session.add(cart)
    db.session.commit()

    return cs.jsonify(cart), 201

@cart.route('/<int:id>', methods=['PUT'])
def add_product_to_cart(id):
    cs = CartSchema()

    cart = Cart.query.get(id)
    product = Products.query.get(request.json['product_id'])

    cart.products.append(product)

    db.session.commit()

    return cs.jsonify(cart), 201

@cart.route('/<int:cart_id>/<int:product_id>', methods=['DELETE'])
def delete_product_of_cart(cart_id, product_id):
    cs = CartSchema()

    cart = Cart.query.get(cart_id)

    product = list(filter(lambda product: product.id == product_id, products))[0]
    products.remove(product)
    db.session.commit()

    return cs.jsonify(cart), 200

@cart.route('/<int:id>', methods=['DELETE'])
def delete_cart(id):
    cs = CartSchema()

    cart = Cart.query.get(id)

    db.session.delete(cart)
    db.session.commit()

    return cs.jsonify(cart), 200
