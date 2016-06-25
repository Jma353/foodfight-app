import os 
from flask import request 
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io, requests
import json
from pprint import pprint

# Function to determine if a request is an API request for JSON or a standard resource request
# Credit: http://flask.pocoo.org/snippets/45/
def request_for_json():
	best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
	return best == 'application/json' and \
		request.accept_mimetypes[best] > \
		request.accept_mimetypes['text/html']


# Function to read in JSON 
def read_json(path): 
	with open(path) as json_data: 
		d = json.load(json_data)
		json_data.close() 
		return d 


# Yelp auth + client init 
auth = Oauth1Authenticator(
	consumer_key=os.environ['YELP_CONSUMER_KEY'],
	consumer_secret=os.environ['YELP_CONSUMER_SECRET'],
	token=os.environ['YELP_TOKEN'],
	token_secret=os.environ['YELP_TOKEN_SECRET']
)

# Yelp client for querying 
client = Client(auth)

def yelpApiCoordinates(lat, long, params):
	return client.search_by_coordinates(lat, long, **params)

def yelpApiBoundingBox(lat, long, params):
	return client.search_by_bounding_box(lat1,long1,lat2,long2,**params)

def yelpApiSearch(location, params):
	return client.search(location, **params)

def yelpBusinsess(id):
	return client.get_business(id);

def getYelpInfo(lat, long, term):
	params = {
		"limit": 20,
		"term": term
	}
	response = yelpApiCoordinates(lat, long, params)


	responses = []
	for i in range(0, len(response.businesses)):
		review = yelpBusinsess(response.businesses[i].id)

	responses.append({
		"id": response.businesses[i].id,
		"name": response.businesses[i].name,
		"rating": response.businesses[i].rating,
		"cats": response.businesses[i].categories,
		"lat": response.businesses[i].location.coordinate.latitude,
		"long": response.businesses[i].location.coordinate.longitude,
		"review": review.business.reviews[0].excerpt
	});
	return responses






