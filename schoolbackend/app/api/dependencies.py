from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import crud_user
from app.core import security
from app.models.user import User

# 1. Configuración del Guardia
# Le decimos: "Si alguien no trae token, mándalo a esta URL para que se loguee"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/access-token")

# 2. La función del Guardia (Validar el Token)
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme) # <--- Aquí el guardia exige el token
):
    # Preparamos el mensaje de error "401 No Autorizado"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 3. Decodificamos el token con la clave secreta
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception # Token falso o expirado
    
    # 4. Buscamos si el usuario sigue existiendo en la BD
    user = crud_user.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
        
    # 5. ¡Pase usted! Devolvemos al usuario validado
    return user