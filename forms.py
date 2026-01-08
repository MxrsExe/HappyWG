from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField(
        "Benutzername",
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    password = PasswordField(
        "Passwort",
        validators=[DataRequired()]
    )
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField(
        "Benutzername",
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    email = StringField(
        "E-Mail",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Passwort",
        validators=[DataRequired(), Length(min=6)]
    )

    confirm_password = PasswordField(
        "Passwort bestätigen",
        validators=[DataRequired(),EqualTo('password', message="Passwörter stimmen nicht überein")]
    )

    submit = SubmitField("Registrieren")