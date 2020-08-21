from flask import Flask
from app.models import configure as config_db
from app.models import configure as config_ma
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Development')

    config_db(app)
    config_ma(app)

    Migrate(app, app.db)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    from app.routes.sectors import sec

    app.register_blueprint(sec, url_prefix='/sectors')

    return manager
