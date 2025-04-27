from flask import jsonify
from src.models import CourseClass, Teacher, Student, db
from .base_controller import BaseController

class CourseClassController(BaseController[CourseClass]):
    def __init__(self):
        super().__init__()

    def get_all(self):
        return jsonify({
            "course_classes": [self._serialize(course_class) for course_class in CourseClass.query.all()]
        })

    def get_by_id(self, id: int):
        course_class = self.__validate_course_class_existence_and_return(id)
        return jsonify(self._serialize(course_class))

    def delete_by_id(self, id: int):
        course_class = self.__validate_course_class_existence_and_return(id)
        db.session.delete(course_class)
        db.session.commit()
        return "Deleted course class successfully", 200

    def update_by_id(self, id: int, teacher_id: int):
        course_class = self.__validate_course_class_existence_and_return(id)
        teacher = Teacher.query.get(teacher_id)
        if teacher is None:
            raise Exception("Professor não encontrado")
        course_class.teacher = teacher
        db.session.commit()

    def create(self, teacher_id: int):
        teacher = Teacher.query.get(teacher_id)
        if teacher is None:
            return "Professor não encontrado", 404
        course_class = CourseClass(teacher=teacher)
        db.session.add(course_class)
        db.session.commit()
        return course_class.id

    def get_students_by_course_class_id(self, id: int) -> dict:
        course_class = self.__validate_course_class_existence_and_return(id)
        return {
            "teacher": {
                "id": course_class.teacher.id,
                "name": course_class.teacher.name,
            },
            "students": [self._serialize_student(s) for s in course_class.students]
        }

    def add_student_to_course_class(self, course_class_id: int, student_id: int):
        course_class = self.__validate_course_class_existence_and_return(course_class_id)
        student = Student.query.get(student_id)
        if student is None:
            return "Aluno não encontrado", 404
        course_class.students.append(student)
        db.session.commit()
        return "Aluno adicionado com sucesso", 201

    def remove_student_from_course_class(self, course_class_id: int, student_id: int):
        course_class = self.__validate_course_class_existence_and_return(course_class_id)
        student = Student.query.get(student_id)
        if student is None:
            raise Exception("Aluno não encontrado")
        course_class.students.remove(student)
        db.session.commit()

    def __validate_course_class_existence_and_return(self, id: int) -> CourseClass:
        course_class = CourseClass.query.get(id)
        if course_class is None:
            raise Exception("Turma não encontrada")
        return course_class

    def _serialize(self, course_class: CourseClass) -> dict:
        return {
            "id": course_class.id,
            "teacher": {
                "id": course_class.teacher.id,
                "name": course_class.teacher.name
            },
            "students": [self._serialize_student(s) for s in course_class.students]
        }

    def _serialize_student(self, student: Student) -> dict:
        return {
            "id": student.id,
            "name": student.name,
            "age": student.age
        }
