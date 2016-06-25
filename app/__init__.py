# GEvent needed for sockets (must patch server before anything else)
from gevent import monkey 
monkey.patch_all() 
from helpers import * 

# All flask imports 
from flask import Flask

# SocketIO for Flask 
from flask_socketio import SocketIO 

# App init 
app = Flask(__name__)
app.debug = True 
app.config.from_object(os.environ["APP_SETTINGS"])

# Init socketio 
socketio = SocketIO()
socketio.init_app(app)

# Import our routes
from app.routes import * 






