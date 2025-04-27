from .base_entity import db, TimestampMixin, PersonMixin
from .association import course_class_student

class Student(db.Model, TimestampMixin, PersonMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    course_classes = db.relationship("CourseClass", secondary=course_class_student, back_populates="students")
