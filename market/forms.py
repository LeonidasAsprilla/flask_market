from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Nombre de usario ya existe! Por favor intente con otro nombre.")
    
    def validate_email_addres(self, email_addres_to_check):
        email_addres = User.query.filter_by(email_addres=email_addres_to_check.data).first()
        if email_addres:
            raise ValidationError("Email ya existe! Por favor intente con otro correo.")

    username = StringField(label='Nombre Usuario:', validators=[Length(min=2, max=30), DataRequired()])
    email_addres = StringField(label='Correo', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Contraseña:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Repita Contraseña', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Crear Cuenta')

