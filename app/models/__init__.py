from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

bp = Bcrypt()
ma = Marshmallow()
db = SQLAlchemy()

def configure_bp(app):
    bp.init_app(app)

def configure_ma(app):
    ma.init_app(app)

def configure_db(app):
    db.init_app(app)
    app.db = db
