from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Grade(Base):  
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, nullable=False)
    
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))

    student = relationship("Student")
    subject = relationship("Subject")