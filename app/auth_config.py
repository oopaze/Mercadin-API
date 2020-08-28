from .models.employees import Employees
from flask_jwt import JWT



def authenticate(registration, password):
    user = Employees.query.filter_by(registration=registration).scalar()
    if user.verify_password(password):
        return user

def identity(payload):
    return Employees.query.filter(Employees.id == payload['identity']).scalar()

jwt = JWT(authentication_handler = authenticate, identity_handler = identity)

def configure(app):
    jwt.init_app(app)
    app.config['JWT_AUTH_USERNAME_KEY'] = 'registration'
    return jwt
