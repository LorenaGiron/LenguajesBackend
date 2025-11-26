from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.grade import GradeCreate, GradeResponse
from app.crud import crud_grade, crud_student, crud_subject # Importamos todos los CRUDs
from app.models.user import User
from app.api import dependencies

router = APIRouter()

@router.post("/", response_model=GradeResponse)
def create_grade(
    grade: GradeCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    # 1. Validar que el Alumno exista
    student = crud_student.get_student(db, student_id=grade.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="El alumno no existe")

    # 2. Validar que la Materia exista
    # Nota: Necesitamos una función get_subject en crud_subject. 
    # (Si no la tienes, te la paso abajo para que la agregues)
    subject = crud_subject.get_subject(db, subject_id=grade.subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="La materia no existe")

    return crud_grade.create_grade(db=db, grade=grade)

@router.get("/student/{student_id}", response_model=List[GradeResponse])
def read_student_grades(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    return crud_grade.get_grades_by_student(db, student_id=student_id)