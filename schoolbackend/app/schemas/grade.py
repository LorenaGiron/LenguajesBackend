from pydantic import BaseModel
from typing import Optional

# Base común
class GradeBase(BaseModel):
    student_id: int
    subject_id: int
    score: float

class GradeCreate(GradeBase):
    pass

class GradeResponse(GradeBase):
    id: int
    
    # Esto es útil para mostrar nombres en lugar de solo IDs en el frontend
    # (Lo veremos más adelante si lo necesitas)
    
    class Config:
        from_attributes = True