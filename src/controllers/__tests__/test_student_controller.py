import unittest
from datetime import datetime
from src.controllers.student_controller import StudentController
from src.models import Student

class TestStudentController(unittest.TestCase):
    def setUp(self):
        self.controller = StudentController()
        self.test_student = Student("Test Student", datetime(2000, 1, 1))
        
    def test_get_all(self):
        result = self.controller.get_all()
        self.assertIsInstance(result, list)
        
    def test_get_by_id(self):
        self.controller.create(self.test_student)
        result = self.controller.get_by_id(self.test_student.id)
        self.assertIsInstance(result, Student)
        self.assertEqual(result.name, "Test Student")
        
        with self.assertRaises(Exception) as context:
            self.controller.get_by_id(999)
        self.assertEqual(str(context.exception), 'Aluno não encontrado')
        
    def test_create(self):
        student_id = self.controller.create(self.test_student)
        self.assertIsInstance(student_id, int)
        
        with self.assertRaises(Exception) as context:
            self.controller.create("invalid data")
        self.assertEqual(str(context.exception), 'Dados incorretos')
        
    def test_update_by_id(self):
        self.controller.create(self.test_student)
        new_name = "Updated Student"
        new_birthdate = datetime(2001, 1, 1)
        
        self.controller.update_by_id(self.test_student.id, new_name, new_birthdate)
        updated_student = self.controller.get_by_id(self.test_student.id)
        self.assertEqual(updated_student.name, new_name)
        
        with self.assertRaises(Exception) as context:
            self.controller.update_by_id(999, new_name, new_birthdate)
        self.assertEqual(str(context.exception), 'Aluno não encontrado')
        
    def test_delete_by_id(self):
        self.controller.create(self.test_student)
        
        self.controller.delete_by_id(self.test_student.id)
        with self.assertRaises(Exception) as context:
            self.controller.get_by_id(1)
        self.assertEqual(str(context.exception), 'Aluno não encontrado')
        
        with self.assertRaises(Exception) as context:
            self.controller.delete_by_id(999)
        self.assertEqual(str(context.exception), 'Aluno não encontrado')
        
    def test_get_course_classes_by_student_id(self):
        self.controller.create(self.test_student)
        
        result = self.controller.get_course_classes_by_student_id(self.test_student.id)
        self.assertIsInstance(result, dict)
        self.assertIn('student', result)
        self.assertIn('course_classes', result)
        
        with self.assertRaises(Exception) as context:
            self.controller.get_course_classes_by_student_id(999)
        self.assertEqual(str(context.exception), 'Aluno não encontrado')

if __name__ == '__main__':
    unittest.main()
