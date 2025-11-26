from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.student import student_subject_association



class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    
    teacher = relationship("User")

  
    students = relationship(
        "Student", 
        secondary=student_subject_association, 
        back_populates="subjects"
    )