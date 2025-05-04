from datetime import datetime
from src.models import Teacher, db
from .base_controller import BaseController

class TeacherController(BaseController[Teacher]):
    def __init__(self):
        super().__init__()

    def get_all(self):
      try:
        teachers = Teacher.query.all()
        if not teachers:
            raise Exception("Nenhum professor encontrado.")
        return [self._serialize(t) for t in teachers]
      except Exception as e:
        print(f"Erro ao obter professores: {str(e)}")
        raise Exception("Erro ao tentar obter todos os professores.")  # Detalhar o erro


    def get_by_id(self, id: int):
        teacher = self.__validate_teacher_existence_and_return(id)
        return self._serialize(teacher)

    def delete_by_id(self, id: int):
        teacher = self.__validate_teacher_existence_and_return(id)
        db.session.delete(teacher)
        db.session.commit()

    def update_by_id(self, id: int, name: str, birthdate: datetime):
        teacher = self.__validate_teacher_existence_and_return(id)
        teacher.name = name
        teacher.birthdate = birthdate
        db.session.commit()

    def create(self, data: Teacher) -> int:
        if not isinstance(data, Teacher):
            raise Exception("Dados incorretos")
        db.session.add(data)
        db.session.commit()
        return data.id

    def get_course_classes_by_teacher_id(self, id: int) -> dict:
        teacher = self.__validate_teacher_existence_and_return(id)
        return {
            "teacher": {
                "name": teacher.name,
                "age": teacher.age
            },
            "course_classes": [
                {"id": cc.id} for cc in teacher.course_classes
            ]
        }

    def get_teacher_students_by_id(self, id: int):
        teacher = self.__validate_teacher_existence_and_return(id)
        students = {student.id: student for cc in teacher.course_classes for student in cc.students}
        return [self._serialize_student(s) for s in students.values()]

    def __validate_teacher_existence_and_return(self, id: int) -> Teacher:
        teacher = Teacher.query.get(id)
        if teacher is None:
            raise Exception("Professor não encontrado")
        return teacher

    def _serialize(self, teacher: Teacher) -> dict:
        return {
            "id": teacher.id,
            "name": teacher.name,
            "birthdate": teacher.birthdate.strftime("%Y-%m-%d"),
            "age": teacher.age
        }

    def _serialize_student(self, student):
        return {
            "id": student.id,
            "name": student.name,
            "age": student.age
        }
