from flask_wtf import FlaskForm

from wtforms import DateField, IntegerField, ValidationError, TextAreaField
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange, DataRequired
from db import User,db

class UserExistsValidator:
    def __init__(self, message='WG-Mitglied existiert nicht'):
        self.message = message

    def __call__(self, form, field): 
        user = user = db.session.execute(db.select(User).filter_by(username=field.data)).scalars().first()
        if not user:
            raise ValidationError(self.message)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=100)])
    submit = SubmitField('Login')

class CreateTodoForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=1, max=100)])
    description = StringField('Description', validators=[Length(max=500)])
    submit = SubmitField('Create Todo')

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
    submit = SubmitField('Idee einreichen')

class CommentForm(FlaskForm):
    content = TextAreaField("Kommentar", validators=[DataRequired(), Length(min=1, max=300)], render_kw={"placeholder": "Schreibe einen Kommentar..."})
    submit = SubmitField('Kommentar posten')
    

