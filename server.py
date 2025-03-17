from flask import Flask, jsonify, request, abort
from datetime import datetime
from abc import ABC, abstractmethod


"""
UTILS -> Some useful code
"""
def serialize_teacher(teacher):
    return {
        "id": teacher.id,
        "name": teacher.name,
        "created_at": teacher.created_at
    }

def serialize_course_class(course_class):
    return {
        "id": course_class.id,
        "teacher": serialize_teacher(course_class.teacher),
        "created_at": course_class.created_at
    }

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
    self.__course_classes = HashMap[int, CourseClass]()

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

  def update_student_by_id(self, student_id: int, name: str, birthdate: datetime) -> None:
    student = self.__students.get(student_id)

    student.name = name
    student.birthdate = birthdate
  
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
  

class CourseClassController(BaseController[CourseClass]):
  def __init__(self):
    super().__init__()

  def get_all(self):
    return self._repository.course_classes.to_list()

  def get_by_id(self, id: int):
    course_class = self.__validate_course_class_existence_and_return(id)

    return course_class
  
  def delete_by_id(self, id: int):
    self.__validate_course_class_existence_and_return(id)

    self._repository.delete_course_class_by_id(id)

  def update_by_id(self, id: int, teacher_id: int):
    self.__validate_course_class_existence_and_return(id)

    teacher = self._repository.teachers.get(teacher_id)

    if teacher is None:
      raise Exception('Professor não encontrado')

    self._repository.update_course_class_by_id(id, teacher)
  
  def create(self, data):
    if not isinstance(data, Student):
      raise Exception('Dados incorretos')

    return self._repository.add_student(data)
  
  def get_students_by_course_class_id(self, id: int) -> dict:
    course_class = self.__validate_course_class_existence_and_return(id)

    return {
      "teacher": {
        "id": course_class.teacher.id,
        "name": course_class.teacher.name,
      },
      "students": course_class.students.to_list()
    }
  
  def remove_student_from_course_class(self, course_class_id: int, student_id: int) -> None:
    course_class = self.__validate_course_class_existence_and_return(course_class_id)
    student: Student = course_class.students.get(student_id)

    if student is None:
      raise Exception('Aluno não encontrado')
    
    self._repository.remove_student_from_course_class(student, course_class)
  
  def __validate_course_class_existence_and_return(self, id: int) -> CourseClass:
    course_class = self._repository.course_classes.get(id)

    if course_class is None:
      raise Exception('Turma não encontrada')
    
    return course_class


"""
ROUTES -> Definition of the routes pointing to each specific controller
"""
app = Flask(__name__)
student_controller = StudentController()
teacher_controller = TeacherController()
course_class_controller = CourseClassController()


## ALUNOS
@app.route('/students', methods=['GET'])
def get_all_students():
    try:
        result = student_controller.get_all()
        return jsonify({
            "students": [{"id": s.id, "name": s.name, "created_at": s.created_at} for s in result]
        })
    except Exception as e:
        abort(500, description=str(e))

