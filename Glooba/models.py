from datetime import datetime, timezone
from enum import Enum
from flask_login import UserMixin
from flask import url_for  # Para crear URLs de la imagen de perfil.
from . import db
from werkzeug.utils import secure_filename

class User(UserMixin, db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(100))
    password = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    ultima_conexion = db.Column(db.DateTime)
    imagen_perfil = db.Column(db.String(255), nullable=True)  # Ruta de la imagen

    @property
    def imagen_perfil_url(self):
        tipo_usuario = self.__class__.__name__.lower()
        nombre_usuario = secure_filename(self.nombre)
        return url_for(
            'static', 
            filename=f'uploads/profile/{tipo_usuario}/{nombre_usuario}/picture/perfil/{self.imagen_perfil}', 
            _external=True
        ) if self.imagen_perfil else None

    # Similar para otras imágenes (imagen_principal_url, imagen_secundaria_arriba_url, etc.)


    # Agregar campo para identificar el tipo de usuario
    @property
    def user_type(self):
        return self.__class__.__name__
    
    def get_id(self):
        """
        Sobrescribe el método get_id de UserMixin para incluir el tipo de usuario
        """
        return f"{self.user_type}:{self.id}"

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.email}>'


class CommonUser(User):
    __tablename__ = 'common_user'
    apellido1 = db.Column(db.String(100), nullable=False)
    apellido2 = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    verificacion_email = db.Column(db.Boolean)
    token_verificacion = db.Column(db.String(100))  # Para el proceso de verificación por email
    
    # Relaciones
    favoritos = db.relationship('Favorito', 
                              backref='usuario', 
                              lazy=True, 
                              cascade='all, delete-orphan')
    
    reportes_stock = db.relationship('UsuarioStock', 
                                   backref='usuario', 
                                   lazy=True, 
                                   cascade='all, delete-orphan')
    
    @property
    def ofertas_favoritas(self):
        """Obtener las ofertas favoritas del usuario"""
        return Oferta.query.join(Favorito).filter(Favorito.usuario_id == self.id).all()
    
    @property
    def nombre_completo(self):
        if self.apellido2:
            return f"{self.nombre} {self.apellido1} {self.apellido2}"
        return f"{self.nombre} {self.apellido1}"

class Empresa(User):
    __tablename__ = 'empresa'
    rut_empresa = db.Column(db.String(50), unique=True, nullable=False)
    sitio_web = db.Column(db.String(255))
    rubro = db.Column(db.String(255))
    certificaciones = db.Column(db.String(255), nullable=True)
    servicio_a_domicilio = db.Column(db.Boolean, default=False)
    descripcion = db.Column(db.Text)
    imagen_principal = db.Column(db.String(255), nullable=True) 
    imagen_secundaria_arriba = db.Column(db.String(255), nullable=True)  
    imagen_secundaria_abajo = db.Column(db.String(255), nullable=True)  

    # Relaciones
    ubicaciones = db.relationship('Ubicacion', backref='empresa', lazy=True, cascade='all, delete-orphan')
    ofertas = db.relationship('Oferta', backref='empresa', lazy=True, cascade='all, delete-orphan')

    @property
    def imagen_perfil_url(self):
        tipo_usuario = self.__class__.__name__.lower()
        nombre_usuario = secure_filename(self.nombre)
        return url_for(
            'static', 
            filename=f'uploads/profile/{tipo_usuario}/{nombre_usuario}/picture/perfil/{self.imagen_perfil}', 
            _external=True
        ) if self.imagen_perfil else None

    @property
    def imagen_principal_url(self):
        tipo_usuario = self.__class__.__name__.lower()
        nombre_usuario = secure_filename(self.nombre)
        print(f'uploads/profile/{tipo_usuario}/{nombre_usuario}/picture/principal/{self.imagen_principal}')
        return url_for(
            'static', 
            filename=f'uploads/profile/{tipo_usuario}/{nombre_usuario}/picture/principal/{self.imagen_principal}', 
            _external=True
        ) if self.imagen_principal else None

    @property
    def imagen_secundaria_arriba_url(self):
        tipo_usuario = self.__class__.__name__.lower()
        nombre_usuario = secure_filename(self.nombre)
        return url_for(
            'static', 
            filename=f'uploads/profile/{tipo_usuario}/{nombre_usuario}/picture/secundaria_arriba/{self.imagen_secundaria_arriba}', 
            _external=True
        ) if self.imagen_secundaria_arriba else None

    @property
    def imagen_secundaria_abajo_url(self):
        tipo_usuario = self.__class__.__name__.lower()
        nombre_usuario = secure_filename(self.nombre)
        return url_for(
            'static', 
            filename=f'uploads/profile/{tipo_usuario}/{nombre_usuario}/picture/secundaria_abajo/{self.imagen_secundaria_abajo}', 
            _external=True
        ) if self.imagen_secundaria_abajo else None


    @property
    def sitio_web_formateado(self):
        """Retorna la URL del sitio web correctamente formateada"""
        if not self.sitio_web:
            return None
            
        url = self.sitio_web.strip()
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

    def set_sitio_web(self, url):
        """Formatea y valida la URL antes de guardarla"""
        if url:
            url = url.strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
        self.sitio_web = url

