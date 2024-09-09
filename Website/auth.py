from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, user_logged_out, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Email = request.form.get('email')
        Password = request.form.get('password')

        user = User.query.filter_by(email=Email).first()
        if user:
            if check_password_hash(user.password, Password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Email not registered', category='error')

    return render_template('login.html', boolean = True)

@auth.route('/logoff')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        Email = request.form.get('email')
        FirstName = request.form.get('firstname')
        Surname = request.form.get('surname')
        Password1 = request.form.get('password1')
        Password2 = request.form.get('password2')

        user = User.query.filter_by(email=Email).first()
        if user:
            flash('Email already registered', category='error')
        elif len(Email) < 10:
            flash('Email must be greater than 9 characters', category='error')
        elif len(FirstName) < 2:
            flash('First Name must be longer than 1 Character', category='error')
        elif len(Surname) < 2:
            flash('Surname must be longer than 1 Character', category='error')
        elif Password1 != Password2:
            flash('Passwords do not match', category='error')
        elif len(Password1) < 9:
            flash('Password must be at least 8 Characters', category='error')
        else:
            new_user = User(email=Email, firstname=FirstName, surname=Surname, password=generate_password_hash(Password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account Created Successfully :D', category='success')
            return redirect(url_for('views.home'))
    return render_template('signup.html')