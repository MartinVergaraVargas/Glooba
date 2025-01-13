from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, URLField, \
    DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed

class OfertaForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    precio = IntegerField('Precio', validators=[Optional()])
    es_descuento = BooleanField('Es un descuento', validators=[Optional()])
    porcentaje_descuento = IntegerField('Porcentaje de Descuento', validators=[Optional()])
    fecha_fin = DateField('Fecha de Fin', validators=[Optional()])
    imagen = FileField('Imagen de la Oferta', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Solo se permiten imágenes JPG, JPEG, PNG y WEBP.')
    ])
    sitio_web = URLField('Enlace del Sitio Web', validators=[Optional()]) 
    submit = SubmitField('Confirmar')

