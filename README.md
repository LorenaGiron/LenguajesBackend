# Mini-SICE API - Sistema de Gestión Escolar

Proyecto desarrollada con FastAPI para la gestión integral de un sistema escolar, incluyendo administración de estudiantes, profesores, materias, calificaciones y reportes académicos.

## Tabla de Contenidos

1. [Objetivos](#objetivos)
2. [Módulos Funcionales](#módulos-funcionales)
3. [Estructura de Carpetas](#estructura-de-carpetas)
4. [Endpoints Mínimos](#endpoints-mínimos)
5. [Tecnologías](#tecnologías)
6. [Modelo ER](#modelo-er)
7. [Instrucciones de Instalación](#instrucciones-de-instalación)
8. [Manual Técnico](#manual-técnico)
9. [Entregables Finales](#entregables-finales)

---

## Objetivos

### Propósitos de Aprendizaje

- Implementar una API RESTful completa utilizando FastAPI
- Aplicar principios de arquitectura en capas (API, CRUD, Modelos, Esquemas)
- Implementar autenticación y autorización con JWT
- Gestionar relaciones complejas en base de datos (Uno-a-Muchos, Muchos-a-Muchos)
- Desarrollar operaciones CRUD completas con validación de datos
- Generar reportes y estadísticas académicas

### Alcances del Proyecto

- Sistema de autenticación con tokens JWT
- Gestión completa de usuarios (profesores y administradores)
- Administración de estudiantes con búsqueda avanzada
- Gestión de materias con asignación de profesores
- Sistema de calificaciones por estudiante y materia
- Generación de reportes académicos y estadísticas
- Control de acceso basado en roles (admin/profesor)

---

## Módulos Funcionales

### Módulo de Autenticación
- Login de usuarios con generación de tokens JWT
- Validación de credenciales
- Protección de endpoints mediante autenticación Bearer

### Módulo de Usuarios
- Registro de profesores y administradores
- Consulta de usuarios con filtrado por rol
- Actualización y eliminación de usuarios
- Gestión de perfiles de usuario

### Módulo de Estudiantes
- CRUD completo de estudiantes
- Búsqueda de estudiantes por nombre, apellido o email
- Asignación de estudiantes a materias
- Consulta de información académica de estudiantes

### Módulo de Materias
- Creación y gestión de materias
- Asignación de profesores a materias
- Inscripción de estudiantes a materias (relación Many-to-Many)
- Consulta de carga académica por profesor
- Listado de estudiantes inscritos en una materia

### Módulo de Calificaciones
- Registro de calificaciones por estudiante y materia
- Consulta de calificaciones por estudiante
- Consulta de calificaciones por materia
- Actualización de calificaciones

### Módulo de Reportes
- Reporte académico individual por estudiante
- Promedio general de calificaciones
- Reporte de calificaciones por materia
- Estadísticas generales (total estudiantes, materias, profesores)
- Búsqueda de reportes por identificador de estudiante

---

## Estructura de Carpetas

```
LenguajesBackend/
├── schoolbackend/
│   └── app/
│       ├── api/                    # Capa de API/Rutas
│       │   ├── dependencies.py     # Dependencias compartidas (autenticación)
│       │   └── v1/                 # Versión 1 de la API
│       │       ├── auth.py         # Endpoints de autenticación
│       │       ├── users.py        # Endpoints de usuarios
│       │       ├── students.py     # Endpoints de estudiantes
│       │       ├── subjects.py     # Endpoints de materias
│       │       ├── grades.py       # Endpoints de calificaciones
│       │       ├── teacher.py      # Endpoints de profesores
│       │       └── reports.py      # Endpoints de reportes
│       │
│       ├── core/                   # Configuración central
│       │   ├── config.py           # Variables de configuración
│       │   └── security.py         # Utilidades de seguridad (JWT, hash)
│       │
│       ├── crud/                   # Capa de acceso a datos
│       │   ├── crud_user.py        # Operaciones CRUD de usuarios
│       │   ├── crud_student.py     # Operaciones CRUD de estudiantes
│       │   ├── crud_subject.py     # Operaciones CRUD de materias
│       │   ├── crud_grade.py       # Operaciones CRUD de calificaciones
│       │   └── crud_teacher.py      # Operaciones CRUD de profesores
│       │
│       ├── db/                     # Configuración de base de datos
│       │   ├── base.py             # Base de SQLAlchemy
│       │   └── session.py          # Configuración de sesión y conexión
│       │
│       ├── models/                 # Modelos de SQLAlchemy (ORM)
│       │   ├── user.py             # Modelo Usuario
│       │   ├── student.py          # Modelo Estudiante
│       │   ├── subject.py          # Modelo Materia
│       │   ├── grade.py            # Modelo Calificación
│       │   └── teacher.py          # Modelo Profesor
│       │
│       ├── schemas/                 # Esquemas Pydantic (validación)
│       │   ├── user.py             # Esquemas de Usuario
│       │   ├── student.py          # Esquemas de Estudiante
│       │   ├── subject.py          # Esquemas de Materia
│       │   ├── grade.py            # Esquemas de Calificación
│       │   └── teacher.py          # Esquemas de Profesor
│       │
│       └── main.py                 # Punto de entrada de la aplicación
│
├── venv/                           # Entorno virtual de Python
└── README.md                       # Este archivo
```

### Arquitectura del Backend

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
│                      (main.py)                          │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌─────────▼────────┐
│  API Layer     │            │  CORS Middleware │
│  (api/v1/)     │            │                  │
└───────┬────────┘            └─────────────────┘
        │
        │ Dependencies (Auth, DB Session)
        │
┌───────▼────────┐
│  CRUD Layer   │
│  (crud/)      │
└───────┬────────┘
        │
        │ SQLAlchemy ORM
        │
┌───────▼────────┐
│  Models Layer  │
│  (models/)     │
└───────┬────────┘
        │
        │ PyMySQL Driver
        │
┌───────▼────────┐
│   MySQL DB     │
└────────────────┘
```

---

## Endpoints Utilizados

### Autenticación
- `POST /api/v1/auth/login/access-token` - Iniciar sesión y obtener token JWT

### Usuarios
- `GET /api/v1/users/` - Listar usuarios (con filtro opcional por rol)
- `GET /api/v1/users/me` - Obtener información del usuario autenticado
- `POST /api/v1/users/` - Crear nuevo usuario
- `PUT /api/v1/users/{user_id}` - Actualizar usuario
- `DELETE /api/v1/users/{user_id}` - Eliminar usuario

### Estudiantes
- `GET /api/v1/students/` - Listar estudiantes 
- `GET /api/v1/students/{id}` - Obtener estudiante por ID
- `GET /api/v1/students/search/{query}` - Buscar estudiantes por nombre/apellido/email
- `POST /api/v1/students/` - Crear estudiante
- `PUT /api/v1/students/{id}` - Actualizar estudiante
- `DELETE /api/v1/students/{id}` - Eliminar estudiante

### Materias
- `GET /api/v1/subjects/` - Listar todas las materias
- `GET /api/v1/subjects/{subject_id}` - Obtener materia por ID
- `GET /api/v1/subjects/{subject_id}/students` - Obtener estudiantes de una materia
- `GET /api/v1/subjects/teacher-load/` - Obtener carga académica de profesor
- `POST /api/v1/subjects/` - Crear materia
- `PUT /api/v1/subjects/{subject_id}` - Actualizar materia
- `PUT /api/v1/subjects/{subject_id}/students/` - Asignar estudiantes a materia
- `DELETE /api/v1/subjects/{subject_id}/students/{student_id}` - Remover estudiante de materia
- `DELETE /api/v1/subjects/{subject_id}` - Eliminar materia

### Calificaciones
- `GET /api/v1/grades/student/{student_id}` - Obtener calificaciones de un estudiante
- `GET /api/v1/grades/by-subject/{subject_id}` - Obtener calificaciones de una materia
- `POST /api/v1/grades/` - Crear calificación
- `PUT /api/v1/grades/{grade_id}` - Actualizar calificación

### Reportes
- `GET /api/v1/reports/student/{student_id}` - Reporte académico de estudiante
- `GET /api/v1/reports/student-grades-search/{identifier}` - Buscar reporte por identificador
- `GET /api/v1/reports/subject-grades/{subject_id}` - Reporte de calificaciones por materia
- `GET /api/v1/reports/stats/students` - Total de estudiantes
- `GET /api/v1/reports/stats/subjects` - Total de materias
- `GET /api/v1/reports/stats/professors` - Total de profesores

**Nota:** Todos los endpoints (excepto login y algunos reportes públicos) requieren autenticación mediante token Bearer.

---

## Tecnologías

### Lenguajes y Frameworks
- **Python 3.8+** - Lenguaje de programación
- **FastAPI 0.122.0** - Framework web moderno y rápido
- **Uvicorn** - Servidor ASGI de alto rendimiento

### Base de Datos
- **MySQL** - Sistema de gestión de bases de datos relacional
- **SQLAlchemy 2.0.44** - ORM (Object-Relational Mapping)
- **PyMySQL 1.1.2** - Driver MySQL para Python

### Seguridad y Autenticación
- **Python-JOSE** - Implementación de JWT (JSON Web Tokens)
- **Passlib** - Biblioteca para hash de contraseñas
- **Bcrypt 3.2.2** - Algoritmo de hash para contraseñas

### Validación y Utilidades
- **Pydantic** - Validación de datos usando tipos de Python
- **Python-dotenv** - Gestión de variables de entorno
- **Email-validator** - Validación de direcciones de correo

---

## Modelo ER

### Diagrama Entidad-Relación

```mermaid
erDiagram
    USER ||--o{ SUBJECT : "imparte"
    STUDENT ||--o{ GRADE : "obtiene"
    SUBJECT ||--o{ GRADE : "evalúa"
    STUDENT }o--o{ SUBJECT : "inscrito_en"

    USER {
        int id PK
        string email UK
        string hashed_password
        string full_name
        string role
        boolean is_active
    }

    STUDENT {
        int id PK
        string first_name
        string last_name
        string last_name2
        string email UK
    }

    SUBJECT {
        int id PK
        string name UK
        int teacher_id FK
    }

    GRADE {
        int id PK
        float score
        int student_id FK
        int subject_id FK
    }
```

### Descripción de Entidades

**User (Usuarios)**
- Almacena información de profesores y administradores
- Relación 1:N con Subject (un profesor puede tener múltiples materias)
- Campos: id, email (único), hashed_password, full_name, role, is_active

**Student (Estudiantes)**
- Almacena información de estudiantes
- Relación N:M con Subject (un estudiante puede estar en múltiples materias)
- Relación 1:N con Grade (un estudiante puede tener múltiples calificaciones)
- Campos: id, first_name, last_name, last_name2, email (único)

**Subject (Materias)**
- Almacena información de materias académicas
- Relación N:1 con User (cada materia tiene un profesor asignado)
- Relación N:M con Student (una materia puede tener múltiples estudiantes)
- Relación 1:N con Grade (una materia puede tener múltiples calificaciones)
- Campos: id, name (único), teacher_id

**Grade (Calificaciones)**
- Almacena las calificaciones de estudiantes por materia
- Relación N:1 con Student (cada calificación pertenece a un estudiante)
- Relación N:1 con Subject (cada calificación pertenece a una materia)
- Campos: id, score, student_id, subject_id

**student_subject (Tabla de asociación)**
- Tabla intermedia para la relación Many-to-Many entre Student y Subject
- Permite que un estudiante esté inscrito en múltiples materias

---

## Instrucciones de Instalación

### Requisitos Previos

- Python 3.8 o superior
- MySQL 5.7 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd LenguajesBackend
```

### Paso 2: Crear Entorno Virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install fastapi uvicorn sqlalchemy pymysql pydantic python-dotenv email-validator "passlib[bcrypt]" "python-jose[cryptography]" python-multipart bcrypt==3.2.2
```

### Paso 4: Configurar Base de Datos

1. Crear la base de datos en MySQL:
```sql
CREATE DATABASE IF NOT EXISTS DB_Escolar;
USE DB_Escolar;
```

2. Crear archivo `.env` en la carpeta `schoolbackend/`:
```env
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/school_db
SECRET_KEY=tu-clave-secreta-super-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Importante:** Reemplazar `usuario`, `contraseña` y `tu-clave-secreta-super-segura-aqui` con valores reales.

### Paso 5: Ejecutar la Aplicación

```bash
cd schoolbackend
uvicorn app.main:app --reload
```

El servidor estará disponible en: `http://127.0.0.1:8000`

### Paso 6: Acceder a la Documentación

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## Manual Técnico

### Configuración

#### Variables de Entorno

El archivo `.env` debe contener las siguientes variables:

- `DATABASE_URL`: Cadena de conexión a MySQL en formato SQLAlchemy
- `SECRET_KEY`: Clave secreta para firmar tokens JWT (debe ser segura y aleatoria)
- `ALGORITHM`: Algoritmo de encriptación JWT (por defecto HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token en minutos

#### Configuración de CORS

La aplicación está configurada para aceptar peticiones desde:
- `http://localhost:5173` (Vite/React)
- `http://localhost:3000` (Create-React-App)
- `*` (todos los orígenes - solo para desarrollo)

### Dependencias Principales

```
fastapi==0.122.0
uvicorn==0.38.0
sqlalchemy==2.0.44
pymysql==1.1.2
pydantic
python-dotenv==1.2.1
email-validator==2.3.0
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.5.0
python-multipart==0.0.20
bcrypt==3.2.2
```

### Despliegue

#### Desarrollo Local

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Autenticación

El sistema utiliza JWT (JSON Web Tokens) para autenticación:

1. **Obtener token:**
   ```bash
   POST /api/v1/auth/login/access-token
   Content-Type: application/x-www-form-urlencoded
   
   username=email@ejemplo.com
   password=contraseña
   ```

2. **Usar token en peticiones:**
   ```bash
   Authorization: Bearer <token>
   ```

### Creación Automática de Tablas

Las tablas se crean automáticamente al iniciar la aplicación mediante:
```python
Base.metadata.create_all(bind=engine)
```

---

## Entregables Finales
## Entregables Finales

### Backend (API)
- Código completo del backend con arquitectura en capas
- Autenticación JWT implementada
- Validaciones en cada endpoint con Pydantic
- Conexión a base de datos MySQL mediante SQLAlchemy
- Postman Collection exportada (disponible en el repositorio)
- Documentación completa de endpoints (métodos, parámetros, respuestas, errores, ejemplos)
- Documentación interactiva en `/docs` (Swagger UI) y `/redoc`

### Frontend
- Manejo de autenticación con el backend
- Consumo de API con CRUD completo
- Protección de rutas privadas
- Interfaz moderna con framework CSS

### Documentación
- **README.md** - Documentación detallada del proyecto (este documento)
- **Modelo ER** - Diagrama entidad-relación de la base de datos (incluido en este README)
- **Diagramas de Arquitectura** - Diagramas de flujo y arquitectura del backend (incluidos en este README)
- **Script SQL** - Configuración completa de la base de datos MySQL
- **Manual de Usuario** - Screenshots y flujo de uso de la aplicación
- **Manual Técnico** - Configuración, dependencias y despliegue (incluido en este README)

### Video
- Demostración funcional del proyecto
- Contenido del video:
  - Login y autenticación
  - Flujo principal de la aplicación
  - CRUDs funcionando
  - Validaciones implementadas
  - Explicación rápida de la arquitectura

---
