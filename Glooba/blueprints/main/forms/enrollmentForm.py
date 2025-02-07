from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email

class EmpresaEnrollmentForm(FlaskForm):
    nombre_empresa = StringField('Nombre de la Empresa', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    certificaciones = SelectField('Certificaciones', choices=[
        ('bcorp', 'B Corp'),
        ('carbon', 'Carbon Neutral'),
        ('leed', 'LEED'),
        ('otro', 'Otro')
    ], validators=[DataRequired()])
    descripcion = TextAreaField('Descripción Sustentable', validators=[DataRequired()])