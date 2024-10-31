import os
from datetime import timedelta

class Config:
    # Usar variables de entorno con valores por defecto seguros
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-never-use-this-in-production'
    
    # La URL de la base de datos se toma de una variable de entorno
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://admin:admin@localhost:5432/glooba_db'
    
    # Rutas configurables
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or '/home/martin/Tesis/Desarrollo/archivos_csv'

class ProductionConfig(Config):
    DEBUG = False
    # En producción, estas variables DEBEN estar configuradas en el ambiente
    def __init__(self):
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("No SECRET_KEY set for Production")
        if not os.environ.get('DATABASE_URL'):
            raise ValueError("No DATABASE_URL set for Production")

class DevelopmentConfig(Config):
    DEBUG = True
    # Valores por defecto seguros para desarrollo
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin@localhost:5432/glooba_db'

class TestingConfig(Config):
    TESTING = True
    # Base de datos específica para testing
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin@localhost:5432/glooba_db'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}