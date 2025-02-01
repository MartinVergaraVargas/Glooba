from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, URLField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, URL, Optional
from flask_wtf.file import FileField, FileAllowed

class EmpresaProfileForm(FlaskForm):
    imagen_perfil = FileField(
        'Imagen de Perfil', 
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten imágenes JPG, JPEG, PNG y WEBP')]
    )
    nombre = StringField('Nombre Empresa', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    rut_empresa = StringField('RUT Empresa', validators=[DataRequired(), Length(max=50)])
    telefono = TelField('Teléfono', validators=[Optional(), Length(max=20)])
    sitio_web = URLField('Sitio Web', validators=[Optional(), URL(), Length(max=150)])
    rubro = StringField('Rubro', validators=[DataRequired(), Length(max=150)])
    certificaciones = StringField('Certificacion(es)', validators=[Optional(), Length(max=150)])
    servicio_a_domicilio = BooleanField('Servicio a Domicilio')
    descripcion = TextAreaField('Descripción')
    imagen_principal = FileField(
        'Imagen Principal', 
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Solo se permiten imágenes JPG, JPEG, PNG y WEBP')]
    )
    imagen_secundaria_arriba = FileField(
        'Imagen Secundaria Arriba', 
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Solo se permiten imágenes JPG, JPEG, PNG y WEBP')]
    )
    imagen_secundaria_abajo = FileField(
        'Imagen Secundaria Abajo', 
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Solo se permiten imágenes JPG, JPEG, PNG y WEBP')]
    )

