from flask import Flask
from database.models import db
import os

app = Flask('User server')

# import relevant config
Environment = os.environ.get('ENVIRONMENT') or 'TEST'
if Environment == 'TEST':
    from project_config import TestGlobalConfig as GlobalConfig
elif Environment == 'PRODUCTION':
    from project_config import ProductionGlobalConfig as GlobalConfig

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:root@localhost:3306/{GlobalConfig.database_name}"
app.config['SECRET_KEY'] = os.environ.get('FLASK-SECRET-KEY') or 'secret'

app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)