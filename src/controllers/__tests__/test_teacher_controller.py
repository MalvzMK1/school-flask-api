import unittest
from datetime import datetime
from src.controllers.teacher_controller import TeacherController
from src.models import Teacher, CourseClass, Student

class TestTeacherController(unittest.TestCase):
    def setUp(self):
        self.controller = TeacherController()
        self.test_teacher = Teacher("Test Teacher", datetime(1980, 1, 1))
        
    def test_get_all(self):
        teachers = self.controller.get_all()
        self.assertIsInstance(teachers, list)
        
    def test_get_by_id(self):
        self.controller.create(self.test_teacher)
        teacher = self.controller.get_by_id(self.test_teacher.id)
        self.assertIsInstance(teacher, Teacher)
        
        with self.assertRaises(Exception):
            self.controller.get_by_id(999)
            
    def test_delete_by_id(self):
        with self.assertRaises(Exception):
            self.controller.delete_by_id(999)
            
    def test_update_by_id(self):
        with self.assertRaises(Exception):
            self.controller.update_by_id(999, "New Name", datetime.now())
            
    def test_create(self):
        new_teacher = Teacher("New Teacher", datetime(1990, 1, 1))
        teacher_id = self.controller.create(new_teacher)
        self.assertIsInstance(teacher_id, int)
        
        with self.assertRaises(Exception):
            self.controller.create("invalid data")
            
    def test_get_course_classes_by_teacher_id(self):
        self.controller.create(self.test_teacher)
        course_class = CourseClass(self.test_teacher)
        self.test_teacher.add_course_class(course_class)
        result = self.controller.get_course_classes_by_teacher_id(self.test_teacher.id)
        self.assertIsInstance(result, dict)
        self.assertIn("teacher", result)
        self.assertIn("course_classes", result)
        self.assertEqual(result['course_classes'][0], course_class)
        
        with self.assertRaises(Exception):
            self.controller.get_course_classes_by_teacher_id(999)
            
    def test_get_teacher_students_by_id(self):
        self.controller.create(self.test_teacher)
        students = self.controller.get_teacher_students_by_id(self.test_teacher.id)
        self.assertIsInstance(students, list)
        
        with self.assertRaises(Exception):
            self.controller.get_teacher_students_by_id(999)
            
    def test_validate_teacher_existence(self):
        with self.assertRaises(Exception):
            self.controller._TeacherController__validate_teacher_existence_and_return(999)

if __name__ == '__main__':
    unittest.main()
