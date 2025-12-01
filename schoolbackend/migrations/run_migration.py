"""
Script para ejecutar la migración de agregar campos de perfil al modelo User
Ejecutar: python -m schoolbackend.migrations.run_migration
"""
from sqlalchemy import text
from app.db.session import engine
import sys

def run_migration():
    """Ejecuta la migración para agregar campos description y photo_url"""
    
    migration_sql = """
    ALTER TABLE users 
    ADD COLUMN IF NOT EXISTS description TEXT NULL,
    ADD COLUMN IF NOT EXISTS photo_url VARCHAR(500) NULL;
    """
    
    # MySQL no soporta IF NOT EXISTS en ALTER TABLE, así que usamos un enfoque diferente
    migration_sql_mysql = """
    ALTER TABLE users 
    ADD COLUMN description TEXT NULL AFTER is_active,
    ADD COLUMN photo_url VARCHAR(500) NULL AFTER description;
    """
    
    try:
        with engine.connect() as connection:
            # Verificar si las columnas ya existen
            check_sql = """
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME IN ('description', 'photo_url');
            """
            
            result = connection.execute(text(check_sql))
            existing_columns = [row[0] for row in result]
            
            if 'description' in existing_columns and 'photo_url' in existing_columns:
                print("✅ Las columnas 'description' y 'photo_url' ya existen en la tabla users")
                return True
            
            # Ejecutar la migración
            print("🔄 Ejecutando migración...")
            
            if 'description' not in existing_columns:
                connection.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN description TEXT NULL AFTER is_active
                """))
                print("✅ Columna 'description' agregada")
            
            if 'photo_url' not in existing_columns:
                connection.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN photo_url VARCHAR(500) NULL AFTER description
                """))
                print("✅ Columna 'photo_url' agregada")
            
            connection.commit()
            print("✅ Migración completada exitosamente")
            return True
            
    except Exception as e:
        error_msg = str(e)
        if "Duplicate column name" in error_msg or "already exists" in error_msg.lower():
            print("✅ Las columnas ya existen en la base de datos")
            return True
        else:
            print(f"❌ Error al ejecutar la migración: {e}")
            return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)

