import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from film import app, db, bcrypt
from film.forms import RegistrationForm, LoginForm, PostForm
from film.models import User, Post, Film, Acteur, Regisseur, Rol
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('/register.html', title='Registeren', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('/login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

#Films
@app.route("/films")
def films():
    posts = Film.query.all()
    return render_template('/films/films.html', title='Films', posts=posts)

@app.route("/films/films_toevoegen", methods=['GET', 'POST'])
@login_required
def create_films():
    form = PostForm()
    if form.validate_on_submit():
        film = Film(titel=form.titel.data, releasedatum=form.releasedatum.data, toevoegingen=form.toevoegingen.data, regisseur_id=form.regisseur_id.data, acteur_id=form.acteur_id.data)
        db.session.add(film)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('films'))
    return render_template('/films/create_films.html', title='Film Toevoegen', form=form, legend='Film Toevoegen')

@app.route("/films/film/<int:film_id>")
def film(film_id):
    film = Film.query.get_or_404(film_id)
    return render_template('/films/read_films.html', title=film.titel, film=film)

@app.route("/films/film/<int:film_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_films(film_id):
    film = Film.query.get_or_404(film_id)
    form = PostForm()
    if form.validate_on_submit():
        film.titel = form.titel.data
        film.releasedatum = form.releasedatum.data
        film.toevoegingen = form.toevoegingen.data
        film.regisseur_id = form.regisseur_id.data
        film.acteur_id = form.acteur_id.data
        db.session.commit()
        flash('De filmgegevens zijn aangepast!', 'success')
        return redirect(url_for('film', film_id=film.id))
    elif request.method == 'GET':
        form.titel.data = film.titel
        form.releasedatum.data = film.releasedatum
        form.toevoegingen.data = film.toevoegingen
        form.regisseur_id.data = film.regisseur_id
        form.acteur_id.data = film.acteur_id
    return render_template('/films/create_films.html', title='Film Bewerken', form=form, legend='Film Bewerken')

@app.route("/films/film/<int:film_id>/delete", methods=['POST'])
@login_required
def delete_films(film_id):
    film = Film.query.get_or_404(film_id)
    db.session.delete(film)
    db.session.commit()
    flash('De film is verwijderd', 'success')
    return redirect(url_for('films'))

