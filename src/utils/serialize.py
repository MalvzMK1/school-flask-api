def serialize_teacher(teacher):
    try:
        return {
            "id": teacher.id,
            "name": teacher.name,
            "created_at": teacher.created_at.strftime('%d/%m/%Y') if teacher.created_at else None
        }
    except Exception as e:
        print(f"Erro ao serializar o professor: {str(e)}")
        return {"error": "Erro ao serializar o professor"}

def serialize_course_class(course_class):
    try:
        return {
            "id": course_class.id,
            "teacher": serialize_teacher(course_class.teacher) if course_class.teacher else None,
            "created_at": course_class.created_at.strftime('%d/%m/%Y') if course_class.created_at else None
        }
    except Exception as e:
        print(f"Erro ao serializar a turma: {str(e)}")
        return {"error": "Erro ao serializar a turma"}
