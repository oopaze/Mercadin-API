from app.models.schemas import EmployeeSchema, CartSchema, SaleSchema
from flask_jwt import jwt_required, current_identity
from app.models.employees import Employees
from app.models.carts import Carts
from app.models.sales import Sales, Sales_product
from flask import Blueprint, request, jsonify
from app.models import db

emp = Blueprint('employees', __name__)

@emp.route('/<int:id>', methods=['GET'])
@emp.route('/', methods=['GET'])
def show_users(id = None):
    """
        Route that show all or one user selected by ID
    """
    es = EmployeeSchema(many=True)
    cs = CartSchema(many=True)
    ss = SaleSchema(many=True)

    employees = Employees.query.all()

    if id:
        employees = Employees.query.get(id)
        sales = employees.sales
        carts = employees.carts

        es.many = False
        employees = es.dump(employees)

        employees['sales'] = ss.dump(sales)
        employees['carts'] = cs.dump(carts)


    employees = es.dump(employees)

    return jsonify(employees), 200

@emp.route('/', methods=['POST'])
def insert_user():
    """
        JSON like:
            {"data": {
                'name': user complete name, 'password': an password, 'admin': true/false}
            }
    """
    try:
        es = EmployeeSchema()
        data = request.json['data']

        employee = Employees(data['name'], data['password'], data['admin'])

        db.session.add(employee)
        db.session.commit()

        employee.registration = employee.id + 1000

        db.session.commit()

        json = {'data':es.dump(employee), 'message':'User created sucessfully!'}

        return jsonify(json), 201

    except (TypeError, KeyError):
        json = {'message':'Invalid Data!'}
        return jsonify(json), 406

@emp.route('/<int:employee_id>/<int:cart_id>/new-cart', methods=['POST'])
def insert_cart_to_employee(employee_id, cart_id):
    """
        Route that allows a employee have a cart of products
        receiving a JSON like:
            {"data": {
                    "cart_id": id of the cart
                }
            }
    """
    try:
        es = EmployeeSchema()
        cs = CartSchema()

        employee = Employees.query.get(employee_id)
        cart = Carts.query.get(cart_id)

        employee.carts.append(cart)

        db.session.commit()

        carts = employee.carts

        employee = es.dump(employee)
        employee['carts'] = cs.dump(carts)

        json = {'data':employee, 'message':'Product added sucessfully!'}

        return jsonify(json), 201

    except (TypeError, KeyError):
        json = {'message':'Invalid Data!'}
        return jsonify(json), 406

    except AttributeError:
        json = {'message':'Unable to employee!'}
        return jsonify(json), 404

@emp.route('/<int:employee_id>/<int:cart_id>/new-sale', methods=['POST'])
def make_sale(employee_id, cart_id = None):
    """
        Route that allows us transform a cart in a real sale
        you can pass nothing and then the sale will be made with the first
        employee cart, or you can pass a cart_id of the carts that this employee
        is owner.
    """
    try:
        es = EmployeeSchema()
        ss = SaleSchema()

        employee = Employees.query.get(employee_id)
        cart = employee.carts[0]

        if cart_id:
                cart = Carts.query.get(cart_id)

        employee.carts.remove(cart)

        cart.calculate_total_price()

        sale = Sales(cart.total_price)
        sale.products = [Sales_product(product.product) for product in cart.products]
        cart.products = []
        cart.total_price = 0


        db.session.add(sale)
        db.session.commit()

        employee.sales.append(sale)

        db.session.commit()

        sales = employee.sales
        employee = es.dump(employee)
        employee['sale'] = ss.dump(sales[-1])
        json = {'data':employee, 'message':'Product sold sucessfully!'}

        return jsonify(json), 201

    except (TypeError, KeyError):
        json = {'message':'Invalid Data!'}
        return jsonify(json), 406

    except AttributeError:
        json = {'message':'Unable to employee!'}
        return jsonify(json), 404

@emp.route('/<int:id>/', methods=['PUT'])
@jwt_required()
def update_employee(id):
    """
        Route that allows update employee
        receiving a JSON like:
         {'data': {
                "name": new name of user,
                "password": new password of user,
                "admin": new admin bool
            }
         }
    """
    try:
        es = EmployeeSchema()
        data = request.json['data']

        employee = Employees.query.get(id)
        employee.name = data['name']
        employee.password = employee.generate_hash_password(data['password'])
        employee.admin = data['admin']

        db.session.commit()

        json = {'data':es.dump(employee), 'message':'User updated sucessfully!'}

        return jsonify(json), 200

    except (TypeError, KeyError):
        json = {'message':'Invalid Data!'}
        return jsonify(json), 406

    except AttributeError:
        json = {'message':'Unable to employee!'}
        return jsonify(json), 404

@emp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    """
        Route that allow us to delete a employee
        receiving the ID on url params
    """
    try:
        es = EmployeeSchema()
        employee = Employees.query.get(id)

        db.session.delete(employee)
        db.session.commit()

        json = {'data': es.dump(employee), 'message':'User deleted sucessfully!'}

        return jsonify(json), 200

    except AttributeError:
        json = {'message':'Unable to employee!'}
        return jsonify(json), 404


@emp.route('/<int:employee_id>/<int:cart_id>', methods=['DELETE'])
@jwt_required()
def delete_cart_of_employee(employee_id, cart_id):
    """
        Route that allows delete a cart of a employee
        just receiving the employee and cart ID
    """
    try:
        es = EmployeeSchema()
        cs = CartSchema()

        employee = Employees.query.get(employee_id)
        cart = list(filter(lambda cart: cart.id == cart_id, employee.carts))[0]
        employee.cart.remove(cart)
        db.session.commit()

        carts = employee.carts

        employee = es.dump(employee)
        employee['carts'] = cs.dump(carts)

        json = {'data': employee, 'message':'Cart deleted sucessfully!'}

        return jsonify(json), 200

    except (AttributeError, IndexError):
        json = {'message':'Unable to find employee or cart!'}
        return jsonify(json), 404
