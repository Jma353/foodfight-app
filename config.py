import os 
basedir = os.path.abspath(os.path.dirname(__file__))

# File for different environments 

class Config(object): 
	DEBUG = False 
	TESTING = False
	CSRF_ENABLED = True 
	CSRF_SESSION_KEY = "secret"
	SECRET_KEY = os.environ['SECRET_KEY']
	THREADS_PER_PAGE = 2


class ProductionConfig(Config):
	DEBUG = False 
	MONGODB_HOST = os.environ["MONGODB_HOST"]
	MONGODB_PORT = int(os.environ['MONGODB_PORT']) 
	MONGODB_DATABASE = os.environ['MONGODB_DATABASE'] 
	MONGODB_USERNAME = os.environ['MONGODB_USERNAME']
	MONGODB_PASSWORD = os.environ['MONGODB_PASSWORD'] 


class StagingConfig(Config):
	DEVELOPMENT = True 
	DEBUG = True 


class DevelopmentConfig(Config):
	DEVELOPMENT = True 
	DEBUG = True 
	MONGODB_HOST = 'localhost'
	MONGODB_PORT = 27017
	MONGODB_DATABASE = 'foodfight-app'


class TestingConfig(Config):
	TESTING = True 