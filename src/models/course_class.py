from .base_entity import db, TimestampMixin
from .association import course_class_student

class CourseClass(db.Model, TimestampMixin):
    __tablename__ = 'course_classes'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)

    teacher = db.relationship("Teacher", back_populates="course_classes")
    students = db.relationship("Student", secondary=course_class_student, back_populates="course_classes")
