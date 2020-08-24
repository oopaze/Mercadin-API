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

@prod.route('/many', methods=['POST'])
def insert_many_products():
    try:
        ps = ProductsSchema(many=True)
        data = request.json['data']

        products = []
        for i in range(1, len(data)+1):
            product = data[str(i)]

            product_class = Products(name=product['name'], price=product['price'],
                               weight=product['weight'], amount=product['amount'])
            sector = Sectors.query.filter_by(slug=product['sector']).first()
            sector.products.append(product_class)

            db.session.add(product_class)
            db.session.commit()
            products.append(product_class)

        json = {'data':ps.dump(products), 'message':'Products inserted sucessfully!'}
        return jsonify(json), 201

    except UnmappedInstanceError:#(TypeError, KeyError):
        json = {'message':'Invalid Data!'}
        return jsonify(json), 406


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
        data = request.json['data']

        product = Products(name=data['name'], price=data['price'],
                           weight=data['weight'], amount=data['amount'])
        sector = Sectors.query.filter_by(slug=data['sector']).first()
        sector.products.append(product)

        db.session.add(product)
        db.session.commit()

        json = {'data':ps.dump(product), 'message':'Product inserted sucessfully!'}
        return jsonify(json), 201

    except (TypeError, KeyError):
        json = {'message':'Invalid Data!'}
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

        data = request.json['data']
        product = Products.query.get(id)

        product.name = data['name']
        product.weight = data['weight']
        product.price = data['price']
        product.amount = data['amount']

        db.session.commit()

        json = {'data':ps.dump(product), 'message':'Product update sucessfully!'}

        return jsonify(json), 200

    except AttributeError:
        json = {'message':'Unable to find product!'}
        return jsonify(json), 404

    except (TypeError, KeyError):
        json = {'message':'Invalid Data!'}
        return jsonify(json), 406


@prod.route('/<int:id>/<string:slug>', methods=['PUT'])
def update_sector_of_product(id, slug):
    """
        Router that move a product of a sector to another sector
        receiving on route params the product.id and the new sector's slug
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

        json = {'data':ps.dump(newProduct), 'message':'Product sector changed sucessfully!'}
        return jsonify(json), 200

    except AttributeError:
        json = {'message':'Unable to find product!'}
        return jsonify(json), 404


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

        json = {'data':ps.dump(product), 'message':'Product deleted sucessfully!'}

        return jsonify(json), 200

    except UnmappedInstanceError:
        json = {'message':'Product element not found!'}
        return jsonify(json), 404
