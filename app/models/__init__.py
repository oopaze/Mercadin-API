from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

ma = Marshmallow()
db = SQLAlchemy()

def configure(app):
    ma.init_app(app)

def configure(app):
    db.init_app(app)
    app.db = db
