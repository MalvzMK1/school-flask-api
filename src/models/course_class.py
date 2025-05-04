from src.models import db
from sqlalchemy.orm import relationship

class CourseClass(db.Model):
    __tablename__ = 'course_class'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)

    teacher = relationship("Teacher", back_populates="course_classes")
    students = relationship("Student", back_populates="course_class")
