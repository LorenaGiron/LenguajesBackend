from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import func, select,or_
from app.db.session import get_db
from app.schemas.subject import SubjectCreate, SubjectResponse, SubjectUpdate, SubjectStudentAssignment
from app.crud import crud_subject, crud_user
from app.models.user import User
from app.api import dependencies
from app.models.subject import Subject, student_subject_association
from app.models.student import Student
from app.models.grade import Grade
from app.schemas.student import StudentResponse

router = APIRouter()

# ---------------------------------------------------------
# CREAR MATERIA
# ---------------------------------------------------------
@router.post("/", response_model=SubjectResponse)
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    teacher = crud_user.get_user(db, user_id=subject.teacher_id)

    if not teacher:
        raise HTTPException(status_code=404, detail="El ID del profesor no existe")

    if teacher.role != "profesor":
        raise HTTPException(
            status_code=400,
            detail=f"El usuario '{teacher.full_name}' es '{teacher.role}', no es profesor."
        )

    return crud_subject.create_subject(db=db, subject=subject)


# ---------------------------------------------------------
# OBTENER TODAS LAS MATERIAS
# ---------------------------------------------------------
@router.get("/", response_model=List[SubjectResponse])
def read_subjects(db: Session = Depends(get_db)):

    student_count_subquery = select(
        student_subject_association.c.subject_id,
        func.count(student_subject_association.c.student_id).label("student_count")
    ).group_by(student_subject_association.c.subject_id).subquery()

    results = (
        db.query(Subject, student_count_subquery.c.student_count)
        .outerjoin(student_count_subquery, Subject.id == student_count_subquery.c.subject_id)
        .options(joinedload(Subject.teacher))
        .options(selectinload(Subject.students))
        .all()
    )

    



    response_data = []
    for subject, count in results:
        subject.student_count = count or 0
        response_data.append(
        SubjectResponse.model_validate(subject, from_attributes=True)
    )

    return response_data


# ---------------------------------------------------------
# REEMPLAZAR LISTA COMPLETA DE ESTUDIANTES
# ---------------------------------------------------------
@router.put(
    "/{subject_id}/students/",
    response_model=SubjectResponse,
    status_code=status.HTTP_200_OK
)
def update_subject_students(
    subject_id: int,
    assignment: SubjectStudentAssignment,
    db: Session = Depends(get_db)
):

    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    if assignment.student_ids:
        students_to_assign = db.query(Student).filter(Student.id.in_(assignment.student_ids)).all()
    else:
        students_to_assign = []

    subject.students = students_to_assign
    db.commit()

    subject = (
        db.query(Subject)
        .filter(Subject.id == subject_id)
        .options(joinedload(Subject.students))
        .first()
    )

    return subject


# ---------------------------------------------------------
# ELIMINAR UN ALUMNO DE UNA MATERIA (RUTA CORRECTA)
# ---------------------------------------------------------
@router.delete("/{subject_id}/students/{student_id}", response_model=SubjectResponse)
def remove_student(subject_id: int, student_id: int, db: Session = Depends(get_db)):
    subject = crud_subject.remove_student_from_subject(db, subject_id, student_id)
    return subject





@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int, 
    subject_update: SubjectUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    update_data = subject_update.model_dump(exclude_unset=True)
    if "teacher_id" in update_data:
        teacher = crud_user.get_user(db, user_id=update_data["teacher_id"])
        if not teacher:
            raise HTTPException(status_code=404, detail="El ID del profesor no existe")
        if teacher.role != "profesor":
            raise HTTPException(
                status_code=400,
                detail=f"El usuario '{teacher.full_name}' es '{teacher.role}', no es profesor."
            )

    updated_subject = crud_subject.update_subject(db, subject_id, subject_update)
    if not updated_subject:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return updated_subject

@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(
    subject_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    deleted_subject = crud_subject.delete_subject(db, subject_id)
    if not deleted_subject:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{subject_id}/students", response_model=List[StudentResponse])
def read_subject_students(
    subject_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    
    subject = crud_subject.get_subject(db, subject_id=subject_id)

    if not subject:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
        
    if current_user.role == "profesor" and subject.teacher_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="No tienes permiso para ver los alumnos de esta materia."
        )

   
    return subject.students



@router.get("/teacher-load/", response_model=List[SubjectResponse])
def read_teacher_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user),
    teacher_id: Optional[int] = None 
):
    
    student_count_subquery = select(
        student_subject_association.c.subject_id,
        func.count(student_subject_association.c.student_id).label("student_count")
    ).group_by(student_subject_association.c.subject_id).subquery()

    query = (
        db.query(Subject, student_count_subquery.c.student_count)
        .outerjoin(student_count_subquery, Subject.id == student_count_subquery.c.subject_id)
        .options(joinedload(Subject.teacher))
        .options(selectinload(Subject.students))
    )
    
    if current_user.role == "profesor":
        filter_id = current_user.id
    elif teacher_id is not None:
        filter_id = teacher_id
    else:
        filter_id = None
    
    if filter_id is not None:
        query = query.filter(Subject.teacher_id == filter_id)
    

    results = query.all()
    
    response_data = []
    for subject, count in results:
        subject.student_count = count or 0
        response_data.append(
        SubjectResponse.model_validate(subject, from_attributes=True)
    )

    return response_data