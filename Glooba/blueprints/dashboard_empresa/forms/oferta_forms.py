from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, Optional
from datetime import datetime

class OfertaForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[('PRODUCTO', 'Producto'), 
                                      ('SERVICIO', 'Servicio'), 
                                      ('DESCUENTO', 'Descuento')],
                      validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[Optional()])
    porcentaje_descuento = DecimalField('Porcentaje de Descuento', validators=[Optional()])
    fecha_inicio = DateField('Fecha de Inicio', validators=[DataRequired()])
    fecha_fin = DateField('Fecha de Fin', validators=[Optional()])
