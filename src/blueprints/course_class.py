from flask import Blueprint, jsonify, request
from src.controllers import CourseClassController

course_class_controller = CourseClassController()

course_class_bp = Blueprint('course_class', __name__, url_prefix="/course-classes")

@course_class_bp.route('', methods=['GET'])
def get_all_course_classes():
    try:
        return course_class_controller.get_all()
    except Exception as e:
        abort(500, str(e))

@course_class_bp.route('/<int:id>', methods=['GET'])
def get_course_class_by_id(id):
    try:
        course_class = course_class_controller.get_by_id(id)

        return course_class
    except Exception as e:
        abort(404, str(e))

@course_class_bp.route('', methods=['POST'])
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

@course_class_bp.route('/<int:id>', methods=['PUT'])
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

@course_class_bp.route('/<int:id>', methods=['DELETE'])
def delete_course_class(id):
    try:
        return course_class_controller.delete_by_id(id)
    except Exception as e:
        abort(500, str(e))

@course_class_bp.route('/<int:id>/students', methods=['GET'])
def get_students_by_course_class_id(id):
    try:
        result = course_class_controller.get_students_by_course_class_id(id)
        return jsonify(result)
    except Exception as e:
        print(e)
        abort(500, str(e))

@course_class_bp.route('/<int:course_class_id>/students/<int:student_id>', methods=['DELETE'])
def remove_student_from_course_class(course_class_id, student_id):
    try:
        course_class_controller.remove_student_from_course_class(course_class_id, student_id)
        return jsonify({"message": "Student removed from course class successfully"})
    except Exception as e:
        abort(404, str(e))

@course_class_bp.route('/<int:course_class_id>/students/<int:student_id>', methods=['POST'])
def add_student_to_course_class(course_class_id, student_id):
    try:
        return course_class_controller.add_student_to_course_class(course_class_id, student_id)
    except Exception as e:
        abort(500, str(e))
