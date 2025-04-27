from flask import Flask
from src.models import db

app = Flask(__name__)

DEBUG = True
TESTING = True
SECRET_KEY = 'super_secret_key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'  
SQLALCHEMY_TRACK_MODIFICATIONS = False 

app.config['DEBUG'] = DEBUG
app.config['TESTING'] = TESTING
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)