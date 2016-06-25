# GEvent needed for sockets (must patch server before anything else)
from gevent import monkey 
monkey.patch_all() 

# Standard imports 
from datetime import datetime 
import re 
import os 

# All flask imports 
from flask import Flask, request, render_template, redirect, url_for, jsonify 

# SocketIO for Flask 
from flask_socketio import SocketIO 

# MongoDB imports 
from flask_mongokit import MongoKit, Document

# App init 
app = Flask(__name__)
app.debug = True 
app.config.from_object(os.environ["APP_SETTINGS"])

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


# Test route to receive users 
@app.route('/', methods=['GET'])
def show_users():	
	# Retrieve users 
	users = db.User.find() 

	# Build string to observe users 
	user_string = "Users: \n"
	for u in users: 
		user_string += str(u) + "\n"
	return user_string


# Test route to create users 
@app.route('/users/create', methods=['POST'])
def create_user(): 
	user_JSON = request.get_json()['user']
	user = db.User()
	for key in user_JSON.keys(): 
		user[key] = user_JSON[key]
	user.save()
	return user.to_json() 



@app.route('/users/destroy', methods=['POST'])
def destroy_users(): 
	# Remove users 
	db.User.remove()
	return jsonify({ 'success' : true })


# Init socketio 
socketio = SocketIO()
socketio.init_app(app)









