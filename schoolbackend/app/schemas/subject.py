from pydantic import BaseModel
from typing import Optional, List
from app.schemas.user import UserResponse  # tu schema existente


# -----------------------
# SCHEMAS REDUCIDOS
# -----------------------

class StudentMini(BaseModel):
    id: int
    first_name: str
    last_name: str
    last_name2: Optional[str] = None
    email: str

    class Config:
        from_attributes = True


# -----------------------
# SCHEMAS DE SUBJECT
# -----------------------

class SubjectBase(BaseModel):
    name: str
    teacher_id: int


class SubjectCreate(SubjectBase):
    pass


class SubjectResponse(SubjectBase):
    id: int
    teacher: Optional[UserResponse]
    student_count: int = 0
    students: List[StudentMini] = []

    class Config:
        from_attributes = True


class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    teacher_id: Optional[int] = None

    class Config:
        from_attributes = True


class SubjectStudentAssignment(BaseModel):
    student_ids: List[int]
