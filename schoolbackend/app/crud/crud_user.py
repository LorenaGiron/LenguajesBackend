from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash 

# Buscar usuario por email 
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Crear usuario nuevo
def create_user(db: Session, user: UserCreate):
    # 1. Encriptar la contraseña
    hashed_password = get_password_hash(user.password)
    
    db_user = User(
        email=user.email,
        hashed_password=hashed_password, 
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active
    )
    
    # 3. Guardar en BD
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()