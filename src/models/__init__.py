from .base_entity import db
from .student import Student
from .teacher import Teacher
from .course_class import CourseClass

__all__ = [
    'db',
    'Student',
    'Teacher',
    'CourseClass',
]
