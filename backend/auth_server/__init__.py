"""Provides flask application of auth server"""


import os

from flask import Flask

from libraries.database.models import db


# flask settings
app = Flask('User server')
app.config['SECRET_KEY'] = os.environ.get('FLASK-SECRET-KEY') or 'secret'


# database settings
db_url = os.environ.get('DB_URL')
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_port = os.environ.get('DB_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'{db_url}://{db_username}:{db_password}@db:{db_port}/{db_name}'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/koleso2_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# encryption public key
public_key = os.environ.get('JSON_PUBLIC_KEY')
api_key = os.environ.get('API_KEY')



from auth_server.controllers import sessions_controller, tokens_controller, users_controller, keys_controller
