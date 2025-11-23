from sqlalchemy.orm import Session
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate

def get_subjects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Subject).offset(skip).limit(limit).all()

def create_subject(db: Session, subject: SubjectCreate):
    db_subject = Subject(
        name=subject.name,
        teacher_id=subject.teacher_id
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject



def get_subject(db: Session, subject_id: int):
    return db.query(Subject).filter(Subject.id == subject_id).first()