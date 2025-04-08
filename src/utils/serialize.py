def serialize_teacher(teacher):
    return {
        "id": teacher.id,
        "name": teacher.name,
        "created_at": teacher.created_at.strftime('%d/%m/%Y')
    }

def serialize_course_class(course_class):
    return {
        "id": course_class.id,
        "teacher": serialize_teacher(course_class.teacher),
        "created_at": course_class.created_at.strftime('%d/%m/%Y')
    }
