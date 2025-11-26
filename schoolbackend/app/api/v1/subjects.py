from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.subject import SubjectCreate, SubjectResponse
from app.crud import crud_subject, crud_user # <--- Importamos ambos CRUDs
from app.models.user import User
from app.api import dependencies

router = APIRouter()

@router.post("/", response_model=SubjectResponse)
def create_subject(
    subject: SubjectCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user) # Solo usuarios logueados
):
    # --- INICIO DE VALIDACIÓN ---
    
  
    teacher = crud_user.get_user(db, user_id=subject.teacher_id)
    
 
    if not teacher:
        raise HTTPException(status_code=404, detail="El ID del profesor no existe")
   
    if teacher.role != "profesor":
        raise HTTPException(
            status_code=400, 
            detail=f"El usuario '{teacher.full_name}' es '{teacher.role}', no es un Profesor."
        )
    
    # --- FIN DE VALIDACIÓN ---

    return crud_subject.create_subject(db=db, subject=subject)

@router.get("/", response_model=List[SubjectResponse])
def read_subjects(
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    return crud_subject.get_subjects(db, skip=skip, limit=limit)