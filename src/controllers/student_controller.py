from src.models import Student
from datetime import datetime
from .base_controller import BaseController

class StudentController(BaseController[Student]):
  def __init__(self):
    super().__init__()
  
  def get_all(self):
    return self._repository.students.to_list()

  def get_by_id(self, id: int):
    student = self.__validate_student_existence_and_return(id)

    return student
  
  def delete_by_id(self, id: int):
    self.__validate_student_existence_and_return(id)

    self._repository.delete_student_by_id(id)

  def update_by_id(self, id: int, name: str, birthdate: datetime):
    self.__validate_student_existence_and_return(id)

    self._repository.update_student_by_id(id, name, birthdate)
  
  def create(self, data):
    if not isinstance(data, Student):
      raise Exception('Dados incorretos')

    self._repository.add_student(data)

    return data.id
  
  def get_course_classes_by_student_id(self, id: int) -> dict:
    student = self.__validate_student_existence_and_return(id)

    return {
      "student": {
        "name": student.name,
        "age": student.age
      },
      "course_classes": student.course_classes.to_list()
    }
  
  def __validate_student_existence_and_return(self, id: int) -> Student:
    student = self._repository.students.get(id)

    if student is None:
      raise Exception('Aluno não encontrado')
    
    return student

