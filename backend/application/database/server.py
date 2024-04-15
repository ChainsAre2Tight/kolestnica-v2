from flask import Flask
from database.models import db
import os

app = Flask('database manager')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db.init_app(app)