class Administrador(User):
    __tablename__ = 'administrador'
    pass

class TipoOferta(Enum):
    SERVICIO = 'Servicio'
    PRODUCTO = 'Producto'

class Oferta(db.Model):
    __tablename__ = 'oferta'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Integer) 
    es_descuento = db.Column(db.Boolean, default=False) 
    porcentaje_descuento = db.Column(db.Integer)
    fecha_inicio = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    fecha_fin = db.Column(db.DateTime)
    activa = db.Column(db.Boolean, default=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    sitio_web = db.Column(db.String(255), nullable=True) 

    # Relaciones
    ubicaciones = db.relationship('UbicacionOferta', backref='oferta', lazy=True, cascade='all, delete-orphan')
    favoritos = db.relationship('Favorito', backref='oferta', lazy=True, cascade='all, delete-orphan')
    
    @property
    def nombre_empresa(self):
        """Devuelve el nombre de la empresa asociada a esta oferta."""
        return self.empresa.nombre if self.empresa else None
    
    @property
    def imagen_oferta_url(self):
        """Retorna la URL de la imagen de la oferta."""
        nombre_empresa = secure_filename(self.nombre_empresa) if self.nombre_empresa else "default"
        return url_for(
            'static', 
            filename=f'uploads/profile/empresa/{nombre_empresa}/picture/oferta/{self.imagen}', 
            _external=True
        ) if self.imagen else None


class Ubicacion(db.Model):
    __tablename__ = 'ubicacion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)  # Nombre del local/tienda
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    es_propia = db.Column(db.Boolean, default=False)  # True si es tienda propia de la empresa
    activa = db.Column(db.Boolean, default=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
    descripcion = db.Column(db.String(250))
    
    # Relaciones
    ofertas = db.relationship('UbicacionOferta', backref='ubicacion', lazy=True, cascade='all, delete-orphan')
    
    @property
    def logo_empresa_url(self):
        """Retorna la URL de la imagen del perfil."""
        nombre_empresa = secure_filename(self.empresa.nombre) if self.empresa else "default"
        return url_for(
            'static', 
            filename=f'uploads/profile/empresa/{nombre_empresa}/picture/ubicacion/{self.imagen}', 
            _external=True
        ) if self.imagen else None
    

class Favorito(db.Model):
    __tablename__ = 'favorito'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('common_user.id'), nullable=False)
    oferta_id = db.Column(db.Integer, db.ForeignKey('oferta.id'), nullable=False)
    fecha_agregado = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    __table_args__ = (db.UniqueConstraint('usuario_id', 'oferta_id'),)

class UbicacionOferta(db.Model):
    __tablename__ = 'ubicacion_oferta'
    id = db.Column(db.Integer, primary_key=True)
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicacion.id'), nullable=False)
    oferta_id = db.Column(db.Integer, db.ForeignKey('oferta.id'), nullable=False)
    stock_actual = db.Column(db.Boolean, default=True)  # Estado actual del stock
    ultima_actualizacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relaciones
    historial_stock = db.relationship('Stock', backref='ubicacion_oferta', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (db.UniqueConstraint('ubicacion_id', 'oferta_id'),)

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    ubicacion_oferta_id = db.Column(db.Integer, db.ForeignKey('ubicacion_oferta.id'), nullable=False)
    stock_disponible = db.Column(db.Boolean, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    es_oficial = db.Column(db.Boolean, default=False, nullable=False)  # True si es actualización de empresa/admin
    
    # Relaciones
    reportes_usuarios = db.relationship('UsuarioStock', backref='stock', lazy=True, cascade='all, delete-orphan')

class UsuarioStock(db.Model):
    __tablename__ = 'usuario_stock'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('common_user.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    fecha_reporte = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
class Solicitud_Registro_Empresa(db.Model):
    __tablename__ = 'solicitud_registro_empresa'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    certificaciones = db.Column(db.String(255), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    fecha_solicitud = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    estado = db.Column(db.String(50), nullable=True)
