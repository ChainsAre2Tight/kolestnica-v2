"""Initializes notification server application"""


import os

from flask import Flask
from celery import Celery
from flask_socketio import SocketIO


app = Flask('Notification server')
celery = Celery(
    'Notification celery',
    broker=os.environ.get('CELERY_BROKER_URL')
)
socket = SocketIO(app)
api_key = os.environ.get('API_KEY') or 'secret-api-key'
