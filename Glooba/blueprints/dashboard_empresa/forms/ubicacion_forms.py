from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class UbicacionForm(FlaskForm):
    es_propia = BooleanField('¿Es tienda propia?', validators=[Optional()])
    nombre = StringField('Nombre del local/tienda', validators=[DataRequired(), Length(min=4, max=100)])
    latitud = FloatField('Latitud', validators=[DataRequired(), NumberRange(min=-90, max=90)])
    longitud = FloatField('Longitud', validators=[DataRequired(), NumberRange(min=-180, max=180)])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(min=4, max=200)])
    ciudad = StringField('Ciudad', validators=[DataRequired(), Length(min=4, max=100)])
    pais = StringField('País', validators=[DataRequired(), Length(min=4, max=100)])
    descripcion = TextAreaField('Descripción', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Confirmar')
