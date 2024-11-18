import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde .flaskenv
load_dotenv('.flaskenv')


class Config:
    # Usar variables de entorno con valores por defecto seguros
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Construir la URL de la base de datos desde componentes individuales
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'glooba_db')

    # La URL de la base de datos se toma de una variable de entorno
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    # Rutas configurables
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or '/home/martin/Glooba_app/archivos_csv'

class ProductionConfig(Config):
    DEBUG = False
    # En producción, estas variables DEBEN estar configuradas en el ambiente
    def __init__(self):
        super().__init__()
        required_vars = [
            'SECRET_KEY',
            'DB_USER',
            'DB_PASSWORD',
            'DB_HOST',
            'DB_NAME',
            'UPLOAD_FOLDER'
        ]
        
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        if missing_vars:
            raise ValueError(
                f"Las siguientes variables de entorno son requeridas en producción: "
                f"{', '.join(missing_vars)}"
            )

class DevelopmentConfig(Config):
    DEBUG = True
    # Los valores por defecto para desarrollo se tomarán de .flaskenv

class TestingConfig(Config):
    TESTING = True
    # Para testing podemos usar una base de datos SQLite en memoria
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
