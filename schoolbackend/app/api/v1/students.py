from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.db.session import get_db
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.crud import crud_student
from app.models.user import User
from app.models.student import Student
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

# NUEVO ENDPOINT DE BÚSQUEDA
@router.get("/search-my-students", response_model=List[StudentResponse])
def search_my_students(
    q: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Busca solo los alumnos inscritos en las materias que imparte el profesor actual.
    """
    from app.models.subject import Subject
    
    # Obtener las materias del profesor
    teacher_subjects = db.query(Subject).filter(
        Subject.teacher_id == current_user.id
    ).all()
    
    # Obtener IDs de estudiantes de esas materias
    student_ids = set()
    for subject in teacher_subjects:
        for student in subject.students:
            student_ids.add(student.id)
    
    if not student_ids:
        return []  # El profesor no tiene alumnos
    
    # Buscar entre esos estudiantes
    search_term = f"%{q.lower()}%"
    students = db.query(Student).filter(
        Student.id.in_(student_ids),
        or_(
            func.lower(Student.email).like(search_term),
            func.lower(Student.first_name).like(search_term),
            func.lower(Student.last_name).like(search_term),
            func.lower(Student.last_name2).like(search_term)
        )
    ).limit(10).all()
    
    return students

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




@router.get("/search", response_model=List[StudentResponse])
def search_students_suggestions(q: str, db: Session = Depends(get_db)):
    # Lógica similar a la de reports, pero devolviendo solo el estudiante
    search_term = f"%{q.lower()}%"
    students = db.query(Student).filter(
        or_(
            func.lower(Student.email).like(search_term),
            func.lower(Student.first_name).like(search_term),
            func.lower(Student.last_name).like(search_term)
        )
    ).limit(10).all()
    return students
