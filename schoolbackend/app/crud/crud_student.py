from sqlalchemy.orm import Session,joinedload
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.models.subject import Subject
from typing import List

# Función para obtener un alumno por ID
def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

# Función para obtener un alumno por Email (útil para validaciones)
def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()

# Función para listar alumnos (con paginación: skip y limit)
def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()

# Función para CREAR un alumno nuevo
def create_student(db: Session, student: StudentCreate):
    # 1. Convertimos el Schema (datos JSON) a Modelo (Tabla SQL)
    db_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        last_name2=student.last_name2,
        email=student.email,
        
    )
    
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Función para ACTUALIZAR
def update_student(db: Session, student_id: int, student_update: StudentUpdate):
    # 1. Buscamos al alumno existente
    db_student = db.query(Student).filter(Student.id == student_id).first()
    
    if not db_student:
        return None  

    update_data = student_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        return None
        
    db.delete(db_student)
    db.commit()
    return db_student



def enroll_student_to_subject(db: Session, student_id: int, subject_id: int):

    student = db.query(Student).filter(Student.id == student_id).first()
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not student or not subject:
        return None 
    student.subjects.append(subject) 
    db.commit()
    db.refresh(student)
    return student


def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
   
    return db.query(Student)\
             .options(joinedload(Student.subjects))\
             .offset(skip)\
             .limit(limit)\
             .all()

