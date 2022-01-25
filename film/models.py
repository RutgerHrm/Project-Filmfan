from datetime import datetime
from film import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # belangrijk foreign

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



# De rest

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(45), nullable=False)
    releasedatum = db.Column(db.Date, nullable=False)
    toevoegingen = db.Column(db.Text(500), nullable=True)
    regisseur_id = db.Column(db.Integer, db.ForeignKey('regisseur.id'), nullable=False)
    acteur_id = db.Column(db.Integer, db.ForeignKey('acteur.id'), nullable=False)
    acteur = db.relationship('Acteur', backref='author', lazy=True)
    regisseur = db.relationship('Regisseur', backref='author2', lazy=True)
    rol = db.relationship('Rol', backref='author3', lazy=True)

    def __repr__(self):
        return f"Film('{self.titel}', '{self.releasedatum}', '{self.toevoegingen}')"

class Acteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voornaam = db.Column(db.String(30), nullable=False)
    achternaam = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"Acteur('{self.voornaam}', '{self.achternaam}')"

class Regisseur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voornaam = db.Column(db.String(30), nullable=False)
    achternaam = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"Regisseur('{self.voornaam}', '{self.achternaam}')"

class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vertolk = db.Column(db.String(30), nullable=True)
    acteur_id = db.Column(db.Integer, db.ForeignKey('acteur.id'), nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)

    def __repr__(self):
        return f"Regisseur('{self.voornaam}', '{self.achternaam}')"
