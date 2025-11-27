from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.grade import Grade
from app.models.student import Student
from app.api import dependencies
from app.models.user import User
from app.models.subject import Subject

router = APIRouter()

@router.get("/student/{student_id}")
def get_student_report(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
   
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    grades = db.query(Grade).filter(Grade.student_id == student_id).all()

    if not grades:
        average = 0
    else:
     
        total_score = sum([grade.score for grade in grades])
        average = round(total_score / len(grades), 2)

   
    subjects_data = []
    for grade in grades:
        subjects_data.append({
            "subject": grade.subject.name, 
            "score": grade.score
        })

    
    return {
        "student_name": f"{student.first_name} {student.last_name} {student.last_name2}",
        
        "total_average": average,
        "grades": subjects_data
    }




@router.get("/stats/students")
def get_total_students(db: Session = Depends(get_db)):
    total_students = db.query(Student).count()
    return {"total": total_students}

@router.get("/stats/subjects")
def get_total_subjects(db: Session = Depends(get_db)):
    total_subjects = db.query(Subject).count()
    return {"total": total_subjects}

@router.get("/stats/professors")
def get_total_professors(db: Session = Depends(get_db)):
    total_professors = db.query(User).filter(User.role == "profesor").count()
    return {"total": total_professors}