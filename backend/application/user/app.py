from flask import Flask
from database.models import db
import os

app = Flask('User server')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('FLASK-SECRET-KEY') or 'secret'

app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)