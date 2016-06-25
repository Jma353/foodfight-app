from . import app, socketio 
from helpers import * 
import json 
from bson import json_util 
from models import db 

from flask import request, render_template, redirect, url_for, jsonify 


# Test route to receive users 
@app.route('/', methods=['GET'])
def show_users():	
	if request_for_json():
		# Query users + respond with JSON 
		users = list(db.User.find())
		return json.dumps(users, default=json_util.default)
	else: 
		return render_template("index.html")


# Test route to create users 
@app.route('/users/create', methods=['POST'])
def create_user(): 
	user_JSON = request.get_json()['user']
	user = db.User()
	for key in user_JSON.keys(): 
		user[key] = user_JSON[key]
	user.save()
	return user.to_json() 


# Destory users endpoint 
@app.route('/users/destroy', methods=['POST'])
def destroy_users(): 
	# Remove users 
	db.User.remove()
	return jsonify({ 'success' : true })


# JSONs for socket searching 
az_json = read_json('./arizona_bus_info.json')
az_id_json = read_json('./arizona_id_to_name.json')


# Socket testing 
@socketio.on('connect', namespace='/main')
def ws_conn():
	socketio.emit('msg', "You are connected", namespace='/main')

@socketio.on('disconnect', namespace='/main')
def ws_disconn(): 
	socketio.emit('msg', "Someone disconnected", namespace='/main')

@socketio.on('query', namespace='/main')
def chat(query):
	# query is a string 


	socketio.emit('query-results', , namespace="/main")








