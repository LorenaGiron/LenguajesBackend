from sqlalchemy import Column, Integer, String, Table, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship
from app.models.grade import Grade



student_subject_association = Table(
    'student_subject',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False) 
    last_name = Column(String(100), nullable=False)
    last_name2 = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, index=True)
    grades = relationship(
        "Grade", 
        back_populates="student", 
        cascade="all, delete-orphan" 
    )
    subjects = relationship(
        "Subject", 
        secondary=student_subject_association, 
        back_populates="students"
    )