from flask import Flask
from app.models import configure_db as config_db
from app.models import configure_ma as config_ma
from app.models import configure_bp as config_bp
from flask_migrate import Migrate, MigrateCommand

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Production')

    config_db(app)
    config_ma(app)
    config_bp(app)

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
