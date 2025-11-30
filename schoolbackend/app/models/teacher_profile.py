from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class TeacherProfile(Base):
    __tablename__ = "teacher_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    photo_url = Column(String(500), nullable=True)
    
    # Relación con User
    user = relationship("User", backref="teacher_profile")

