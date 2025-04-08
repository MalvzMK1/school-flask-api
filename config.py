from flask import Flask

app = Flask(__name__)

DEBUG = True
TESTING = True
SECRET_KEY = 'super_secret_key'

app.config['DEBUG'] = DEBUG
app.config['TESTING'] = TESTING
app.config['SECRET_KEY'] = SECRET_KEY
