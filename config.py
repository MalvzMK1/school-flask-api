from flask import Flask
from src.models import db

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='super_secret_key',
    SQLALCHEMY_DATABASE_URI='sqlite:///database.sqlite3',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    DEBUG=False,
    TESTING=True
)

db.init_app(app)
