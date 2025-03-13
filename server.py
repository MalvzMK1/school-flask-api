from flask import Flask
from datetime import datetime


"""
UTILS -> Some useful code
"""


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



class CourseClass(Entity):
  def __init__(self):
    super().__init__()

class Student(Entity):
  def __init__(self, name: str, birth_date: datetime):
    super().__init__()

    self.__name = name
    self.__birth_date = birth_date
    self.__enrolled_course_classes: dict[int, CourseClass] = {}

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
  def enrolled_course_classes(self) -> dict[int, CourseClass]:
    return self.__enrolled_course_classes

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