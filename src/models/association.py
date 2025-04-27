from .base_entity import db

course_class_student = db.Table(
    'course_class_student',
    db.Column('course_class_id', db.Integer, db.ForeignKey('course_classes.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True)
)
