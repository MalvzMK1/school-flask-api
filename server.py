from flask import Flask
from datetime import datetime


"""
UTILS -> Some useful code
"""

class HashMap[K, V]:
  def __init__(self):
    self.__size = 0
    self.__elements: dict[K, V] = {}

  @property
  def size(self) -> int:
    return self.__size

  def add(self, key: K, value: V) -> None:
    if key not in self.__elements:
      self.__elements[key] = value

      self.__size += 1

  def remove(self, key: K) -> None:
    if key in self.__elements:
      self.__elements.pop(key)
      self.__size -= 1

  def get(self, key: K) -> V:
    return self.__elements[key] if key in self.__elements else None

  def __repr__(self):
    return self.__elements.__str__()



class IdGenerator:
  def __init__(self):
    self.__next_id = 1

  def generate(self) -> int:
    id = self.__next_id

    self.__next_id += 1

    return id


idGenerator = IdGenerator()


"""
MODELS -> Representation of the entities
"""


class Entity:
  def __init__(self):
    self._id = idGenerator.generate()
    self._created_at = datetime.now()

  @property
  def id(self) -> int:
    return self._id

  @property
  def created_at(self) -> datetime:
    return self._created_at



class Teacher(Entity):
  def __init__(self):
    super().__init__()


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

  # TODO: type parameter
  def add_student(self, student) -> None:
    self.__students.add(student.id, student)

  # TODO: type parameter
  def remove_student_by_id(self, student_id: int) -> None:
    self.__students.remove(student_id)


class Student(Entity):
  def __init__(self, name: str, birth_date: datetime):
    super().__init__()

    self.__name = name
    self.__birth_date = birth_date
    self.__enrolled_course_classes: HashMap[int, CourseClass] = {}

  @property
  def name(self) -> str:
    return self.__name

  @name.setter
  def name(self, name: str) -> None:
    self.__name = name

  @property
  def birth_date(self) -> datetime:
    return self.__birth_date

  @birth_date.setter
  def birth_date(self, birth_date: datetime) -> None:
    self.__birth_date = birth_date

  @property
  def age(self) -> int:
    now = datetime.now()

    return (now - self.__birth_date).days // 365

  @property
  def enrolled_course_classes(self) -> HashMap[int, CourseClass]:
    return self.__enrolled_course_classes

  def add_course_class(self, course_class: CourseClass) -> None:
    self.__enrolled_course_classes.add(course_class.id, course_class)

  def remove_course_class(self, course_class_id: int) -> None:
    self.__enrolled_course_classes.remove(course_class_id)

"""
REPOSITORIES -> Classes to interact with the Database
"""


"""
CONTROLLERS -> Classes that will deal with the HTTP request
"""


"""
ROUTES -> Definition of the routes pointing to each specific controller
"""


app = Flask(__name__)


if __name__ == '__main__':
  pass
