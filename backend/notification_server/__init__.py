"""Initializes notification server application"""


import os

from flask import Flask
from celery import Celery
from flask_socketio import SocketIO


# flask
app = Flask('Notification server')
app.config['SECRET_KEY'] = os.environ.get('FLASK-SECRET-KEY')


# socketio
socket = SocketIO(app)


# celery
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_queue_db = os.environ.get('REDIS_QUEUE_DB')

redis_url = f'redis://{redis_host}:{redis_port}/{redis_queue_db}'
celery = Celery(
    'Feed celery',
    broker=redis_url
)


# miscellaneous
api_key = os.environ.get('API_KEY') or 'secret-api-key'
