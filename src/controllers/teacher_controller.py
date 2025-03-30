from datetime import datetime
from src.models import Teacher, Student
from .base_controller import BaseController

class TeacherController(BaseController[Teacher]):
  def __init__(self):
    super().__init__()

  def get_all(self):
    return self._repository.teachers.to_list()

  def get_by_id(self, id: int):
    teacher = self.__validate_teacher_existence_and_return(id)

    return teacher
  
  def delete_by_id(self, id: int):
    self.__validate_teacher_existence_and_return(id)

    self._repository.delete_teacher_by_id(id)

  def update_by_id(self, id: int, name: str, birthdate: datetime):
    self.__validate_teacher_existence_and_return(id)

    self._repository.update_teacher_by_id(id, name, birthdate)
  
  def create(self, data):
    if not isinstance(data, Teacher):
      raise Exception('Dados incorretos')

    self._repository.add_teacher(data)

    return data.id
  
  def get_course_classes_by_teacher_id(self, id: int) -> dict:
    teacher = self.__validate_teacher_existence_and_return(id)

    return {
      "teacher": {
        "name": teacher.name,
        "age": teacher.age
      },
      "course_classes": teacher.course_classes.to_list()
    }
  
  def get_teacher_students_by_id(self, id: int) -> list[Student]:
    teacher = self.__validate_teacher_existence_and_return(id)
    students_set = set[Student]()

    for course_class in teacher.course_classes.to_list():
      for student in course_class.students.to_list():
        students_set.add(student)

    return list(students_set)

  def __validate_teacher_existence_and_return(self, id) -> Teacher:
    teacher = self._repository.teachers.get(id)

    if teacher is None:
      raise Exception('Professor não encontrado')
    
    return teacher
  
