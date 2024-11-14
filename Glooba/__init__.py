from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import logging
import os
from .config import config

# Configurar logging a nivel de módulo
logger = logging.getLogger(__name__)

# Inicializar extensiones
db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='default'):
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    # Configurar login manager
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Configurar logging para producción
    configure_logging(app)

    # Importar modelos
    from .models import CommonUser, Empresa, Administrador
    from .blueprints.auth.auth import auth_bp, GuestUser

    # Registrar función de carga de usuario
    @login_manager.user_loader
    def load_user(user_id):
        logger.debug(f"Intentando cargar usuario con ID: {user_id}")
        
        if user_id == 'guest':
            logger.debug("Cargando usuario invitado")
            return GuestUser()
        
        try:
            user_type, id_str = user_id.split(":")
            user_id = int(id_str)
        except (ValueError, AttributeError):
            logger.warning(f"ID de usuario inválido: {user_id}")
            return None
        
        user_classes = {
            'CommonUser': CommonUser,
            'Empresa': Empresa,
            'Administrador': Administrador
        }
        
        UserClass = user_classes.get(user_type)
        if not UserClass:
            logger.warning(f"Tipo de usuario inválido: {user_type}")
            return None
        
        user = UserClass.query.get(user_id)
        if user:
            logger.debug(f"Usuario encontrado como {user_type}: {user.email}")
            return user
        
        logger.warning(f"No se encontró ningún usuario con ID: {user_id}")
        return None

    # Registrar blueprints
    register_blueprints(app)

    return app

def configure_logging(app):
    """Configura el sistema de logging según el entorno"""
    if not app.debug and not app.testing:
        if app.config.get('LOG_TO_STDOUT'):
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = logging.FileHandler('logs/glooba.log')
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Glooba startup')

def register_blueprints(app):
    """Registra todos los blueprints de la aplicación"""
    from .blueprints.main.main import main_bp
    from .blueprints.auth.auth import auth_bp
    from .blueprints.administracion.administracion import admin_bp
    from .blueprints.perfil.perfil import perfil_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(perfil_bp, url_prefix='/perfil')