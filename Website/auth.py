from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', text="testing", user="Patrick", boolean = True)

@auth.route('/logoff')
def logout():
    return '<p>LogOut</p>'

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        Email = request.form.get('email')
        FirstName = request.form.get('firstname')
        Surname = request.form.get('surname')
        Password1 = request.form.get('password1')
        Password2 = request.form.get('password2')

        if len(Email) < 10:
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
            flash('Account Created Successfully :D', category='success')
    return render_template('signup.html')