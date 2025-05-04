from datetime import datetime
from flask import jsonify
from src.models import Student, CourseClass, db
from .base_controller import BaseController

class StudentController(BaseController[Student]):
    def __init__(self):
        super().__init__()

    def get_all(self):
        students = Student.query.all()
        return [self._serialize(student) for student in students]

    def get_by_id(self, id: int):
        student = self.__validate_student_existence_and_return(id)
        return self._serialize(student)

    def delete_by_id(self, id: int):
        student = self.__validate_student_existence_and_return(id)
        db.session.delete(student)
        db.session.commit()

    def update_by_id(self, id: int, name: str, birthdate: datetime):
        student = self.__validate_student_existence_and_return(id)
        student.name = name
        student.birthdate = birthdate
        db.session.commit()

    def create(self, data: Student) -> int:
        if not isinstance(data, Student):
            raise Exception('Dados incorretos')
        
        db.session.add(data)
        db.session.commit()
        return data.id

    def get_course_classes_by_student_id(self, id: int) -> dict:
        student = self.__validate_student_existence_and_return(id)

        return {
            "student": {
                "id": student.id,
                "name": student.name,
                "age": student.age
            },
            "course_classes": [
                {
                    "id": cc.id,
                    "teacher": {
                        "id": cc.teacher.id,
                        "name": cc.teacher.name
                    }
                } for cc in student.course_classes
            ]
        }

    def __validate_student_existence_and_return(self, id: int) -> Student:
        student = Student.query.get(id)
        if student is None:
            raise Exception("Aluno não encontrado")
        return student

    def _serialize(self, student: Student) -> dict:
        return {
            "id": student.id,
            "name": student.name,
            "birthdate": student.birthdate.strftime("%Y-%m-%d"),
            "age": student.age
        }
