import os

class Config(object):
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = 'MinhaNamoradaEUmaGostosinhaLinda'
	basedir = os.path.abspath(os.path.dirname(__file__))



class Development(Config):
	ENV = 'Development'
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'mercadin.db')


class Production(Config):
	ENV = 'Production'
	DEBUG = False
	os.environ['FLASK_APP'] = os.path.join(basedir, 'run.py')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'mercadin.db')
