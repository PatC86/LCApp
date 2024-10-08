# Name: models
# Author: Patrick Cronin
# Date: 02/08/2024
# Updated: 24/09/2024
# Purpose: Define db model for Lifting Chains and Users.

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class LiftingChain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equip_no = db.Column(db.String(12))
    chain_length = db.Column(db.Float)
    chain_condition = db.Column(db.Integer)
    chain_pitch_length = db.Column(db.Integer)
    mean_measured_pitch_length = db.Column(db.Integer)
    pitches_measured = db.Column(db.Integer)
    chain_health_score = db.Column(db.Float)
    chain_inspection_date = db.Column(db.DateTime(timezone=True), default=func.now())
    chain_passed = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))


class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer, nullable=False)
    location_desc = db.Column(db.String(30), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)
    lifting_chains = db.relationship('LiftingChain')
