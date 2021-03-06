from flask import Flask
from app.models import configure_db as config_db
from app.models import configure_ma as config_ma
from flask_migrate import Migrate, MigrateCommand
from .auth_config import configure as configure_auth

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Development')

    config_db(app)
    config_ma(app)
    configure_auth(app)

    Migrate(app, app.db)

    from app.routes.sectors import sec
    from app.routes.products import prod
    from app.routes.employees import emp
    from app.routes.carts import cart
    from app.routes.sales import sale

    app.register_blueprint(sec, url_prefix='/sectors')
    app.register_blueprint(prod, url_prefix='/products')
    app.register_blueprint(emp, url_prefix='/employees')
    app.register_blueprint(cart, url_prefix='/carts')
    app.register_blueprint(sale, url_prefix='/sales')


    return app
