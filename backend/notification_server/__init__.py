"""Initializes notification server application"""


import os

from flask import Flask
from flask_socketio import SocketIO


# flask
app = Flask('Notification server')
app.config['SECRET_KEY'] = os.environ.get('FLASK-SECRET-KEY')


@app.route('/socket.io/ping')
def ping():
    return 'p0ng'

# socketio
socket = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins=["http://localhost:1337"])


from notification_server.controllers import EventController
from notification_server.routes import ChatRequests, MembersRequests, MessageRequests