"""Provides seeder server"""


from flask import Flask
from libraries.database import db
import os

app = Flask('database manager')

db_url = os.environ.get('DB_URL')
db_uasername = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_port = os.environ.get('DB_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_url}://{db_uasername}:{db_password}@db:{db_port}/{db_name}'

db.init_app(app)
