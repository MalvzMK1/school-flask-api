from src.blueprints import student_ns, course_class_ns, teacher_ns
from config import app
from src.models import db
from flask_restx import Api

with app.app_context():
    db.create_all()  

api = Api(
    title='School API',
    version='1.0',
    description='School management API',
    doc='/api/docs'
)

api.add_namespace(student_ns)
api.add_namespace(teacher_ns)
api.add_namespace(course_class_ns)

api.init_app(app)

if __name__ == '__main__':
    app.run()
