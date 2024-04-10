from flask import Flask
from database.models import db

app = Flask('User server')

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/koleso2_test"
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)