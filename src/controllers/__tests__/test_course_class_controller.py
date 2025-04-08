import unittest
from datetime import datetime
from src.controllers.course_class_controller import CourseClassController
from src.models import CourseClass, Teacher, Student
from src.repository import Repository

class TestCourseClassController(unittest.TestCase):
    def setUp(self):
        self.controller = CourseClassController()
        self.repository = Repository()
        self.controller._repository = self.repository
        
        self.teacher = Teacher("Test Teacher", datetime(2002, 5, 14))
        self.repository.add_teacher(self.teacher)
        
        self.course_class = CourseClass(self.teacher)
        self.repository.add_course_class(self.course_class)
        
        self.student = Student("Test Student", datetime(2006, 2, 11))
        self.repository.add_student(self.student)

    # EXPECTED ERROR: Running outside a module
    # TODO: Try to find a way to test this or refactor controller
    # def test_get_all(self):
    #     response = self.controller.get_all()
    #     self.assertEqual(response.status_code, 200)

    # EXPECTED ERROR: Running outside a module
    # TODO: Try to find a way to test this or refactor controller
    # def test_get_by_id(self):
    #     response = self.controller.get_by_id(self.course_class.id)
    #     self.assertEqual(response.status_code, 200)
        
    #     response = self.controller.get_by_id(999)
    #     self.assertEqual(response[1], 404)

    def test_delete_by_id(self):
        response = self.controller.delete_by_id(self.course_class.id)
        self.assertEqual(response[1], 200)
        
        response = self.controller.delete_by_id(999)
        self.assertEqual(response[1], 404)

    def test_update_by_id(self):
        new_teacher = Teacher("New Teacher", datetime(1999, 1, 1))
        self.repository.add_teacher(new_teacher)
        
        self.controller.update_by_id(self.course_class.id, new_teacher.id)
        updated_class = self.repository.course_classes.get(self.course_class.id)
        self.assertEqual(updated_class.teacher.id, new_teacher.id)
        
        with self.assertRaises(Exception):
            self.controller.update_by_id(self.course_class.id, 999)

    def test_create(self):
        new_id = self.controller.create(self.teacher.id)
        self.assertIsNotNone(new_id)
        
        result = self.controller.create(999)
        self.assertIsNone(result)

    def test_get_students_by_course_class_id(self):
        response = self.controller.get_students_by_course_class_id(self.course_class.id)
        self.assertIn('teacher', response)
        self.assertIn('students', response)

    def test_remove_student_from_course_class(self):
        self.repository.add_student_to_course_class(self.student, self.course_class)
        
        self.controller.remove_student_from_course_class(self.course_class.id, self.student.id)
        updated_class = self.repository.course_classes.get(self.course_class.id)
        self.assertNotIn(self.student, updated_class.students.to_list())
        
        with self.assertRaises(Exception):
            self.controller.remove_student_from_course_class(self.course_class.id, 999)

    def test_add_student_to_course_class(self):
        response = self.controller.add_student_to_course_class(self.course_class.id, self.student.id)
        self.assertEqual(response[1], 201)
        
        response = self.controller.add_student_to_course_class(999, self.student.id)
        self.assertEqual(response[1], 404)
        
        response = self.controller.add_student_to_course_class(self.course_class.id, 999)
        self.assertEqual(response[1], 404)

if __name__ == '__main__':
    unittest.main()
