from app.models.schemas import CartSchema, ProductsSchema
from flask import Blueprint, request, jsonify
from sqlalchemy.orm.exc import FlushError
from app.models.products import Products
from app.models.carts import Carts, Cart_Product
from app.models import db

cart = Blueprint('carts', __name__)


@cart.route('/<int:id>', methods=['GET'])
@cart.route('/', methods=['GET'])
def show_carts(id = None):
    """
        Route that provides all carts in DB
    """
    try:
        cs = CartSchema(many=True)

        carts = Carts.query.all()

        if id:
            cs.many=False
            ps = ProductsSchema(many=True)
            carts = Carts.query.get(id)
            json = cs.dump(carts)
            json['products'] = ps.dump([product.product for product in carts.products])

            return jsonify(json), 200

        return cs.jsonify(carts), 200

    except AttributeError:
        json = {'message':'Unable to find cart!'}
        return jsonify(json), 404

@cart.route('/', methods=['POST'])
def insert_cart():
    """
        Route insert cart without need
        any data
    """
    cs = CartSchema()
    cart = Carts()

    db.session.add(cart)
    db.session.commit()

    json = {'data': cs.dump(cart), 'message':'Cart created sucessfully!'}

    return jsonify(json), 201


@cart.route('/<int:id>', methods=['POST'])
def add_product_to_cart(id):
    """
        Route that allows us insert product
        into the cart just receiving a JSON like:
            {"data": {
                'product_id': <id of the product>,
                'product_amount': <amount of products>}
            }
    """
    try:
        data = request.json['data']
        cs = CartSchema()

        cart = Carts.query.get(id)

        product = Products.query.get(data['product_id'])

        for i in range(data['product_amount']):
            card_product = Cart_Product(product)
            cart.products.append(card_product)

        db.session.commit()

        cart.calculate_total_price()
        db.session.commit()

        return cs.jsonify(cart), 201

    except (AttributeError, FlushError):
        json = {'message':'Unable to find cart or product!'}
        return jsonify(json), 404

@cart.route('/<int:cart_id>/<int:product_id>', methods=['DELETE'])
def delete_product_of_cart(cart_id, product_id):
    """
        Route that allow us to delete a product of a cart
        receiving on url params the card id and the product id
        in a front 'url/<card id>/<product id>'
    """
    try:
        print(cart_id, product_id)
        cs = CartSchema()

        cart = Carts.query.get(cart_id)

        product = list(filter(lambda product: product.product.id == product_id, cart.products))[0]
        cart.products.remove(product)
        db.session.commit()

        return cs.jsonify(cart), 200

    except (AttributeError, IndexError):
        json = {'message':'Unable to find cart or product!'}
        return jsonify(json), 404

@cart.route('/<int:id>', methods=['DELETE'])
def delete_cart(id):
    """
        Route that allows us delete a cart
    """
    try:
        cs = CartSchema()

        cart = Carts.query.get(id)

        db.session.delete(cart)
        db.session.commit()

        return cs.jsonify(cart), 200

    except AttributeError:
        json = {'message':'Unable to find cart!'}
        return jsonify(json), 404
