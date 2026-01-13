
from flask_wtf import FlaskForm

from wtforms import DateField, IntegerField, ValidationError, TextAreaField
from wtforms.fields import StringField, PasswordField, SubmitField, DateTimeLocalField
from wtforms.validators import InputRequired, Length, NumberRange, DataRequired, Optional,Email, EqualTo
from db import User,db

class UserExistsValidator:
    def __init__(self, message='WG-Mitglied existiert nicht'):
        self.message = message

    def __call__(self, form, field): 
        user = user = db.session.execute(db.select(User).filter_by(username=field.data)).scalars().first()
        if not user:
            raise ValidationError(self.message)

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

#Putzplan Forms
class PutzplanForm(FlaskForm):
    #datum = StringField('Datum', validators=[InputRequired(), Length(min=1, max=10)], render_kw={"placeholder": "TT.MM.JJJJ"})
    aufgabe = StringField('Aufgabe', validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "z.B. Bad putzen"})
    zustaendig = StringField('Zuständig', validators=[InputRequired(), Length(min=1, max=50), UserExistsValidator()], render_kw={"placeholder": "z.B. Max"})
    woche = IntegerField('Kalenderwoche', validators=[InputRequired(), NumberRange(min=1, max=53)], render_kw={"placeholder": "1-53"})
    von_datum = DateField('Von', validators=[InputRequired()], render_kw={"placeholder": "DD.MM.YYYY"})
    bis_datum = DateField('Bis', validators=[InputRequired()], render_kw={"placeholder": "DD.MM.YYYY"})
    submit = SubmitField('Erstellen')


#Innovationboard Forms
class InnovationForm(FlaskForm):
    title = StringField('Titel', validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "Titel der Idee"})
    description = TextAreaField("Beschreibung", validators=[DataRequired(), Length(min=1, max=500)], render_kw={"placeholder": "Beschreibe deine Idee hier..."})
    color = StringField('Farbe', validators=[InputRequired(), Length(min=7, max=7)], render_kw={"type": "color"})
    submit = SubmitField('Idee einreichen')

class CommentForm(FlaskForm):
    content = TextAreaField("Kommentar", validators=[DataRequired(), Length(min=1, max=300)], render_kw={"placeholder": "Schreibe einen Kommentar..."})
    submit = SubmitField('Kommentar posten')

#Activity Forms
class ActivityForm(FlaskForm):
    title = StringField('Titel', validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "Titel der Aktivität"})
    description = TextAreaField("Beschreibung", validators=[DataRequired(), Length(min=1, max=300)], render_kw={"placeholder": "Beschreibe deine Aktivität..."})
    date = DateTimeLocalField("Uhrzeit",format="%Y-%m-%dT%H:%M", validators=[DataRequired()], render_kw={"placeholder": "Wähle Datum und Uhrzeit"})
    updated_at = DateTimeLocalField("Uhrzeit",format="%Y-%m-%dT%H:%M", validators=[DataRequired()], render_kw={"placeholder": "Wähle Datum und Uhrzeit"})
    location = StringField('Ort', validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "Ort der Aktivität"})
    max_participants = IntegerField('Maximale Teilnehmerzahl', validators=[Optional(), NumberRange(min=1)], render_kw={"placeholder": "z.B. 10"})
    submit = SubmitField('Aktivität hinzufügen')

class EinkaufsplanForm(FlaskForm):
    item = StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "Artikel hinzufügen..."})
    quantity = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Menge"})
    submit = SubmitField('+')



    

