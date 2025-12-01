from pydantic import BaseModel, EmailStr
from typing import Optional, List


# -----------------------
# SCHEMAS REDUCIDOS
# -----------------------

class SubjectMini(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# -----------------------
# SCHEMAS DE STUDENT
# -----------------------

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    last_name2: Optional[str] = None
    email: EmailStr


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    last_name2: Optional[str] = None
    email: Optional[EmailStr] = None
    enrollment_code: Optional[str] = None

    class Config:
        from_attributes = True


class StudentResponse(StudentBase):
    id: int
    subjects: List[SubjectMini] = []

    class Config:
        from_attributes = True