@app.route('/students/<int:id>', methods=['GET'])
def get_student_by_id(id):
    try:
        student = student_controller.get_by_id(id)
        return jsonify({
            "id": student.id, "name": student.name, "created_at": student.created_at
        })
    except Exception as e:
        abort(404, description=str(e))

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        student_controller.delete_by_id(id)
        return jsonify({"message": "Student deleted successfully"}), 204
    except Exception as e:
        abort(404, description=str(e))

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        data = request.get_json()
        name = data.get('name')
        birthdate = datetime.strptime(data.get('birthdate'), '%Y-%m-%d')

        if not name or not birthdate:
            abort(400, description="Missing required fields")

        student_controller.update_by_id(id, name, birthdate)
        return jsonify({"message": "Student updated successfully"})
    except ValueError:
        abort(400, description="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        abort(404, description=str(e))

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()

    try:
        name = data.get('name')
        birthdate = datetime.strptime(data.get('birthdate'), '%Y-%m-%d')

        if not name or not birthdate:
            abort(400, description="Missing required fields")

        student = Student(name=name, birthdate=birthdate)
        student_controller.create(student)

        return jsonify({"id": student.id, "message": "Student created successfully"}), 201
    except ValueError:
        abort(400, description="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        abort(500, description=str(e))

@app.route('/students/<int:id>/course-classes', methods=['GET'])
def get_student_course_classes(id):
    try:
        result = student_controller.get_course_classes_by_student_id(id)

        return jsonify(result)
    except Exception as e:
        abort(404, description=str(e))


## PROFESSORES
@app.route('/teachers', methods=['GET'])
def get_all_teachers():
    try:
        teachers = teacher_controller.get_all()
        return jsonify({"teachers": [serialize_teacher(t) for t in teachers]})
    except Exception as e:
        abort(500, str(e))

@app.route('/teachers/<int:id>', methods=['GET'])
def get_teacher_by_id(id):
    try:
        teacher = teacher_controller.get_by_id(id)
        return jsonify(serialize_teacher(teacher))
    except Exception as e:
        abort(404, str(e))

@app.route('/teachers', methods=['POST'])
def create_teacher():
    try:
        data = request.get_json()

        if not data or 'name' not in data or 'birthdate' not in data:
            abort(400, 'Missing required fields: name, birthdate')

        birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d')
        teacher_id = teacher_controller.create(Teacher(name=data['name'], birthdate=birthdate))

        return jsonify({"id": teacher_id}), 201

    except ValueError:
        abort(400, 'Invalid date format. Use YYYY-MM-DD')
    except Exception as e:
        abort(500, str(e))

@app.route('/teachers/<int:id>', methods=['PUT'])
def update_teacher(id):
    try:
        data = request.get_json()

        if not data or 'name' not in data or 'birthdate' not in data:
            abort(400, 'Missing required fields: name, birthdate')

        birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d')
        teacher_controller.update_by_id(id, data['name'], birthdate)

        return jsonify({"message": "Teacher updated successfully"})

    except ValueError:
        abort(400, 'Invalid date format. Use YYYY-MM-DD')
    except Exception as e:
        abort(404, str(e))

@app.route('/teachers/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    try:
        teacher_controller.delete_by_id(id)
        return jsonify({"message": "Teacher deleted successfully"})
    except Exception as e:
        abort(404, str(e))

@app.route('/teachers/<int:id>/course-classes', methods=['GET'])
def get_course_classes_by_teacher_id(id):
    try:
        result = teacher_controller.get_course_classes_by_teacher_id(id)
        return jsonify(result)
    except Exception as e:
        abort(404, str(e))

@app.route('/teachers/<int:id>/students', methods=['GET'])
def get_teacher_students_by_id(id):
    try:
        students = teacher_controller.get_teacher_students_by_id(id)
        return jsonify({"students": [
            {"id": s.id, "name": s.name, "age": s.age} for s in students
        ]})
    except Exception as e:
        abort(404, str(e))


## TURMAS
@app.route('/course-classes', methods=['GET'])
def get_all_course_classes():
    try:
        course_classes = course_class_controller.get_all()
        return jsonify({"course_classes": [serialize_course_class(c) for c in course_classes]})
    except Exception as e:
        abort(500, str(e))

@app.route('/course-classes/<int:id>', methods=['GET'])
def get_course_class_by_id(id):
    try:
        course_class = course_class_controller.get_by_id(id)
        return jsonify(serialize_course_class(course_class))
    except Exception as e:
        abort(404, str(e))

@app.route('/course-classes', methods=['POST'])
def create_course_class():
    try:
        data = request.get_json()

        if not data or 'teacher_id' not in data:
            abort(400, 'Missing required field: teacher_id')

        teacher_id = data['teacher_id']
        course_class_id = course_class_controller.create(CourseClass(teacher_id=teacher_id))

        return jsonify({"id": course_class_id}), 201

    except Exception as e:
        abort(500, str(e))

@app.route('/course-classes/<int:id>', methods=['PUT'])
def update_course_class(id):
    try:
        data = request.get_json()

        if not data or 'teacher_id' not in data:
            abort(400, 'Missing required field: teacher_id')

        teacher_id = data['teacher_id']
        course_class_controller.update_by_id(id, teacher_id)

        return jsonify({"message": "Course class updated successfully"})

    except Exception as e:
        abort(404, str(e))

@app.route('/course-classes/<int:id>', methods=['DELETE'])
def delete_course_class(id):
    try:
        course_class_controller.delete_by_id(id)
        return jsonify({"message": "Course class deleted successfully"})
    except Exception as e:
        abort(404, str(e))

@app.route('/course-classes/<int:id>/students', methods=['GET'])
def get_students_by_course_class_id(id):
    try:
        result = course_class_controller.get_students_by_course_class_id(id)
        return jsonify(result)
    except Exception as e:
        abort(404, str(e))

@app.route('/course-classes/<int:course_class_id>/students/<int:student_id>', methods=['DELETE'])
def remove_student_from_course_class(course_class_id, student_id):
    try:
        course_class_controller.remove_student_from_course_class(course_class_id, student_id)
        return jsonify({"message": "Student removed from course class successfully"})
    except Exception as e:
        abort(404, str(e))


if __name__ == '__main__':
  app.run(debug=True)
