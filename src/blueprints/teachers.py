from flask import request, abort
from datetime import datetime
from src.controllers import TeacherController
from src.models import Teacher
from flask_restx import Namespace, Resource

teacher_controller = TeacherController()

teacher_ns = Namespace('teachers', description='Operations related to teachers')

@teacher_ns.route('')
class TeacherList(Resource):
    @teacher_ns.doc('list_teachers')
    @teacher_ns.response(200, 'Success')
    @teacher_ns.response(500, 'Internal Server Error')
    def get(self):
        """List all teachers"""
        try:
            teachers = teacher_controller.get_all()
            return {"teachers": teachers}
        except Exception as e:
            abort(500, str(e))

    @teacher_ns.doc('create_teacher')
    @teacher_ns.response(201, 'Teacher created successfully')
    @teacher_ns.response(400, 'Invalid input')
    @teacher_ns.response(500, 'Internal Server Error')
    def post(self):
        """Create a new teacher"""
        try:
            data = request.get_json()

            if not data or 'name' not in data or 'birthdate' not in data:
                abort(400, 'Missing required fields: name, birthdate')

            birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d')
            teacher_id = teacher_controller.create(Teacher(name=data['name'], birthdate=birthdate))

            return {"id": teacher_id, "message": "Professor criado com sucesso"}, 201

        except ValueError:
            abort(400, 'Invalid date format. Use YYYY-MM-DD')
        except Exception as e:
            abort(500, str(e))

@teacher_ns.route('/<int:id>')
@teacher_ns.param('id', 'The teacher identifier')
class TeacherResource(Resource):
    @teacher_ns.doc('get_teacher')
    @teacher_ns.response(200, 'Success')
    @teacher_ns.response(404, 'Teacher not found')
    def get(self, id):
        """Get a teacher by ID"""
        try:
            teacher = teacher_controller.get_by_id(id)
            return teacher
        except Exception as e:
            abort(404, str(e))

    @teacher_ns.doc('update_teacher')
    @teacher_ns.response(200, 'Teacher updated successfully')
    @teacher_ns.response(400, 'Invalid input')
    @teacher_ns.response(404, 'Teacher not found')
    def put(self, id):
        """Update a teacher"""
        try:
            data = request.get_json()

            if not data or 'name' not in data or 'birthdate' not in data:
                abort(400, 'Missing required fields: name, birthdate')

            birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d')
            teacher_controller.update_by_id(id, data['name'], birthdate)

            return {"message": "Teacher updated successfully"}

        except ValueError:
            abort(400, 'Invalid date format. Use YYYY-MM-DD')
        except Exception as e:
            abort(404, str(e))

    @teacher_ns.doc('delete_teacher')
    @teacher_ns.response(200, 'Teacher deleted successfully')
    @teacher_ns.response(404, 'Teacher not found')
    def delete(self, id):
        """Delete a teacher"""
        try:
            teacher_controller.delete_by_id(id)
            return {"message": "Teacher deleted successfully"}
        except Exception as e:
            abort(404, str(e))

@teacher_ns.route('/<int:id>/course-classes')
@teacher_ns.param('id', 'The teacher identifier')
class TeacherCourseClasses(Resource):
    @teacher_ns.doc('get_teacher_course_classes')
    @teacher_ns.response(200, 'Success')
    @teacher_ns.response(404, 'Teacher not found')
    def get(self, id):
        """Get course classes for a teacher"""
        try:
            result = teacher_controller.get_course_classes_by_teacher_id(id)
            return result
        except Exception as e:
            abort(404, str(e))

@teacher_ns.route('/<int:id>/students')
@teacher_ns.param('id', 'The teacher identifier')
class TeacherStudents(Resource):
    @teacher_ns.doc('get_teacher_students')
    @teacher_ns.response(200, 'Success')
    @teacher_ns.response(404, 'Teacher not found')
    def get(self, id):
        """Get students for a teacher"""
        try:
            students = teacher_controller.get_teacher_students_by_id(id)
            return {"students": [
                {"id": s.id, "name": s.name, "age": s.age} for s in students
            ]}
        except Exception as e:
            abort(404, str(e))