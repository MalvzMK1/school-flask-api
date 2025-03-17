from flask import Flask
from datetime import datetime
from abc import ABC, abstractmethod


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
    self._birthdate = birthdate if isinstance(birthdate, datetime) else None

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
    if self._birthdate is None: return

    today = datetime.now()
    return (today - self._birthdate).days // 365

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
  
  def delete_student_by_id(self, student_id) -> None:
    self.__students.remove(student_id)

  def update_student_by_id(self, student_id: int, name: str, birthdate: datetime) -> None:
    student = self.__students.get(student_id)

    student.name = name
    student.birthdate = birthdate
  
  def add_teacher(self, teacher: Teacher) -> None:
    self.__teachers.add(teacher)

  def delete_teacher_by_id(self, teacher_id) -> None:
    self.__teachers.remove(teacher_id)

  def update_teacher_by_id(self, teacher_id: int, name: str, birthdate: datetime) -> None:
    teacher = self.__teachers.get(teacher_id)

    teacher.name = name
    teacher.birthdate = birthdate
  
  def add_course_class(self, course_class: CourseClass) -> None:
    self.__course_classes.add(course_class)
  
  def delete_course_class_by_id(self, course_class_id) -> None:
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


# make data be atomic
# TODO: need to improve this later
repository = Repository()


"""
CONTROLLERS -> Classes that will deal with the HTTP request
"""


class BaseController[Model](ABC):
  def __init__(self):
    self._repository = repository

  @abstractmethod
  def get_all(self) -> list[Model]:
    pass

  @abstractmethod
  def get_by_id(self, id: int) -> Model:
    pass

  @abstractmethod
  def delete_by_id(self, id: int) -> None:
    pass

  @abstractmethod
  # TODO: find a way to type the data
  def update_by_id(self, id: int, *data) -> None:
    pass

  @abstractmethod
  def create(self, data: Model) -> int:
    pass

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

    return self._repository.add_student(data)
  
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

    return self._repository.add_teacher(data)
  
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
  


"""
ROUTES -> Definition of the routes pointing to each specific controller
"""


app = Flask(__name__)

if __name__ == '__main__':
  teacher = Teacher('joel', 19)
  cc = CourseClass(teacher)
  cc2 = CourseClass(teacher)

  teacher.add_course_class(cc)
  teacher.add_course_class(cc2)

  student1 = Student('ak', datetime(2006, 2, 11))
  student2 = Student('ab', datetime(2005, 2, 11))
  student3 = Student('ac', datetime(2001, 2, 11))

  cc.add_student(student1)
  cc.add_student(student2)
  cc.add_student(student3)
  cc2.add_student(student2)
  cc2.add_student(student3)

  a = list({student for course_class in teacher.course_classes.to_list() for student in course_class.students.to_list()})

  for b in a:
    print(b.name, b.age)
