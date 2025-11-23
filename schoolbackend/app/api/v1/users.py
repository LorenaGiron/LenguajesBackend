from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud import crud_user

router = APIRouter()

# Endpoint para REGISTRAR un nuevo usuario
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificamos si el email ya existe para no duplicar
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # 2. Creamos el usuario (la contraseña se encripta dentro del CRUD)
    return crud_user.create_user(db=db, user=user)