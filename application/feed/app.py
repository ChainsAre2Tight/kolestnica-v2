from flask import Flask
from database.models import db

app = Flask('Feed')

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/koleso2"
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)