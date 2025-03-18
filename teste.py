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

    # Teste POST para cadastrar uma turma
    def test_003_create_course_class(self):
        response_course_class = requests.post(
            f'{self.BASE_URL}/course-classes',
            json={'teacher_id': self.teacher_id}  
        )

        self.assertEqual(response_course_class.status_code, 201)

        response_json = response_course_class.json()
        self.assertIn('id', response_json)  # Verifica se a turma foi criada
        self.assertEqual(response_json['message'], 'Course class created successfully')

    # Teste GET para buscar todos os professores
    def test_004_get_all_teachers(self):
        response = requests.get(f'{self.BASE_URL}/teachers')

        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn('teachers', response_json)
        self.assertGreater(len(response_json['teachers']), 0)

    # Teste GET para buscar um professor específico
    def test_005_get_teacher_by_id(self):
        response = requests.get(f'{self.BASE_URL}/teachers/{self.teacher_id}')
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['id'], self.teacher_id)
        self.assertEqual(response_json['name'], 'John Doe')
    
     # Teste GET para buscar todos os alunos
    def test_006_get_all_students(self):
        response = requests.get(f'{self.BASE_URL}/students')

        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn('students', response_json)
        self.assertGreater(len(response_json['students']), 0)

    # Teste GET para buscar um aluno específico
    def test_007_get_student_by_id(self):
        response = requests.get(f'{self.BASE_URL}/students/{self.student_id}')
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['id'], self.student_id)
        self.assertEqual(response_json['name'], 'Jane Smith')
        
    # Teste GET para buscar todos os cursos
    def test_008_get_all_course_classes(self):
        response = requests.get(f'{self.BASE_URL}/course-classes')

        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn('course_classes', response_json)
        self.assertGreater(len(response_json['course_classes']), 0) 

    # Teste GET para buscar uma turma específica
    def test_009_get_course_class_by_id(self):
        """
        Teste GET para buscar uma turma específica.
        """
        response = requests.get(f'{self.BASE_URL}/course-classes/{self.course_class_id}')
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['id'], self.course_class_id)

     # ============= PUTS ====================
    def test_010_update_teacher(self):
        updated_data = {
            'name': 'John Updated',
            'birthdate': '1985-07-10'
        }
        
        response = requests.put(
            f'{self.BASE_URL}/teachers/{self.teacher_id}', 
            json=updated_data
        )

        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['message'], 'Teacher updated successfully')

        # Verifique se os dados foram realmente atualizados
        response_check = requests.get(f'{self.BASE_URL}/teachers/{self.teacher_id}')
        self.assertEqual(response_check.status_code, 200)

        response_check_json = response_check.json()
        self.assertEqual(response_check_json['id'], self.teacher_id)
        self.assertEqual(response_check_json['name'], updated_data['name'])
        
    # Teste PUT para atualizar os dados de um aluno específico
    def test_011_update_student(self):
        updated_data = {
            'name': 'Jane Updated',
            'birthdate': '2000-08-15'
        }
        
        response = requests.put(
            f'{self.BASE_URL}/students/{self.student_id}', 
            json=updated_data
        )

        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['message'], 'Student updated successfully')

        # Verifique se os dados foram realmente atualizados
        response_check = requests.get(f'{self.BASE_URL}/students/{self.student_id}')
        self.assertEqual(response_check.status_code, 200)

        response_check_json = response_check.json()
        self.assertEqual(response_check_json['id'], self.student_id)
        self.assertEqual(response_check_json['name'], updated_data['name'])
        
    # DELETE para excluir um professor
    def test_010_delete_teacher(self):
        response = requests.delete(f'{self.BASE_URL}/teachers/{self.teacher_id}')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['message'], 'Teacher deleted successfully')

        # Verifica se o professor foi realmente deletado
        response_check = requests.get(f'{self.BASE_URL}/teachers/{self.teacher_id}')
        self.assertEqual(response_check.status_code, 404)
        
    # DELETE para excluir um aluno
    def test_013_delete_student(self):
        response = requests.delete(f'{self.BASE_URL}/students/{self.student_id}')
        self.assertEqual(response.status_code, 204)  

        # Verifica se o aluno foi realmente deletado
        response_check = requests.get(f'{self.BASE_URL}/students/{self.student_id}')
        self.assertEqual(response_check.status_code, 404)    
if __name__ == '__main__':
    unittest.main()
