from flask import Flask

"""Initialise Web App"""
def create_LCapp():
    LCapp = Flask(__name__)
    LCapp.config['SECRET_KEY'] = 'Super Duper Secret Key :D'

    from .views import views
    from .auth import auth

    LCapp.register_blueprint(views, url_prefix='/')
    LCapp.register_blueprint(auth, url_prefix='/')

    return LCapp