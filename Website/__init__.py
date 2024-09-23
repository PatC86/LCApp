from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
db_name = "database.db"


"""Initialise Web App"""


def create_App():
    App = Flask(__name__)
    App.config['SECRET_KEY'] = 'Super Duper Secret Key :D'
    App.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(App)

    from .views import views
    from .auth import auth

    App.register_blueprint(views, url_prefix='/')
    App.register_blueprint(auth, url_prefix='/')

    from .models import LiftingChain, User
    #from werkzeug.security import generate_password_hash

    #with App.app_context():
        #db.create_all()
        #print('Database successfully created !!! :D')
        #admin_user = User(email='admin@sw.co.uk', firstname='Admin', surname='Admin', role='admin',
        #              password=generate_password_hash('adminadmin', method='pbkdf2:sha256'))
        #db.session.add(admin_user)
        #db.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(App)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return App


