from app.models.schemas import EmployeeSchema, CartSchema, SaleSchema
from app.models.employees import Employees
from app.models.carts import Carts
from app.models.sales import Sales, Sales_product
from flask import Blueprint, request, jsonify
from app.models import db

emp = Blueprint('employees', __name__)

@emp.route('/<int:id>', methods=['GET'])
@emp.route('/', methods=['GET'])
def show_users(id = None):
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
            {'name': user complete name, 'password': an password, 'admin': true/false}
    """
    es = EmployeeSchema()
    data = request.json['data']

    employee = Employees(data['name'], data['password'], data['admin'])

    db.session.add(employee)
    db.session.commit()

    employee.registration = employee.id + 1000

    db.session.commit()

    json = {'data':es.dump(employee), 'message':'User created sucessfully!'}

    return jsonify(json), 201

@emp.route('/<int:employee_id>/new-cart', methods=['POST'])
def insert_cart_to_employee(employee_id):
    es = EmployeeSchema()
    cs = CartSchema()
    data = request.json['data']

    employee = Employees.query.get(employee_id)
    cart = Carts.query.get(data['cart_id'])

    employee.carts.append(cart)

    db.session.commit()

    carts = employee.carts

    employee = es.dump(employee)
    employee['carts'] = cs.dump(carts)

    json = {'data':employee, 'message':'Product added sucessfully!'}

    return jsonify(json), 201

@emp.route('/<int:employee_id>/new-sale', methods=['POST'])
def make_sale(employee_id):
    es = EmployeeSchema()
    ss = SaleSchema()
    data = request.json['data']

    employee = Employees.query.get(employee_id)
    cart = employee.carts[0]

    if "cart_id" in data:
        cart = Carts.query.get(data['cart_id'])

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

@emp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    es = EmployeeSchema()
    data = request.json['data']

    employee = Employees.query.get(id)
    employee.name = data['name']
    employee.password = employee.generate_hash_password(data['password'])
    employee.admin = data['admin']

    db.session.commit()

    json = {'data':es.dump(employee), 'message':'User updated sucessfully!'}

    return jsonify(json), 200

@emp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    es = EmployeeSchema()
    employee = Employees.query.get(id)

    db.session.delete(employee)
    db.session.commit()

    json = {'data': es.dump(employee), 'message':'User deleted sucessfully!'}

    return jsonify(json), 200

@emp.route('/<int:user_id>/<int:cart_id>', methods=['DELETE'])
def delete_cart_of_user(user_id, cart_id):
    es = EmployeeSchema()
    cs = CartSchema()

    employee = Employees.query.get(id)
    cart = list(filter(lambda cart: cart.id == cart_id, employee.carts))[0]
    employee.cart.remove(cart)
    db.session.commit()

    carts = employee.carts

    employee = es.dump(employee)
    employee['carts'] = cs.dump(carts)


    json = {'data': employee, 'message':'Cart deleted sucessfully!'}

    return jsonify(json), 200
