from pydantic import BaseModel, EmailStr
from typing import Optional,List
# Base común
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "profesor" # Por defecto
    is_active: bool = True
# Para crear  usario se ´pide nuestra contraseña
class UserCreate(UserBase):
    password: str
class UserResponse(UserBase):# Para respuestas (sin contraseña)

    id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True


