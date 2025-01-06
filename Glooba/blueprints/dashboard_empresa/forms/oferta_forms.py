from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, \
    DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional

class OfertaForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[Optional()])
    es_descuento = BooleanField('Es un descuento', validators=[Optional()])
    porcentaje_descuento = DecimalField('Porcentaje de Descuento', validators=[Optional()])
    fecha_fin = DateField('Fecha de Fin', validators=[Optional()])
    submit = SubmitField('Confirmar')
