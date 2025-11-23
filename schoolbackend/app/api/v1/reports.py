from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.grade import Grade
from app.models.student import Student
from app.api import dependencies
from app.models.user import User

router = APIRouter()

@router.get("/student/{student_id}")
def get_student_report(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    # 1. Buscamos al alumno
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    # 2. Buscamos todas sus calificaciones
    # Gracias a las relaciones de SQLAlchemy, podemos acceder a 'grade.subject.name'
    grades = db.query(Grade).filter(Grade.student_id == student_id).all()

    # 3. Calculamos el PROMEDIO
    if not grades:
        average = 0
    else:
        # Sumamos todos los scores y dividimos entre la cantidad
        total_score = sum([grade.score for grade in grades])
        average = round(total_score / len(grades), 2)

    # 4. Preparamos una lista bonita con los nombres de las materias
    subjects_data = []
    for grade in grades:
        subjects_data.append({
            "subject": grade.subject.name, 
            "score": grade.score
        })

    # 5. Estructuramos la respuesta final (JSON)
    return {
        "student_name": f"{student.first_name} {student.last_name} {student.last_name2}",
        
        "total_average": average,
        "grades": subjects_data
    }