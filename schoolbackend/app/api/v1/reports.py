from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.session import get_db
from app.models.grade import Grade
from app.models.student import Student
from app.api import dependencies
from app.models.user import User
from app.models.subject import Subject
from sqlalchemy import func, select, or_

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



@router.get("/subject-grades/{subject_id}")
def get_subject_enrollment_report(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    grades = (
        db.query(Grade)
        .filter(Grade.subject_id == subject_id)
        .options(joinedload(Grade.student)) 
        .all()
    )

    if not grades:
        return {
            "subject_name": subject.name,
            "students_with_grades": [],
        }

    students_with_grades = []
    for grade in grades:
        student = grade.student 
        
        students_with_grades.append({
            "student_id": student.id,
            "student_name": f"{student.first_name} {student.last_name} {student.last_name2 or ''}".strip(),
            "score": grade.score,
            "grade_id": grade.id,
        })

    return {
        "subject_name": subject.name,
        "students_with_grades": students_with_grades,
    }

#función para buscar el reporte de un estudiante por su nombre, apellido o email
@router.get("/student-grades-search/{identifier}")
def get_student_grades_report_by_identifier(
    identifier: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    
    search_term = f"%{identifier.lower()}%"
    
    student = db.query(Student).filter(
        or_(
            func.lower(Student.email) == identifier.lower(),
            func.lower(Student.first_name).like(search_term),
            func.lower(Student.last_name).like(search_term),
            func.lower(Student.last_name2).like(search_term)
        )
    ).first() 
    
    if not student:
        raise HTTPException(status_code=404, detail=f"Alumno no encontrado con el identificador: {identifier}")

    student_id = student.id
    
    grades = (
        db.query(Grade)
        .filter(Grade.student_id == student_id)
        .options(joinedload(Grade.subject))
        .all()
    )

    subjects_data = []
    for grade in grades:
        subject = grade.subject 
        subjects_data.append({
            "subject_name": subject.name,
            "score": grade.score,
        })
    
    if not grades:
        average = 0
    else:
        total_score = sum([grade.score for grade in grades])
        average = round(total_score / len(grades), 2)
        
    
    return {
        "student_id": student.id,
        "student_name": f"{student.first_name} {student.last_name} {student.last_name2 or ''}".strip(),
        "total_average": average,
        "grades": subjects_data,
    }
