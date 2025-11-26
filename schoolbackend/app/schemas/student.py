from pydantic import BaseModel, EmailStr
from typing import Optional,List
from app.schemas.subject import SubjectResponse



class StudentBase(BaseModel):
    first_name: str
    last_name: str
    last_name2: str | None = None
    email: EmailStr  
    
class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    last_name2: Optional[str] = None
    email: Optional[EmailStr] = None
    enrollment_code: Optional[str] = None

class StudentResponse(StudentBase):
    id: int  
    subjects: List[SubjectResponse] = []
  
    class Config:
        from_attributes = True