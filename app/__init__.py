from flask import Flask
from app.models import configure as config_db
from app.models import configure as config_ma
from flask_migrate import Migrate, MigrateCommand

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Development')

    config_db(app)
    config_ma(app)

    Migrate(app, app.db)

    from app.routes.sectors import sec
    from app.routes.products import prod

    app.register_blueprint(sec, url_prefix='/sectors')
    app.register_blueprint(prod, url_prefix='/products')


    return app
