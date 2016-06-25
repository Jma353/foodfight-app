from flask import request 

# Function to determine if a request is an API request for JSON or a standard resource request
# Credit: http://flask.pocoo.org/snippets/45/
def request_for_json():
	best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
	return best == 'application/json' and \
		request.accept_mimetypes[best] > \
		request.accept_mimetypes['text/html']
