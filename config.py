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