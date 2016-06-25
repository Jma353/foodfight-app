from . import app 

# Standard imports 
from datetime import datetime 
import re 
from helpers import * 

# MongoDB imports 
from flask_mongokit import MongoKit, Document


# User class (will not be placed here permanently)
class User(Document):
	# Collection name
	__collection__ = 'users'

	# Structure
	structure = {
		'name' : unicode, 
		'email' : unicode, 
		'image_url' : unicode, 
		'created_at': datetime,
		'updated_at': datetime
	}

	required_fields = ['name', 'email']
	default_values = { 'created_at': datetime.utcnow, 'updated_at': datetime.utcnow }
	use_dot_notation = True


# Init db + register documents
db = MongoKit(app)
db.register([User])