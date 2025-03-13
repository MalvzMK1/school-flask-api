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
  app.run()
