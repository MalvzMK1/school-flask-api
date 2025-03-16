import requests
import unittest

class TestSchoolMethods(unittest.TestCase):

    BASE_URL = 'http://localhost:5000'

    def test_001_create_teacher(self):
        response = requests.post(
            f'{self.BASE_URL}/teacher',
            json={'name': 'John Doe', 'birthdate': '1985-05-15'}
        )

        self.assertEqual(response.status_code, 201)

        # Verificando se o nome e a data de nascimento estão corretos
        response_json = response.json()
        self.assertEqual(response_json['name'], 'John Doe')
        self.assertEqual(response_json['birthdate'], '1985-05-15')

    def test_002_create_student(self):
        response = requests.post(
            f'{self.BASE_URL}/student',
            json={'name': 'Jane Smith', 'birthdate': '2000-03-20'}
        )

        self.assertEqual(response.status_code, 201)

        # Verificando se o nome e a data de nascimento estão corretos
        response_json = response.json()
        self.assertEqual(response_json['name'], 'Jane Smith')
        self.assertEqual(response_json['birthdate'], '2000-03-20')

    def test_003_create_course_class(self):
        response_teacher = requests.post(
            f'{self.BASE_URL}/teacher',
            json={'name': 'John Doe', 'birthdate': '1985-05-15'}
        )
        teacher_id = response_teacher.json()['id']

        response_course_class = requests.post(
            f'{self.BASE_URL}/course_class',
            json={'teacher_id': teacher_id}
        )

        self.assertEqual(response_course_class.status_code, 201)

        # Verificando se a turma foi criada corretamente
        response_json = response_course_class.json()
        self.assertEqual(response_json['teacher_id'], teacher_id)
        self.assertEqual(response_json['teacher_name'], 'John Doe')

if __name__ == '__main__':
    unittest.main()
