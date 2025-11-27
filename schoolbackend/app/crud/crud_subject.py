from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.subject import Subject
from app.models.student import Student
from app.schemas.subject import SubjectCreate,SubjectUpdate

def get_subjects(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Subject)
        .options(joinedload(Subject.students))
        .options(joinedload(Subject.teacher))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_subject(db: Session, subject_id: int):
    return (
        db.query(Subject)
        .options(joinedload(Subject.students))
        .options(joinedload(Subject.teacher))
        .filter(Subject.id == subject_id)
        .first()
    )


def create_subject(db: Session, subject: SubjectCreate):
    db_subject = Subject(
        name=subject.name,
        teacher_id=subject.teacher_id
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def remove_student_from_subject(db: Session, subject_id: int, student_id: int):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    if student not in subject.students:
        raise HTTPException(status_code=400, detail="El alumno no está asignado a esta materia")

    # ELIMINA SIN ROMPER LA SESIÓN
    subject.students.remove(student)
    db.commit()
    db.refresh(subject)

    return subject
def update_subject(db: Session, subject_id: int, subject_update: SubjectUpdate):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    
    if not db_subject:
        return None  

    update_data = subject_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_subject, key, value)

    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def delete_subject(db: Session, subject_id: int):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not db_subject:
        return None
        
    db.delete(db_subject)
    db.commit()
    return db_subject