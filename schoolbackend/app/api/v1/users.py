from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.teacher_profile import TeacherProfileResponse, TeacherProfileUpdate
from app.crud import crud_user, crud_teacher_profile
from app.api import dependencies
from app.models.user import User
from typing import List, Optional
from pathlib import Path
import uuid

router = APIRouter()

# Directorio para guardar las fotos de perfil
UPLOAD_DIR = Path("uploads/profiles")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

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


# ---------------------------------------------------------
# ENDPOINTS PARA PERFIL DEL PROFESOR
# ---------------------------------------------------------

@router.get("/profile", response_model=TeacherProfileResponse)
def get_teacher_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Obtiene el perfil del profesor autenticado (descripción y foto)
    """
    if current_user.role != "profesor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este endpoint es solo para profesores"
        )
    
    profile = crud_teacher_profile.get_teacher_profile_by_user_id(db, current_user.id)
    
    # Si no existe perfil, retornar uno vacío
    if not profile:
        return TeacherProfileResponse(
            id=0,
            user_id=current_user.id,
            description=None,
            photo_url=None
        )
    
    return profile


@router.put("/profile", response_model=TeacherProfileResponse)
async def update_teacher_profile(
    description: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Actualiza el perfil del profesor (descripción y/o foto)
    Guarda en la tabla teacher_profiles separada
    """
    if current_user.role != "profesor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este endpoint es solo para profesores"
        )
    
    update_data = {}
    
    # Actualizar descripción si se proporciona
    if description is not None:
        # Validar longitud máxima (500 caracteres como en el frontend)
        if len(description) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La descripción no puede exceder 500 caracteres"
            )
        update_data["description"] = description
    
    # Manejar subida de foto
    if photo is not None:
        # Validar que sea una imagen
        if not photo.content_type or not photo.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo debe ser una imagen"
            )
        
        # Validar tamaño máximo (5MB)
        contents = await photo.read()
        file_size = len(contents)
        if file_size > 5 * 1024 * 1024:  # 5MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La imagen no puede exceder 5MB"
            )
        
        # Generar nombre único para el archivo
        file_extension = Path(photo.filename).suffix if photo.filename else ".jpg"
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Guardar el archivo
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        
        # Si había una foto anterior, eliminarla
        existing_profile = crud_teacher_profile.get_teacher_profile_by_user_id(db, current_user.id)
        if existing_profile and existing_profile.photo_url:
            old_file_path = UPLOAD_DIR / Path(existing_profile.photo_url).name
            if old_file_path.exists():
                old_file_path.unlink()
        
        # Guardar la URL relativa en la base de datos
        # La URL será accesible desde /uploads/profiles/{unique_filename}
        update_data["photo_url"] = f"/uploads/profiles/{unique_filename}"
    
    # Actualizar o crear el perfil en la tabla teacher_profiles
    profile_update = TeacherProfileUpdate(**update_data)
    updated_profile = crud_teacher_profile.update_teacher_profile(
        db, 
        current_user.id, 
        profile_update
    )
    
    return updated_profile