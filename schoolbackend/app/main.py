from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.db.session import engine
from app.db.base import Base

#  Modelos
from app.models.student import Student
from app.models.user import User
from app.models.subject import Subject
from app.models.grade import Grade

# Rutas
from app.api.v1 import students
from app.api.v1 import users
from app.api.v1 import auth
from app.api.v1 import subjects
from app.api.v1 import grades
from app.api.v1 import reports 

# Crear tablas en BD
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Mini-SICE API")

# --- CONFIGURACIÓN CORS------------------------------------------------------
origins = [
    "http://localhost:5173", # Puerto común de Vite/React
    "http://localhost:3000", # Puerto común de Create-React-App
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)
# ---------------------------------------------------------------------------------------

# Rutas-----------------------------------------------------------------------------------
app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(subjects.router, prefix="/api/v1/subjects", tags=["Subjects"])
app.include_router(grades.router, prefix="/api/v1/grades", tags=["Grades"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"]) # <--- CONECTADO

@app.get("/")
def root():
    return {"message": "El sistema está funcionando 0o0"}