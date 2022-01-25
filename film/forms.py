from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from flask_login import current_user
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from film.models import User, Post, Film, Acteur, Regisseur, Rol

class RegistrationForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    confirm_password = PasswordField('Bevestig Wachtwoord', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registreer')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    remember = BooleanField('Herinner mij')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    titel = StringField('Titel', validators=[DataRequired()])
    releasedatum = DateField('Datum', format = '%Y-%m-%d')
    toevoegingen = TextAreaField('Toevoegingen')
    regisseur_id = StringField('ID Regisseur', validators=[DataRequired()])
    acteur_id = StringField('ID Acteur', validators=[DataRequired()])
    submit = SubmitField('Post')