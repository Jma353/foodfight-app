import os
import base64
import json
import urllib2
from pprint import pprint 

file13 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/arizona_total_bus_info_data.json')
bus_info = json.load(file13, encoding="utf8")

# Grab rest JSON 
def restaurant_json(): 
	return bus_info


