from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.crud import crud_student
from app.models.user import User

from app.api import dependencies 

router = APIRouter()

# --- RUTAS PROTEGIDAS ---

@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate, 
    db: Session = Depends(get_db),
  
    current_user: User = Depends(dependencies.get_current_user) 
):
    db_student = crud_student.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return crud_student.create_student(db=db, student=student)

@router.get("/", response_model=List[StudentResponse])
def read_students(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
  
    current_user: User = Depends(dependencies.get_current_user) 
):
    
    
    return crud_student.get_students(db, skip=skip, limit=limit)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int, 
    student_update: StudentUpdate, 
    db: Session = Depends(get_db),
 
    current_user: User = Depends(dependencies.get_current_user)
):
    updated_student = crud_student.update_student(db, student_id, student_update)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return updated_student

@router.delete("/{student_id}", response_model=StudentResponse)
def delete_student(
    student_id: int, 
    db: Session = Depends(get_db),
   
    current_user: User = Depends(dependencies.get_current_user)
):
    deleted_student = crud_student.delete_student(db, student_id)
    if not deleted_student:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return deleted_student





@router.post("/{student_id}/enroll/{subject_id}", response_model=StudentResponse)
def enroll_student(
    student_id: int, 
    subject_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
   
    student = crud_student.enroll_student_to_subject(db, student_id, subject_id)
    if not student:
        raise HTTPException(status_code=404, detail="Alumno o Materia no encontrados")
    return student