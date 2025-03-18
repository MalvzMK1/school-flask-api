import requests
import unittest

class TestSchoolMethods(unittest.TestCase):

    BASE_URL = 'http://localhost:5000'

    def setUp(self):
        """
        Método chamado antes de cada teste. Ele garante que o professor, aluno
        e turma sejam criados antes de cada teste, assim o teacher_id, student_id
        e course_class_id estarão disponíveis.
        """
        # Criando um professor antes de cada teste
        response_teacher = requests.post(
            f'{self.BASE_URL}/teachers',
            json={'name': 'John Doe', 'birthdate': '1985-05-15'}
        )
        self.assertEqual(response_teacher.status_code, 201)
        
        response_teacher_json = response_teacher.json()
        self.teacher_id = response_teacher_json['id']

        # Criando um aluno antes de cada teste
        response_student = requests.post(
            f'{self.BASE_URL}/students',
            json={'name': 'Jane Smith', 'birthdate': '2000-03-20'}
        )
        self.assertEqual(response_student.status_code, 201)
        
        response_student_json = response_student.json()
        self.student_id = response_student_json['id']

        # Criando uma turma antes de cada teste
        response_course_class = requests.post(
            f'{self.BASE_URL}/course-classes',
            json={'teacher_id': self.teacher_id}
        )

        self.assertEqual(response_course_class.status_code, 201)

        response_course_class_json = response_course_class.json()
        self.course_class_id = response_course_class_json['id']

    def test_001_create_teacher(self):
        """
        Teste que cria um professor. O professor é criado no método setUp,
        então este teste apenas verifica se o professor foi realmente criado.
        """
        response = requests.get(f'{self.BASE_URL}/teachers/{self.teacher_id}')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['id'], self.teacher_id)
        self.assertEqual(response_json['name'], 'John Doe')

    def test_002_create_student(self):
        """
        Teste que cria um aluno. O aluno é criado no método setUp, então
        este teste apenas verifica se o aluno foi realmente criado.
        """
        response = requests.get(f'{self.BASE_URL}/students/{self.student_id}')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['id'], self.student_id)
        self.assertEqual(response_json['name'], 'Jane Smith')

if __name__ == '__main__':
    unittest.main()
