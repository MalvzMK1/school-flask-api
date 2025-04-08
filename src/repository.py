from datetime import datetime
from src.utils import HashMap
from src.models import Student, Teacher, CourseClass

class Repository:
  def __init__(self):
    self.__students = HashMap[int, Student]()
    self.__teachers = HashMap[int, Teacher]()
    self.__course_classes = HashMap[int, CourseClass]()
  
  @property
  def students(self) -> HashMap[int, Student]:
    return self.__students

  @property
  def teachers(self) -> HashMap[int, Teacher]:
    return self.__teachers

  @property
  def course_classes(self) -> HashMap[int, CourseClass]:
    return self.__course_classes

  def add_student(self, student: Student) -> None:
    self.__students.add(student.id, student)
  
  def delete_student_by_id(self, student_id) -> None:
    self.__students.remove(student_id)

  def update_student_by_id(self, student_id: int, name: str, birthdate: datetime = None) -> None:
    student = self.__students.get(student_id)

    if student is None: return

    student.name = name or student.name
    student.birthdate = birthdate or student.birthdate
  
  def add_teacher(self, teacher: Teacher) -> None:
    self.__teachers.add(teacher.id, teacher)

  def delete_teacher_by_id(self, teacher_id) -> None:
    self.__teachers.remove(teacher_id)

  def update_teacher_by_id(self, teacher_id: int, name: str, birthdate: datetime) -> None:
    teacher = self.__teachers.get(teacher_id)

    teacher.name = name
    teacher.birthdate = birthdate
  
  def add_course_class(self, course_class: CourseClass) -> None:
    self.__course_classes.add(course_class.id, course_class)
  
  def delete_course_class_by_id(self, course_class_id) -> None:
    self.__course_classes.remove(course_class_id)

  def update_course_class_by_id(self, course_class_id: int, teacher: Teacher) -> None:
    course_class = self.__course_classes.get(course_class_id)

    course_class.teacher = teacher
  
  def add_student_to_course_class(self, student: Student, course_class: CourseClass) -> None:
    course_class.add_student(student)
    student.add_course_class(course_class)

  def remove_student_from_course_class(self, student: Student, course_class: CourseClass) -> None:
    student.remove_course_class_by_id(course_class.id)
    course_class.remove_student_by_id(student.id)
  
repository_intance = Repository()

__all__ = [
  'repository_intance'
]
