import random
from app.db.session import SessionLocal
from app.models.user import User
from app.models.student import Student
from app.models.subject import Subject
from app.models.grade import Grade
from app.core import security

db = SessionLocal()

# Listas de datos
professor_names = [
    "Ana López", "Carlos Pérez", "Marta Sánchez",
    "Luis Hernández", "Elena Torres", "Jorge Ramírez"
]

admin_names = [
    "Admin One", "Admin Two",
    "Super Admin"
]

student_names = [
    ("Juan", "Martínez", "Gómez"),
    ("Lucía", "Rodríguez", "Hernández"),
    ("Pedro", "Gómez", "López"),
    ("María", "Vega", "Santos"),
    ("Sofía", "Ramírez", "Pérez"),
    ("Diego", "Morales", "Castro"),
    ("Camila", "Díaz", "Flores"),
    ("Valentina", "Soto", "Rojas")
]

subjects_list = [
    "Matemáticas", "Historia", "Física", "Química", "Literatura",
    "Biología", "Geografía", "Arte", "Educación Física"
]

# -----------------------------
# Crear usuarios
# -----------------------------
users = []

for name in professor_names:
    full_name = name
    email = name.lower().replace(" ", ".") + "@school.com"
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        print(f"⚠️ Usuario {email} ya existe, se omite.")
        users.append(existing_user)
        continue
    password = security.get_password_hash("123456")
    user = User(full_name=full_name, email=email, hashed_password=password, role="profesor")
    db.add(user)
    db.commit()
    db.refresh(user)
    users.append(user)

for name in admin_names:
    full_name = name
    email = name.lower().replace(" ", ".") + "@school.com"
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        print(f"⚠️ Usuario {email} ya existe, se omite.")
        users.append(existing_user)
        continue
    password = security.get_password_hash("admin123")
    user = User(full_name=full_name, email=email, hashed_password=password, role="admin")
    db.add(user)
    db.commit()
    db.refresh(user)
    users.append(user)

# -----------------------------
# Crear estudiantes
# -----------------------------
students = []
for first, last1, last2 in student_names:
    email = f"{first.lower()}.{last1.lower()}@school.com"
    existing_student = db.query(Student).filter(Student.email == email).first()
    if existing_student:
        print(f"⚠️ Estudiante {email} ya existe, se omite.")
        students.append(existing_student)
        continue
    student = Student(first_name=first, last_name=last1, last_name2=last2, email=email)
    db.add(student)
    db.commit()
    db.refresh(student)
    students.append(student)

# -----------------------------
# Crear materias
# -----------------------------
subjects = []
for subject_name in subjects_list:
    existing_subject = db.query(Subject).filter(Subject.name == subject_name).first()
    if existing_subject:
        print(f"⚠️ Materia {subject_name} ya existe, se omite.")
        subjects.append(existing_subject)
        continue
    # Asignar profesor al azar
    professor = random.choice([u for u in users if u.role == "profesor"])
    subject = Subject(name=subject_name, teacher_id=professor.id)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    subjects.append(subject)

# -----------------------------
# Inscribir estudiantes en materias (solo si no está inscrito)
# -----------------------------
for student in students:
    selected_subjects = random.sample(subjects, random.randint(3, 5))
    for subj in selected_subjects:
        if subj not in student.subjects:
            student.subjects.append(subj)
db.commit()

# -----------------------------
# Crear calificaciones (solo si no existe)
# -----------------------------
for student in students:
    for subject in student.subjects:
        existing_grade = db.query(Grade).filter(
            Grade.student_id == student.id,
            Grade.subject_id == subject.id
        ).first()
        if existing_grade:
            continue
        grade = Grade(score=random.uniform(60, 100), student_id=student.id, subject_id=subject.id)
        db.add(grade)
db.commit()

print("✅ Base de datos poblada sin duplicados.")
