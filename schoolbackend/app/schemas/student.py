from pydantic import BaseModel, EmailStr
from typing import Optional

# 1. Base común (datos compartidos al crear y leer)
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    last_name2: str | None = None
    email: EmailStr  # Valida automáticamente que sea un email real
    

# 2. Schema para CREAR (Lo que el usuario envía)
# Hereda los campos de arriba
class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    enrollment_code: Optional[str] = None
# 3. Schema para RESPONDER (Lo que la API devuelve)
class StudentResponse(StudentBase):
    id: int  # La API devuelve el ID, pero el usuario NO lo envía al crear

    # Esto es vital: permite que Pydantic lea datos de SQLAlchemy
    class Config:
        from_attributes = True