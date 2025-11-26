from sqlalchemy.orm import Session
from app.models.grade import Grade
from app.schemas.grade import GradeCreate

def create_grade(db: Session, grade: GradeCreate):
    db_grade = Grade(
        student_id=grade.student_id,
        subject_id=grade.subject_id,
        score=grade.score
    )
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

def get_grades_by_student(db: Session, student_id: int):
    return db.query(Grade).filter(Grade.student_id == student_id).all()

def get_all_grades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Grade).offset(skip).limit(limit).all()