from flask import jsonify
from .base_controller import BaseController
from src.models import CourseClass, Student
from src.utils import serialize_course_class, serialize_teacher

class CourseClassController(BaseController[CourseClass]):
  def __init__(self):
    super().__init__()

  def get_all(self):
    return jsonify({"course_classes": [serialize_course_class(course_class) for course_class in self._repository.course_classes.to_list()]})

  def get_by_id(self, id: int):
    course_class = self.__validate_course_class_existence_and_return(id)

    if not isinstance(course_class, CourseClass):
        return "Course class not found", 404

    return jsonify(serialize_course_class(course_class))
  
  def delete_by_id(self, id: int):
    exist = self.__validate_course_class_existence_and_return(id)

    if exist is None:
        return "Course class not found", 404

    self._repository.delete_course_class_by_id(id)

    return "Deleted course class successfully", 200

  def update_by_id(self, id: int, teacher_id: int):
    self.__validate_course_class_existence_and_return(id)

    teacher = self._repository.teachers.get(teacher_id)

    if teacher is None:
      raise Exception('Professor não encontrado')

    self._repository.update_course_class_by_id(id, teacher)
  
  def create(self, teacher_id):
    teacher = self._repository.teachers.get(teacher_id)

    if teacher is None:
        return 

    course_class = CourseClass(teacher)

    self._repository.add_course_class(course_class)

    return course_class.id
  
  def get_students_by_course_class_id(self, id: int) -> dict:
    course_class = self.__validate_course_class_existence_and_return(id)

    return {
      "teacher": {
        "id": course_class.teacher.id,
        "name": course_class.teacher.name,
      },
      "students": [serialize_teacher(student) for student in course_class.students.to_list()]
    }
  
  def remove_student_from_course_class(self, course_class_id: int, student_id: int) -> None:
    course_class = self.__validate_course_class_existence_and_return(course_class_id)
    student: Student = course_class.students.get(student_id)

    if student is None:
      raise Exception('Aluno não encontrado')
    
    self._repository.remove_student_from_course_class(student, course_class)

  def add_student_to_course_class(self, course_class_id: int, student_id: int) -> None:
    course_class = self.__validate_course_class_existence_and_return(course_class_id)

    if course_class is None:
        return "Turma não encontrada", 404

    student: Student = self._repository.students.get(student_id)

    if student is None:
      return 'Aluno não encontrado', 404
    
    self._repository.add_student_to_course_class(student, course_class)

    return "Aluno adicionado com sucesso", 201
  
  def __validate_course_class_existence_and_return(self, id: int) -> CourseClass:
    course_class = self._repository.course_classes.get(id)

    return course_class
