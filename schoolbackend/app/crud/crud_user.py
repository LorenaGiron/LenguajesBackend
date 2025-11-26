from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
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




def get_users(db: Session, skip: int = 0, limit: int = 100, role: str = None):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return query.offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        return None  

    update_data = user_update.model_dump(exclude_unset=True)
    
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
        
    db.delete(db_user)
    db.commit()
    return db_user