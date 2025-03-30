from .student import Student
from .teacher import Teacher
from .base_entity import Entity
from src.utils import HashMap

class CourseClass(Entity):
  def __init__(self, teacher: Teacher):
    super().__init__()
    self.__teacher = teacher
    self.__students = HashMap[int, Student]()

  @property
  def teacher(self) -> Teacher:
    return self.__teacher

  @teacher.setter
  def teacher(self, new_teacher: Teacher) -> None:
    self.__teacher = new_teacher

  @property
  def students(self) -> HashMap:
    return self.__students

  @property
  def student_ammount(self) -> int:
    return self.__students.size

  def add_student(self, student: Student) -> None:
    self.__students.add(student.id, student)

  def remove_student_by_id(self, student_id: int) -> None:
    self.__students.remove(student_id)
