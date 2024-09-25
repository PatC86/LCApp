# Name: __init__
# Author: Patrick Cronin
# Date: 02/08/2024
# Updated: 24/09/2024
# Purpose: Creation of App, Database and initial admin user.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import logging


db = SQLAlchemy()
db_name = "lcappdatabase.db"


def create_App():
    App = Flask(__name__)

    try:
        App.config['SECRET_KEY'] = 'Super Duper Secret Key :D'
        App.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://lcappdatabase_rj41_user:Dq2A5NlKlY9WC06LNFuZMI1dqRos4ccU@dpg-crpl8q8gph6c739usnrg-a.frankfurt-postgres.render.com/lcappdatabase_rj41"
        db.init_app(App)

    except Exception as e:
        logging.error(f"Error during application configuration: {e}")
        raise

    from .views import views
    from .auth import auth

    try:
        App.register_blueprint(views, url_prefix='/')
        App.register_blueprint(auth, url_prefix='/')
    except Exception as e:
        logging.error(f"Error registering blueprint: {e}")
        raise

    from .models import LiftingChain, User


    with App.app_context():
        db.create_all()
        print('Database successfully created !!! :D')

        admin_user = User.query.filter_by(role='admin').first()
        if not admin_user:

            admin_user = User(email='admin@sw.co.uk', firstname='Admin', surname='Admin', role='admin',
                  password=generate_password_hash('adminadmin', method='pbkdf2:sha256'))
            db.session.add(admin_user)
            db.session.commit()
            print('Initial admin User created')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'

    try:
        login_manager.init_app(App)

        @login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))
    except Exception as e:
        logging.error(f"Error loading user with id {id}: {e}")
        return None

    return App
