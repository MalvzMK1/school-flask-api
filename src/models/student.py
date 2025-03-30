from datetime import datetime
from .base_entity import Entity
from .person import Person
from src.utils import HashMap

class Student(Entity, Person):
  def __init__(self, name: str, birthdate: datetime):
    Entity.__init__(self)
    Person.__init__(self, name, birthdate)
    self.__course_classes = HashMap()

  @property
  def course_classes(self) -> HashMap:
    return self.__course_classes

  @property
  def course_classes_ammount(self) -> int:
    return self.__course_classes.size

  def add_course_class(self, course_class) -> None:
    self.__course_classes.add(course_class.id, course_class)

  def remove_course_class_by_id(self, course_class_id: int) -> None:
    self.__course_classes.remove(course_class_id)
