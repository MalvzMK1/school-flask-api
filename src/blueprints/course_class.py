from flask import Blueprint, jsonify, request
from src.controllers import CourseClassController
from flask import abort
from flask_restx import Namespace, Resource

course_class_controller = CourseClassController()

course_class_bp = Blueprint('course_class', __name__, url_prefix="/course-classes")

course_class_ns = Namespace('course-classes', description='Operations related to course classes')

@course_class_ns.route('')
class CourseClassList(Resource):
    @course_class_ns.doc('list_course_classes')
    @course_class_ns.response(200, 'Success')
    @course_class_ns.response(500, 'Internal Server Error')
    def get(self):
        """List all course classes"""
        try:
            return course_class_controller.get_all()
        except Exception as e:
            abort(500, str(e))

    @course_class_ns.doc('create_course_class')
    @course_class_ns.response(201, 'Course class created successfully')
    @course_class_ns.response(400, 'Invalid input')
    @course_class_ns.response(500, 'Internal Server Error')
    def post(self):
        """Create a new course class"""
        data = request.get_json()

        try:
            if not data or 'teacher_id' not in data:
                abort(400, 'Missing required field: teacher_id')

            teacher_id = data['teacher_id']
            course_class_id = course_class_controller.create(teacher_id)

            return {"id": course_class_id, "message": "Course class created successfully"}, 201

        except Exception as e:
            abort(500, str(e))

@course_class_ns.route('/<int:id>')
@course_class_ns.param('id', 'The course class identifier')
class CourseClassResource(Resource):
    @course_class_ns.doc('get_course_class')
    @course_class_ns.response(200, 'Success')
    @course_class_ns.response(404, 'Course class not found')
    def get(self, id):
        """Get a course class by ID"""
        try:
            course_class = course_class_controller.get_by_id(id)
            return course_class
        except Exception as e:
            abort(404, str(e))

    @course_class_ns.doc('update_course_class')
    @course_class_ns.response(200, 'Course class updated successfully')
    @course_class_ns.response(400, 'Invalid input')
    @course_class_ns.response(404, 'Course class not found')
    def put(self, id):
        """Update a course class"""
        try:
            data = request.get_json()

            if not data or 'teacher_id' not in data:
                abort(400, 'Missing required field: teacher_id')

            teacher_id = data['teacher_id']
            course_class_controller.update_by_id(id, teacher_id)

            return {"message": "Course class updated successfully"}

        except Exception as e:
            abort(404, str(e))

    @course_class_ns.doc('delete_course_class')
    @course_class_ns.response(200, 'Course class deleted successfully')
    @course_class_ns.response(500, 'Internal Server Error')
    def delete(self, id):
        """Delete a course class"""
        try:
            return course_class_controller.delete_by_id(id)
        except Exception as e:
            abort(500, str(e))

@course_class_ns.route('/<int:id>/students')
@course_class_ns.param('id', 'The course class identifier')
class CourseClassStudents(Resource):
    @course_class_ns.doc('get_course_class_students')
    @course_class_ns.response(200, 'Success')
    @course_class_ns.response(500, 'Internal Server Error')
    def get(self, id):
        """Get students in a course class"""
        try:
            result = course_class_controller.get_students_by_course_class_id(id)
            return result
        except Exception as e:
            print(e)
            abort(500, str(e))

@course_class_ns.route('/<int:course_class_id>/students/<int:student_id>')
@course_class_ns.param('course_class_id', 'The course class identifier')
@course_class_ns.param('student_id', 'The student identifier')
class CourseClassStudentManagement(Resource):
    @course_class_ns.doc('remove_student_from_course_class')
    @course_class_ns.response(200, 'Student removed successfully')
    @course_class_ns.response(404, 'Not found')
    def delete(self, course_class_id, student_id):
        """Remove a student from a course class"""
        try:
            course_class_controller.remove_student_from_course_class(course_class_id, student_id)
            return {"message": "Student removed from course class successfully"}
        except Exception as e:
            abort(404, str(e))

    @course_class_ns.doc('add_student_to_course_class')
    @course_class_ns.response(200, 'Success')
    @course_class_ns.response(500, 'Internal Server Error')
    def post(self, course_class_id, student_id):
        """Add a student to a course class"""
        try:
            return course_class_controller.add_student_to_course_class(course_class_id, student_id)
        except Exception as e:
            abort(500, str(e))