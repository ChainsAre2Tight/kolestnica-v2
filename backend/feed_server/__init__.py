"""Initialises feed service Flask application"""


import os

from flask import Flask
from celery import Celery

from libraries.database import db


# flask
app = Flask('Feed')
app.config['SECRET_KEY'] = os.environ.get('FLASK-SECRET-KEY')


# database
db_url = os.environ.get('DB_URL')
db_uasername = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_port = os.environ.get('DB_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_url}://{db_uasername}:{db_password}@db:{db_port}/{db_name}'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# celery
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_queue_db = os.environ.get('REDIS_QUEUE_DB')

redis_url = f'redis://{redis_host}:{redis_port}/{redis_queue_db}'
celery = Celery(
    'tasks',
    broker=redis_url,
    backend=redis_url
)

celery.conf.ignore_result = True
celery.conf.worker_concurrency = 0

from feed_server.controllers import chats_controller, messages_controller, members_controller
