# Name: auth
# Author: Patrick Cronin
# Date: 02/08/2024
# Updated: 24/09/2024
# Purpose: Define authorisation routes.

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import logging
import re

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Email = request.form.get('email')
        Password = request.form.get('password')
        try:
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
        except Exception as e:
            flash('An Error has occurred during Log In. Please Try Again', category='error')
            logging.error(f"log in error: {e}")

    return render_template('login.html', user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        Email = request.form.get('email')
        FirstName = request.form.get('firstname')
        Surname = request.form.get('surname')
        Password1 = request.form.get('password1')
        Password2 = request.form.get('password2')

        try:
            user = User.query.filter_by(email=Email).first()
            password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
            email_regex = r'^[a-zA-Z0-9._%+-]+@sw\.co\.uk$'
            if user:
                flash('Email already registered', category='error')
            elif len(Email) < 10:
                flash('Email must be greater than 9 characters', category='error')
            elif not re.match(Email, email_regex):
                flash('email must be southern water @sw.co.uk address')
            elif len(FirstName) < 2:
                flash('First Name must be longer than 1 Character', category='error')
            elif len(Surname) < 2:
                flash('Surname must be longer than 1 Character', category='error')
            elif Password1 != Password2:
                flash('Passwords do not match', category='error')
            elif len(Password1) < 9:
                flash('Password must be at least 8 Characters', category='error')
            elif not re.match(password_regex, Password1):
                flash('Password must contain a number, symbol, uppercase and lowercase letter', category='error')
            else:
                new_user = User(email=Email, firstname=FirstName, surname=Surname, role='standard',
                            password=generate_password_hash(Password1, method='pbkdf2:sha256').decode('utf-8'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account Created Successfully :D', category='success')
                return redirect(url_for('views.home'))
        except Exception as e:
            flash('An Error has occurred during sign up. Please try again.', category='error')
            logging.error(f"Sign up error: {e}")

    return render_template('signup.html', user=current_user)


@auth.route('/logoff')
@login_required
def logout():
    try:
        logout_user()
        flash('Log out successful!', category='success')

    except Exception as e:
        flash('An Error has occurred during log out. Please try again.', category='error')
        logging.error(f"Log out error: {e}")
    return redirect(url_for('auth.login'))
