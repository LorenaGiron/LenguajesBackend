from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.subject import SubjectCreate, SubjectResponse, SubjectUpdate
from app.crud import crud_subject, crud_user 
from app.models.user import User
from app.api import dependencies
from sqlalchemy.orm import Session, joinedload

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





def update_subject(db: Session, subject_id: int, subject_update: SubjectUpdate):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    
    if not db_subject:
        return None

    update_data = subject_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_subject, key, value)

    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def delete_subject(db: Session, subject_id: int):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    
    if not db_subject:
        return None
        
    db.delete(db_subject)
    db.commit()
    return db_subject


@router.get("/", response_model=List[SubjectResponse])
def read_subjects(
   
    db: Session = Depends(dependencies.get_db),
  
):
    
    query = db.query(Subject).options(joinedload(Subject.teacher))
    
    return query.offset(skip).limit(limit).all()