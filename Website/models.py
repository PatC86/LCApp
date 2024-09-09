from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class LiftingChain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equip_no = db.Column(db.String(12))
    equip_desc = db.Column(db.String(50), nullable=False)
    location_on_site = db.Column(db.String(50))
    SWL = db.Column(db.Float)
    date_installed = db.Column(db.DateTime(timezone=True))
    chain_length = db.Column(db.Float)
    site_no = db.Column(db.String(12), nullable=False)
    site_desc = db.Column(db.String(50), nullable=False)
    chain_condition = db.Column(db.Integer)
    mean_measured_pitch_length = db.Column(db.Integer)
    pitches_measured = db.Column(db.Integer)
    chain_health_score = db.Column(db.Float)
    chain_inspection_date = db.Column(db.DateTime(timezone=True), default=func.now())
    chain_passed = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    lifting_chains = db.relationship('LiftingChain')
