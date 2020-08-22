from sqlalchemy.orm.exc import UnmappedInstanceError
from app.models.schemas import ProductsSchema
from flask import Blueprint, request, jsonify
from app.models.products import Products
from app.models.sectors import Sectors
from app.models import db

prod = Blueprint('products', __name__)

@prod.route('/<int:id>', methods=['GET'])
@prod.route('/', methods=['GET'])
def show_products(id = None):
    """
        Router that show all or one product
    """
    ps = ProductsSchema(many=True)

    products = Products.query.all()

    if id:
        products = Products.query.get(id)

    return ps.jsonify(products), 200


@prod.route('/', methods=['POST'])
def insert_product():
    """
        Router that allow us insert products in DB
        receiving a JSON like:
            {'name':'product-name', 'price':'product-price',
             'weight':'product-weight', 'amount':'product-amount',
             'sector':'sector-slug'}
    """
    try:
        ps = ProductsSchema()
        data = request.json

        product = Products(name=data['name'], price=data['price'],
                           weight=data['weight'], amount=data['amount'])
        sector = Sectors.query.filter_by(slug=data['sector']).first()
        sector.products.append(product)

        db.session.add(product)
        db.session.commit()

        json = {'Data':ps.dumps(product), 'Message':'Product insert sucessfully!'}

        return jsonify(json), 201

    except (TypeError, KeyError):
        json = {'Message':'Invalid Data!'}
        return jsonify(json), 406


@prod.route('/<int:id>', methods=['PUT'])
def update_product(id):
    """
        Router that update a product
        receiving a JSON like:
            {'name':'product-name', 'price':'product-price',
             'weight':'product-weight', 'amount':'product-amount'}
    """
    try:
        ps = ProductsSchema()

        data = request.json
        product = Products.query.get(id)

        product.name = data['name']
        product.weight = data['weight']
        product.price = data['price']
        product.amount = data['amount']

        db.session.commit()

        json = {'Data':ps.dumps(product), 'Message':'Product update sucessfully!'}

        return jsonify(json)

    except AttributeError:
        json = {'Message':'Unable to find product!'}
        return jsonify(json), 404

@prod.route('/<int:id>/<string:slug>', methods=['PUT'])
def update_sector_of_product(id, slug):
    """
        Router that move a product of a sector to another sector
        receivindo on route params the product.id and the new sector's slug
    """
    try:
        ps = ProductsSchema()

        product = Products.query.get(id)
        db.session.delete(product)

        newProduct = Products(product.name, product.price, product.amount, product.weight)

        sector = Sectors.query.filter_by(slug=slug).first()
        sector.products.append(newProduct)


        db.session.add(newProduct)
        db.session.commit()

        json = {'data':ps.dumps(newProduct), 'Message':'Product sector changed sucessfully!'}
        return jsonify(json), 200

    except AttributeError:
        json = {'Message':'Unable to find product!'}
        return jsonify(json), 404

    except (TypeError, KeyError):
        json = {'Message':'Invalid data!'}
        return jsonify(json), 406

@prod.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    """
        Router that delete a single product from DataBase by ID
    """
    try:
        ps = ProductsSchema()

        product = Products.query.get(id)
        db.session.delete(product)
        db.session.commit()

        json = {'Data':ps.dumps(product), 'Message':'Product deleted sucessfully!'}

        return jsonify(json), 200

    except UnmappedInstanceError:
        json = {'Message':'Product element not found!'}
        return jsonify(json), 404
