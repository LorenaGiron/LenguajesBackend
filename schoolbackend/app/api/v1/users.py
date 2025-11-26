from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.crud import crud_user
from app.api import dependencies
from app.models.user import User
from typing import List, Optional

router = APIRouter()

# Endpoint para REGISTRAR un nuevo usuario
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    #  Verificamos si el email ya existe para no duplicar
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Creamos el usuario (la contraseña se encripta dentro del CRUD)
    return crud_user.create_user(db=db, user=user)


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(dependencies.get_current_user)):
   
    return current_user   



@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    # Permite filtrar por rol (e.g., /api/v1/users/?role=profesor)
    role: Optional[str] = None, 
    skip: int = 0, 
    limit: int = 100,
    current_user: User = Depends(dependencies.get_current_user)
):
    return crud_user.get_users(db, skip=skip, limit=limit, role=role)



@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    updated_user = crud_user.update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user_route(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    deleted_user = crud_user.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return deleted_user