"""Initializes notification server application"""


import os

from flask import Flask
from celery import Celery
from flask_socketio import SocketIO


# flask
app = Flask('Notification server')
app.config['SECRET_KEY'] = os.environ.get('FLASK-SECRET-KEY')


@app.route('/socket.io/ping')
def ping():
    return 'p0ng'

# socketio
socket = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins=["http://localhost:3000"])


# celery
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_queue_db = os.environ.get('REDIS_QUEUE_DB')

redis_url = f'redis://{redis_host}:{redis_port}/{redis_queue_db}'

def make_celery(app):
    celery = Celery('notification', backend=redis_url,
                    broker=redis_url)
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)


# miscellaneous
api_key = os.environ.get('API_KEY') or 'secret-api-key'

from notification_server.controllers import EventController
from notification_server.tasks import *