from app.models.schemas import SaleSchema, ProductsSchema, EmployeeSchema
from flask import Blueprint, jsonify, request
from app.models.employees import Employees
from app.models.sales import Sales
from app.models import db

sale = Blueprint('sales', __name__)

@sale.route('/<int:id>', methods=['GET'])
@sale.route('/', methods=['GET'])
def show_sales(id = None):
    """
        Route that allow us see one or many sales
        show one just receiving the sale id on url params
    """
    try:
        ss = SaleSchema(many=True)
        sales = Sales.query.all()
        sales = ss.dump(sales)

        if id:
            ss.many = False
            es = EmployeeSchema()
            ps = ProductsSchema(many=True)

            sales = Sales.query.get(id)
            salesman = Employees.query.get(sales.salesman)
            products = [sale_product.product for sale_product in sales.products]

            sales = ss.dump(sales)
            sales['products'] = ps.dump(products)
            sales['salesman'] = es.dump(salesman)


        return jsonify(sales), 200

    except (AttributeError, IndexError):
        json = {'message':'Unable to find sale!'}
        return jsonify(json), 404


@sale.route('/<int:sale_id>/<int:product_id>', methods=['DELETE'])
def delete_product_of_sale(sale_id, product_id):
    """
        Route that delete product of a sale refreshing her
        price automatically, just receiving sales ID
        in url params and a json like:
            {'data':
                {"product_id": ID of the product}
            }
    """
    try:
        ss = SaleSchema()
        sale = Sales.query.get(sale_id)

        product = list(filter(lambda product: product.product.id == product_id, sale.products))[0]
        sale.products.remove(product)
        sale.calculate_total_price()

        db.session.commit()

        es = EmployeeSchema()
        ps = ProductsSchema(many=True)

        salesman = Employees.query.get(sale.salesman)
        products = [sale_product.product for sale_product in sale.products]

        sale = ss.dump(sale)
        sale['products'] = ps.dump(products)
        sale['salesman'] = es.dump(salesman)

        json = {"data": sale, "message":"Product deleted and price ajusted sucessfully!"}

        return jsonify(sale), 200

    except (AttributeError, IndexError):
        json = {'message':'Unable to find sale or product!'}
        return jsonify(json), 404


@sale.route('/<int:id>', methods=['DELETE'])
def delete_sale(id):
    """
        Route that delete a product based on ID url param
    """
    try:
        ss = SaleSchema()

        sale = Sales.query.get(id)

        db.session.delete(sale)
        db.session.commit()

        json = {'data': ss.dump(sale), "message":"Sale deleted sucessfully!"}, 200
        return jsonify(json)

    except AttributeError:
        json = {'message':'Unable to find sale!'}
        return jsonify(json), 404
