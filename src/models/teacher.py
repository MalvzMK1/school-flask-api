from src.models import db
from sqlalchemy.orm import relationship

class Teacher(db.Model):
    __tablename__ = 'teacher'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    course_classes = relationship("CourseClass", back_populates="teacher")

    @property
    def age(self):
        from datetime import date
        return date.today().year - self.birthdate.year
