from src.blueprints import student_bp, course_class_bp, teacher_bp
from config import app
from src.models import db

with app.app_context():
    db.create_all()  

app.register_blueprint(student_bp)
app.register_blueprint(course_class_bp)
app.register_blueprint(teacher_bp)

if __name__ == '__main__':
    app.run()
