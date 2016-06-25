#!/bin/bash

http POST localhost:5000/users/destroy 
http POST localhost:5000/users/create < joe.json
http POST localhost:5000/users/create < ilan.json 