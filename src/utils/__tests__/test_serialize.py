import unittest
from datetime import datetime
from src.utils.serialize import serialize_teacher, serialize_course_class

class TestSerialize(unittest.TestCase):
    def test_serialize_teacher(self):
        class MockTeacher:
            def __init__(self):
                self.id = 1
                self.name = "John Doe"
                self.created_at = datetime.now()

        teacher = MockTeacher()
        serialized = serialize_teacher(teacher)

        self.assertEqual(serialized["id"], teacher.id)
        self.assertEqual(serialized["name"], teacher.name)
        self.assertEqual(serialized["created_at"], teacher.created_at)

    def test_serialize_course_class(self):
        class MockTeacher:
            def __init__(self):
                self.id = 1
                self.name = "John Doe"
                self.created_at = datetime.now()

        class MockCourseClass:
            def __init__(self):
                self.id = 1
                self.teacher = MockTeacher()
                self.created_at = datetime.now()

        course_class = MockCourseClass()
        serialized = serialize_course_class(course_class)

        self.assertEqual(serialized["id"], course_class.id)
        self.assertEqual(serialized["created_at"], course_class.created_at)
        self.assertEqual(serialized["teacher"]["id"], course_class.teacher.id)
        self.assertEqual(serialized["teacher"]["name"], course_class.teacher.name)
        self.assertEqual(serialized["teacher"]["created_at"], course_class.teacher.created_at)

if __name__ == '__main__':
    unittest.main()
