from datetime import datetime
from src.models import db
from sqlalchemy.orm import relationship

class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course_class_id = db.Column(db.Integer, db.ForeignKey('course_class.id'), nullable=True)

    course_class = relationship("CourseClass", back_populates="students")

    @property
    def age(self):
        from datetime import date
        return date.today().year - self.birthdate.year
