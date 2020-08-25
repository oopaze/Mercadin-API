import os

class Config(object):
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = 'MinhaNamoradaEUmaGostosinhaLinda'


class Development(Config):
	ENV = 'Development'
	DEBUG = True
	basedir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'mercadin.db')


class Production(Config):
	ENV = 'Production'
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
