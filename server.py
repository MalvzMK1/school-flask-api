from flask import Flask
from datetime import datetime
from abc import ABC


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
  
  def to_list(self) -> list[V]:
    arr: list[V] = []

    for key in self.__elements:
      arr.append(self.__elements[key])

    return arr

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


class Entity(ABC):
  def __init__(self):
    self._id = idGenerator.generate()
    self._created_at = datetime.now()

  @property
  def id(self) -> int:
    return self._id

  @property
  def created_at(self) -> datetime:
    return self._created_at

class Person(ABC):
  def __init__(self, name: str, birthdate: datetime):
    self._name = name
    self._birthdate = birthdate

  @property
  def name(self) -> str:
    return self._name

  @name.setter
  def name(self, name: str) -> None:
    self._name = name
  
  @property
  def birthdate(self) -> datetime:
    return self._birthdate

  @birthdate.setter
  def birthdate(self, birthdate: datetime) -> None:
    self._birthdate = birthdate

  @property
  def age(self) -> int:
    today = datetime.now()
    return (today - self.__birthdate).days // 365

class Teacher(Entity, Person):
  def __init__(self, name: str, birthdate: datetime):
    Entity.__init__(self)
    Person.__init__(self, name, birthdate)
    self.__course_classes = HashMap[int, CourseClass]()
  
  @property
  # TODO: type return
  def course_classes(self):
    return self.__course_classes
  
  @property
  def course_classes_ammount(self) -> int:
    return self.__course_classes.size

  def add_course_class(self, course_class) -> None:
    self.__course_classes.add(course_class.id, course_class)

  def remove_course_class_by_id(self, course_class_id: int) -> None:
    self.__course_classes.remove(course_class_id)


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


class Student(Entity, Person):
  def __init__(self, name: str, birthdate: datetime):
    Entity.__init__(self)
    Person.__init__(self, name, birthdate)
    self.__course_classes: HashMap[int, CourseClass] = {}

  @property
  def course_classes(self) -> HashMap[int, CourseClass]:
    return self.__course_classes

  @property
  def course_classes_ammount(self) -> int:
    return self.__course_classes.size

  def add_course_class(self, course_class: CourseClass) -> None:
    self.__course_classes.add(course_class.id, course_class)

  def remove_course_class_by_id(self, course_class_id: int) -> None:
    self.__course_classes.remove(course_class_id)


"""
REPOSITORIES -> Classes to interact with the Database
"""


class Repository:
  def __init__(self):
    self.__students: HashMap[int, Student] = []
    self.__teachers: HashMap[int, Teacher] = []
    self.__course_classes: HashMap[int, CourseClass] = []
  
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
    self.__students.add(student)
  
  def remove_student_by_id(self, student_id) -> None:
    self.__students.remove(student_id)

  def update_student_by_id(self, student_id: int, name: str, birthdate: datetime) -> None:
    student = self.__students.get(student_id)

    student.name = name
    student.birthdate = birthdate
  
  def add_teacher(self, teacher: Teacher) -> None:
    self.__teachers.add(teacher)

  def remove_teacher_by_id(self, teacher_id) -> None:
    self.__teachers.remove(teacher_id)

  def update_teacher_by_id(self, teacher_id: int, name: str, birthdate: datetime) -> None:
    teacher = self.__teachers.get(teacher_id)

    teacher.name = name
    teacher.birthdate = birthdate
  
  def add_course_class(self, course_class: CourseClass) -> None:
    self.__course_classes.add(course_class)
  
  def remove_course_class_by_id(self, course_class_id) -> None:
    self.__course_classes.remove(course_class_id)

  def update_course_class_by_id(self, course_class_id: int, teacher: Teacher) -> None:
    course_class = self.__course_classes.get(course_class_id)

    course_class.teacher = teacher
  
  def add_student_to_course_class(self, student: Student, course_class: CourseClass) -> None:
    course_class.add_student(student)
    student.add_course_class(course_class)
    # course_class = self.__course_classes.get(course_class_id)

    # if course_class is None:
    #   raise KeyError('Turma não encontrada')

    # student = self.__students.get(student_id)
    
    # if student is None:
    #   raise KeyError('Aluno não encontrado')

    # if course_class.students.get(student_id) is not None:
    #   raise Exception('Aluno já está incluso na turma')
    
    # course_class.add_student(student)
    # student.add_course_class(course_class)

  def remove_student_from_course_class(self, student: Student, course_class: CourseClass) -> None:
    student.remove_course_class_by_id(course_class.id)
    course_class.remove_student_by_id(student.id)


"""
CONTROLLERS -> Classes that will deal with the HTTP request
"""


"""
ROUTES -> Definition of the routes pointing to each specific controller
"""


app = Flask(__name__)


if __name__ == '__main__':
  pass
