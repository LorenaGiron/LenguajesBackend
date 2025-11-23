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
    # 1. Buscamos al usuario por email
    # Nota: OAuth2PasswordRequestForm usa 'username' aunque nosotros usemos email
    user = crud_user.get_user_by_email(db, email=form_data.username)

    # 2. Verificamos si el usuario existe y si la contraseña coincide
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Si todo es correcto, generamos el Token JWT
    access_token = security.create_access_token(data={"sub": user.email})

    # 4. Devolvemos el token y el tipo
    return {"access_token": access_token, "token_type": "bearer"}