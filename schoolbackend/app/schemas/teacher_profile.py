from pydantic import BaseModel
from typing import Optional

class TeacherProfileBase(BaseModel):
    description: Optional[str] = None
    photo_url: Optional[str] = None

class TeacherProfileCreate(TeacherProfileBase):
    pass

class TeacherProfileUpdate(TeacherProfileBase):
    pass

class TeacherProfileResponse(TeacherProfileBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

