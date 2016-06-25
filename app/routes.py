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

	# Grab the user fields 
	user_JSON = request.get_json()['user']

	# Create the user 
	user = db.User()
	for key in user_JSON.keys(): 
		user[key] = user_JSON[key]
	user.save()

	# Call static data from S3 
	az_json = restaurant_json() 

	# Grab training data 
	training_data = gen_training_data(az_json)

	# Build result 
	user = user.to_json()
	result = {}
	result['user'] = json.loads(user)
	result['training_data'] = training_data

	# Respond 
	return jsonify(result)



@app.route('/users/add_pref', methods=['POST'])
def add_pref():

	# Grab the pref fields 
	user_JSON = request.get_json()['user']
	pref_JSON = request.get_json()['pref']

	# Grab the user 
	user = db.User.find_one(user_JSON)

	# Modify preferences 
	if pref_JSON['prefer']:
		user['likes'].append(pref_JSON['business_id'])
	else: 
		user['dislikes'].append(pref_JSON['business_id'])

	user.save() 

	return jsonify({ 'success': True, 'user' : json.loads(user.to_json()) })


@app.route('/choices/recommend', methods=['POST'])
def return_prefs(): 

	# choice_JSON 
	choices = request.get_json()['choices']

	# Array of users' names 
	users = request.get_json()['users']

	likes = []
	dislikes = [] 
	for u in users: 
		user = db.User.find_one(u)
		likes += user['likes']
		dislikes += user['dislikes']

	result_ids = [elem[0] for elem in find_similar(choices, likes, dislikes, 32, -112)]

	restaurants = []
	for rest_id in result_ids: 
		rest = restaurant_json()[rest_id]
		restaurants.append(rest)

	return jsonify({ 'success': True, 'suggestions': json.dumps(restaurants) })


# Destory users endpoint 
@app.route('/users/destroy', methods=['POST'])
def destroy_users(): 
	# Remove users 
	users = db.User.find() 
	for user in users: 
		user.delete() 

	return jsonify({ 'success' : True })



# Socket connect
@socketio.on('connect', namespace='/main')
def ws_conn():
	socketio.emit('msg', "You are connected", namespace='/main')

# Socket disconnect
@socketio.on('disconnect', namespace='/main')
def ws_disconn(): 
	socketio.emit('msg', "Someone disconnected", namespace='/main')

# Query for terms 
@socketio.on('query', namespace='/main')
def chat(query):
	# query is a string 
	socketio.emit('query-results', [elem[0] for elem in run(query)], namespace="/main")







