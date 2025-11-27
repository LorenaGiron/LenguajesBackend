from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False) # Contraseña encriptada
    full_name = Column(String(100))
    role = Column(String(50), default="profesor") # Roles: 'admin' o 'profesor'
    is_active = Column(Boolean, default=True)
    subjects = relationship("Subject", back_populates="teacher")
