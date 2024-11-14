import sys
import os
from pathlib import Path

# Añadir el directorio del proyecto al PATH para poder importar los módulos
project_dir = Path(__file__).parent
sys.path.append(str(project_dir))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def test_db_connection():
    """
    Script para probar la conexión a la base de datos usando la configuración de Flask
    """
    try:
        # Importar la configuración desde el módulo correcto
        from Glooba.config import SQLALCHEMY_DATABASE_URI
        
        # Crear una aplicación Flask mínima
        app = Flask(__name__)
        
        # Configurar la base de datos usando la configuración importada
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        print(f"\nIntentando conectar a: {SQLALCHEMY_DATABASE_URI}")
        
        # Inicializar SQLAlchemy
        db = SQLAlchemy(app)
        
        # Intentar establecer la conexión
        with app.app_context():
            # Intentar ejecutar una consulta simple
            result = db.session.execute('SELECT 1').fetchone()
            print("\n✅ Conexión exitosa a la base de datos!")
            print(f"Resultado de prueba: {result[0]}")
            return True
            
    except ImportError as e:
        print("\n❌ Error al importar la configuración:")
        print(f"Error: {str(e)}")
        print("\nAsegúrate de que:")
        print("1. El archivo config.py existe en Glooba/config.py")
        print("2. La variable SQLALCHEMY_DATABASE_URI está definida en config.py")
        return False
        
    except Exception as e:
        print("\n❌ Error al conectar a la base de datos:")
        print(f"Error: {str(e)}")
        print("\nVerifica lo siguiente:")
        print("1. Usuario y contraseña son correctos")
        print("2. La base de datos existe")
        print("3. PostgreSQL está ejecutándose")
        print("4. La configuración en config.py es correcta")
        return False

if __name__ == "__main__":
    test_db_connection()
