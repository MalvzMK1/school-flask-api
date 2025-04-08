import unittest
from datetime import datetime
from src.models import Student, Teacher, CourseClass
from src.repository import Repository 

class TestRepository(unittest.TestCase):
    def setUp(self):
        self.repository = Repository()
        self.student = Student("John Doe", datetime(2000, 1, 1))
        self.teacher = Teacher("Jane Smith", datetime(1980, 1, 1))
        self.course_class = CourseClass(self.teacher)

    def test_add_student(self):
        self.repository.add_student(self.student)
        self.assertEqual(self.repository.students.get(self.student.id), self.student)
    
    def test_delete_student_by_id(self):
        self.repository.add_student(self.student)
        self.assertTrue(self.repository.students.get(self.student.id) is not None)
        self.repository.delete_student_by_id(self.student.id)
        student = self.repository.students.get(self.student.id)
        self.assertIsNone(student)
    
    def test_update_student_by_id(self):
        self.repository.add_student(self.student)
        self.assertIsNotNone(self.repository.students.get(self.student.id))
        self.repository.update_student_by_id(self.student.id, "Jack Doe")
        student = self.repository.students.get(self.student.id)
        self.assertIsNotNone(student)
        self.assertEqual(student.id, self.student.id)
        self.assertEqual(student.age, self.student.age)
        self.assertEqual(student.name, "Jack Doe")

    def test_add_teacher(self):
        self.repository.add_teacher(self.teacher)
        self.assertIsNotNone(self.repository.teachers.get(self.teacher.id))
    
    def test_delete_teacher_by_id(self):
        self.repository.add_teacher(self.teacher)
        self.assertIsNotNone(self.repository.teachers.get(self.teacher.id))
        self.repository.delete_teacher_by_id(self.teacher.id)
        self.assertIsNone(self.repository.teachers.get(self.teacher.id))
    
    def test_update_teacher_by_id(self):
        self.repository.add_teacher(self.teacher)
        self.assertIsNotNone(self.repository.teachers.get(self.teacher.id))
        new_name = "Jane Doe"
        new_birthdate = datetime(1985, 1, 1)
        self.repository.update_teacher_by_id(self.teacher.id, new_name, new_birthdate)
        teacher = self.repository.teachers.get(self.teacher.id)
        self.assertEqual(teacher.name, new_name)
        self.assertEqual(teacher.birthdate, new_birthdate)

    def test_add_course_class(self):
        self.repository.add_course_class(self.course_class)
        self.assertIsNotNone(self.repository.course_classes.get(self.course_class.id))

    def test_delete_course_class_by_id(self):
        self.repository.add_course_class(self.course_class)
        self.assertIsNotNone(self.repository.course_classes.get(self.course_class.id))
        self.repository.delete_course_class_by_id(self.course_class.id)
        self.assertIsNone(self.repository.course_classes.get(self.course_class.id))

    def test_update_course_class_by_id(self):
        self.repository.add_course_class(self.course_class)
        new_teacher = Teacher("New Teacher", datetime(1990, 1, 1))
        self.repository.update_course_class_by_id(self.course_class.id, new_teacher)
        course_class = self.repository.course_classes.get(self.course_class.id)
        self.assertEqual(course_class.teacher, new_teacher)

    def test_add_student_to_course_class(self):
        self.repository.add_student_to_course_class(self.student, self.course_class)
        self.assertIn(self.student, self.course_class.students.to_list())
        self.assertIn(self.course_class, self.student.course_classes.to_list())

    def test_remove_student_from_course_class(self):
        self.repository.add_student_to_course_class(self.student, self.course_class)
        self.repository.remove_student_from_course_class(self.student, self.course_class)
        self.assertNotIn(self.student, self.course_class.students.to_list())
        self.assertNotIn(self.course_class, self.student.course_classes.to_list())

if __name__ == '__main__':
    unittest.main()
