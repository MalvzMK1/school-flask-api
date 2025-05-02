from flask import Blueprint, jsonify, request, abort
from datetime import datetime
from src.controllers import TeacherController
from src.models import Teacher
from src.utils.serialize import serialize_teacher

teacher_controller = TeacherController()

teacher_bp = Blueprint('teacher', __name__, url_prefix="/teachers")

# PROFESSORES
@teacher_bp.route('', methods=['GET'])
def get_all_teachers():
    try:
        teachers = teacher_controller.get_all()
        return jsonify({"teachers": teachers})
    except Exception as e:
        print(f"Erro ao obter professores: {str(e)}")  
        abort(500, str(e))


@teacher_bp.route('/<int:id>', methods=['GET'])
def get_teacher_by_id(id):
    try:
        teacher = teacher_controller.get_by_id(id)  
        return jsonify(teacher)
    except Exception as e:
        abort(404, str(e))


@teacher_bp.route('', methods=['POST'])
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

@teacher_bp.route('/<int:id>', methods=['PUT'])
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

@teacher_bp.route('/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    try:
        teacher_controller.delete_by_id(id)
        return jsonify({"message": "Teacher deleted successfully"})
    except Exception as e:
        abort(404, str(e))

@teacher_bp.route('/<int:id>/course-classes', methods=['GET'])
def get_course_classes_by_teacher_id(id):
    try:
        result = teacher_controller.get_course_classes_by_teacher_id(id)
        return jsonify(result)
    except Exception as e:
        abort(404, str(e))

@teacher_bp.route('/<int:id>/students', methods=['GET'])
def get_teacher_students_by_id(id):
    try:
        students = teacher_controller.get_teacher_students_by_id(id)
        return jsonify({"students": [
            {"id": s.id, "name": s.name, "age": s.age} for s in students
        ]})
    except Exception as e:
        abort(404, str(e))

