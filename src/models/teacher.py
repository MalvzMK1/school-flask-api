from .base_entity import db, TimestampMixin, PersonMixin

class Teacher(db.Model, TimestampMixin, PersonMixin):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    course_classes = db.relationship("CourseClass", back_populates="teacher")
