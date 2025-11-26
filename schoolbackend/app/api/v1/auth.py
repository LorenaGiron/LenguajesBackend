from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import crud_user
from app.core import security

router = APIRouter()

@router.post("/login/access-token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = crud_user.get_user_by_email(db, email=form_data.username)
    
    # Definición de la excepción genérica (oculta el fallo real)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email o contraseña incorrectos",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 1. Verificar si el usuario existe
    if not user:
        raise credentials_exception

    # 2. Verificar la contraseña (solo si el usuario existe)
    if not security.verify_password(form_data.password, user.hashed_password):
        raise credentials_exception

    # Si todo es correcto...
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}