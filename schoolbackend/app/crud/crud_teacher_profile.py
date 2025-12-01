from sqlalchemy.orm import Session
from app.models.teacher_profile import TeacherProfile
from app.schemas.teacher_profile import TeacherProfileCreate, TeacherProfileUpdate

def get_teacher_profile_by_user_id(db: Session, user_id: int):
    """Obtiene el perfil del profesor por user_id"""
    return db.query(TeacherProfile).filter(TeacherProfile.user_id == user_id).first()

def create_teacher_profile(db: Session, user_id: int, profile: TeacherProfileCreate):
    """Crea un nuevo perfil de profesor"""
    db_profile = TeacherProfile(
        user_id=user_id,
        description=profile.description,
        photo_url=profile.photo_url
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_teacher_profile(db: Session, user_id: int, profile_update: TeacherProfileUpdate):
    """Actualiza el perfil del profesor"""
    db_profile = db.query(TeacherProfile).filter(TeacherProfile.user_id == user_id).first()
    
    if not db_profile:
        # Si no existe, crear uno nuevo
        profile_create = TeacherProfileCreate(
            description=profile_update.description,
            photo_url=profile_update.photo_url
        )
        return create_teacher_profile(db, user_id, profile_create)
    
    # Actualizar campos que se proporcionaron
    update_data = profile_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_profile, key, value)
    
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

