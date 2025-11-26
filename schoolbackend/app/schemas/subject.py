
from pydantic import BaseModel
from typing import Optional, List
from app.schemas.user import UserResponse 

class SubjectBase(BaseModel):
    name: str
    teacher_id: int 

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int
    teacher: UserResponse 

    class Config:
        from_attributes = True

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    teacher_id: Optional[int] = None
    
    class Config:
        from_attributes = True