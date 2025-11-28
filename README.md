1. Crear un entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

2. Activar entorno virtual

.\venv\Scripts\Activate.ps1


3. Instalar dependencias:
pip install fastapi uvicorn sqlalchemy pymysql pydantic python-dotenv email-validator "passlib[bcrypt]" "python-jose[cryptography]" python-multipart bcrypt==3.2.2


4.Dirigirse a la carpeta:

cd schoolbackend

5.  uvicorn app.main:app --reload


6. Si se desea probar los endpoint dirigirse a -----http://127.0.0.1:8000/docs

ola