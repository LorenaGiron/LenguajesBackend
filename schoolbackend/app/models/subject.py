from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False) # Ej: "Matemáticas I"
    # RELACIÓN: Una materia pertenece a un Usuario (Profesor)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    # Relación con el modelo User (Profesor)
    teacher = relationship("User")