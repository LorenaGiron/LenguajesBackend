from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.teacher_profile import TeacherProfileResponse, TeacherProfileUpdate, TeacherProfileCreate
from app.crud import crud_user, crud_teacher_profile
from app.api import dependencies
from app.models.user import User
from typing import List, Optional
from pathlib import Path
import uuid
import io
from PIL import Image

router = APIRouter()

# Directorio para guardar las fotos de perfil
UPLOAD_DIR = Path("app/uploads/profiles")
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
            description="",
            photo_url=""
        )
    
    return profile

@router.put("/profile", response_model=TeacherProfileResponse)
async def update_teacher_profile(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Actualiza el perfil del profesor (descripción y/o foto)
    """
    if current_user.role != "profesor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este endpoint es solo para profesores"
        )

    try:
        # Parsear el formulario multipart manualmente
        form = await request.form()
        update_data = {}

        # Obtener descripción si existe
        description = form.get("description")
        if description:
            description = str(description).strip()
            if description:
                if len(description) > 500:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="La descripción no puede exceder 500 caracteres"
                    )
                update_data["description"] = description

        # Obtener foto si existe
        photo = form.get("photo")
        if photo and isinstance(photo, UploadFile):
            try:
                # Validar tipo de contenido
                if not photo.content_type or not photo.content_type.startswith("image/"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El archivo debe ser una imagen válida"
                    )

                # Leer el contenido de forma segura
                contents = await photo.read()
                
                if not contents:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El archivo está vacío"
                    )

                # Validar tamaño
                if len(contents) > 5 * 1024 * 1024:  # 5MB
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="La imagen no puede exceder 5MB"
                    )

                # Validar que sea una imagen real usando Pillow
                try:
                    image = Image.open(io.BytesIO(contents))
                    image.verify()  # Verifica que la imagen es válida
                except Exception:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El archivo no es una imagen válida"
                    )

                # Guardar la imagen
                extension = Path(photo.filename).suffix.lower() if photo.filename else ".jpg"
                # Asegurar que la extensión sea válida
                valid_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
                if extension not in valid_extensions:
                    extension = ".jpg"
                
                filename = f"{uuid.uuid4()}{extension}"
                filepath = UPLOAD_DIR / filename

                with open(filepath, "wb") as f:
                    f.write(contents)

                # Eliminar foto anterior si existe
                existing_profile = crud_teacher_profile.get_teacher_profile_by_user_id(db, current_user.id)
                if existing_profile and existing_profile.photo_url:
                    try:
                        old_path = UPLOAD_DIR / Path(existing_profile.photo_url).name
                        if old_path.exists():
                            old_path.unlink()
                    except Exception:
                        pass  # Ignorar errores al eliminar archivo anterior

                update_data["photo_url"] = f"/uploads/profiles/{filename}"

            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error al procesar la imagen"
                )

        # Si no hay datos para actualizar, retornar el perfil actual
        if not update_data:
            profile = crud_teacher_profile.get_teacher_profile_by_user_id(db, current_user.id)
            if not profile:
                # Crear un perfil vacío si no existe
                profile = crud_teacher_profile.create_teacher_profile(
                    db, 
                    current_user.id, 
                    TeacherProfileCreate(description="", photo_url="")
                )
            return profile

        # Actualizar perfil
        profile_update = TeacherProfileUpdate(**update_data)
        updated_profile = crud_teacher_profile.update_teacher_profile(db, current_user.id, profile_update)
        return updated_profile

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en update_teacher_profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar la solicitud"
        )