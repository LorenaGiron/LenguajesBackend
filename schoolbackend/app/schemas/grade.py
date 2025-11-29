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
    
class GradeUpdate(BaseModel):
    score: float
    
    class Config:
        from_attributes = True