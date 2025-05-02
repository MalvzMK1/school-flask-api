from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PersonMixin:
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    @property
    def age(self):
        return (datetime.now().date() - self.birthdate).days // 365
