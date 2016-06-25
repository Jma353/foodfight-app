import os
import base64
import json
import urllib2

file13 = urllib2.urlopen('https://s3.amazonaws.com/stantemptesting/arizona_total_bus_info_data.json')
bus_info = json.load(file13, encoding="utf8")

def search(bus_id):
	bus_info[bus_id]