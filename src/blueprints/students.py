from flask import Blueprint, jsonify, request, abort
from src.controllers import StudentController
from src.models import Student
from datetime import datetime

student_controller = StudentController()

student_bp = Blueprint('student', __name__, url_prefix='/students')

@student_bp.route('', methods=['GET'])
def get_all_students():
    try:
        result = student_controller.get_all()
        return jsonify({
            "students": [{"id": s.id, "name": s.name, "created_at": s.created_at} for s in result]
        })
    except Exception as e:
        abort(500, description=str(e))

@student_bp.route('/<int:id>', methods=['GET'])
def get_student_by_id(id):
    try:
        student = student_controller.get_by_id(id)
        return jsonify({
            "id": student.id, "name": student.name, "created_at": student.created_at
        })
    except Exception as e:
        abort(404, description=str(e))

@student_bp.route('/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        student_controller.delete_by_id(id)
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        abort(404, description=str(e))

@student_bp.route('/<int:id>', methods=['PUT'])
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

@student_bp.route('', methods=['POST'])
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

@student_bp.route('/<int:id>/course-classes', methods=['GET'])
def get_student_course_classes(id):
    try:
        result = student_controller.get_course_classes_by_student_id(id)

        return jsonify(result)
    except Exception as e:
        abort(404, description=str(e))
