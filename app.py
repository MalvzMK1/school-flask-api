from flask import Flask, jsonify, request, abort
from datetime import datetime
from src.controllers import StudentController, TeacherController, CourseClassController
from src.models import Student, Teacher
from src.utils import serialize_teacher


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

        return jsonify({"id": teacher_id, "message": "Professor criado com sucesso"}), 201

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
        return course_class_controller.get_all()
    except Exception as e:
        abort(500, str(e))

@app.route('/course-classes/<int:id>', methods=['GET'])
def get_course_class_by_id(id):
    try:
        course_class = course_class_controller.get_by_id(id)

        return course_class
    except Exception as e:
        abort(404, str(e))

@app.route('/course-classes', methods=['POST'])
def create_course_class():
    data = request.get_json()

    try:
        if not data or 'teacher_id' not in data:
            abort(400, 'Missing required field: teacher_id')

        teacher_id = data['teacher_id']
        course_class_id = course_class_controller.create(teacher_id)

        return jsonify({"id": course_class_id, "message": "Course class created successfully"}), 201

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
        return course_class_controller.delete_by_id(id)
    except Exception as e:
        abort(500, str(e))

@app.route('/course-classes/<int:id>/students', methods=['GET'])
def get_students_by_course_class_id(id):
    try:
        result = course_class_controller.get_students_by_course_class_id(id)
        return jsonify(result)
    except Exception as e:
        print(e)
        abort(500, str(e))

@app.route('/course-classes/<int:course_class_id>/students/<int:student_id>', methods=['DELETE'])
def remove_student_from_course_class(course_class_id, student_id):
    try:
        course_class_controller.remove_student_from_course_class(course_class_id, student_id)
        return jsonify({"message": "Student removed from course class successfully"})
    except Exception as e:
        abort(404, str(e))

@app.route('/course-classes/<int:course_class_id>/students/<int:student_id>', methods=['POST'])
def add_student_to_course_class(course_class_id, student_id):
    try:
        return course_class_controller.add_student_to_course_class(course_class_id, student_id)
    except Exception as e:
        abort(500, str(e))


if __name__ == '__main__':
  app.run(debug=True)
