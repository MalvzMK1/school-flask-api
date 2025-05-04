from flask import Blueprint, jsonify, request, abort
from src.controllers import StudentController
from src.models import Student
from datetime import datetime
from flask_restx import Namespace, Resource

student_controller = StudentController()

student_bp = Blueprint('student', __name__, url_prefix='/students')

student_ns = Namespace('students', description='Operations related to students')

@student_ns.route('')
class StudentList(Resource):
    @student_ns.doc('list_students')
    @student_ns.response(200, 'Success')
    @student_ns.response(500, 'Internal Server Error')
    def get(self):
        """List all students"""
        try:
            result = student_controller.get_all()
            return {"students": result}
        except Exception as e:
            abort(500, description=str(e))

    @student_ns.doc('create_student')
    @student_ns.response(201, 'Student created successfully')
    @student_ns.response(400, 'Invalid input')
    @student_ns.response(500, 'Internal Server Error')
    def post(self):
        """Create a new student"""
        data = request.get_json()

        try:
            name = data.get('name')
            birthdate = datetime.strptime(data.get('birthdate'), '%Y-%m-%d')

            if not name or not birthdate:
                abort(400, description="Missing required fields")

            student = Student(name=name, birthdate=birthdate)
            student_controller.create(student)

            return {"id": student.id, "message": "Student created successfully"}, 201
        except ValueError:
            abort(400, description="Invalid date format. Use YYYY-MM-DD")
        except Exception as e:
            abort(500, description=str(e))

@student_ns.route('/<int:id>')
@student_ns.param('id', 'The student identifier')
class StudentResource(Resource):
    @student_ns.doc('get_student')
    @student_ns.response(200, 'Success')
    @student_ns.response(404, 'Student not found')
    def get(self, id):
        """Get a student by ID"""
        try:
            student = student_controller.get_by_id(id)
            return student
        except Exception as e:
            abort(404, description=str(e))

    @student_ns.doc('delete_student')
    @student_ns.response(200, 'Student deleted successfully')
    @student_ns.response(404, 'Student not found')
    def delete(self, id):
        """Delete a student"""
        try:
            student_controller.delete_by_id(id)
            return {"message": "Student deleted successfully"}, 200
        except Exception as e:
            abort(404, description=str(e))

    @student_ns.doc('update_student')
    @student_ns.response(200, 'Student updated successfully')
    @student_ns.response(400, 'Invalid input')
    @student_ns.response(404, 'Student not found')
    def put(self, id):
        """Update a student"""
        try:
            data = request.get_json()
            name = data.get('name')
            birthdate = datetime.strptime(data.get('birthdate'), '%Y-%m-%d')

            if not name or not birthdate:
                abort(400, description="Missing required fields")

            student_controller.update_by_id(id, name, birthdate)
            return {"message": "Student updated successfully"}
        except ValueError:
            abort(400, description="Invalid date format. Use YYYY-MM-DD")
        except Exception as e:
            abort(404, description=str(e))

@student_ns.route('/<int:id>/course-classes')
@student_ns.param('id', 'The student identifier')
class StudentCourseClasses(Resource):
    @student_ns.doc('get_student_course_classes')
    @student_ns.response(200, 'Success')
    @student_ns.response(404, 'Student not found')
    def get(self, id):
        """Get course classes for a student"""
        try:
            result = student_controller.get_course_classes_by_student_id(id)
            return result
        except Exception as e:
            abort(404, description=str(e))