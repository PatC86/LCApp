# Name: views
# Author: Patrick Cronin
# Date: 02/08/2024
# Updated: 24/09/2024
# Purpose: Define views.

from . import db
from .models import User
from .models import LiftingChain
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .liftingchainhealthscore import *
from .userrolewrappers import admin_required, contracteng_required
import logging

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        try:
            EquipNo = request.form.get('equip_no')
            ChainLength = request.form.get('chain_length')
            ChainCondition = request.form.get('chain_condition')
            ChainPitchLength = request.form.get('chain_pitch_length')
            MeanMeasuredPitchLength = request.form.get('mean_measured_pitch_length')
            PitchesMeasured = request.form.get('pitches_measured')

            if not all([EquipNo, ChainLength, ChainCondition, ChainPitchLength, MeanMeasuredPitchLength, PitchesMeasured]):
                flash('All fields required to be completed', category='error')
                return render_template('home.html', user=current_user)

            PercentWare = percentagewear(MeanMeasuredPitchLength, ChainPitchLength)
            ChainHealthScore = liftingchainhealthscore(PercentWare, ChainCondition)
            ChainPassed = chainpass(ChainHealthScore)

            if not 8000 <= int(EquipNo) <= 999999999999:
                flash('Equip No will be a whole number between 8000 and less than 999999999999 (inclusive)', category='error')
            elif not 1.0 <= float(ChainLength) <= 50:
                flash('Chain length should be between 1m and 50m (inclusive)', category='error')
            elif not 100 <= int(ChainPitchLength) <= 500:
                flash('Chain pitch length should be between 100mm and 500mm (inclusive)', category='error')
            elif int(ChainPitchLength) > int(MeanMeasuredPitchLength):
                flash('Mean measured pitch length will be greater than the original chain pitch length', category='error')
            elif 1 > int(ChainCondition) > 5:
                flash('Chain Condition should be a whole number from 1 to 5', category='error')
            elif int(PitchesMeasured) < 10:
                flash('At least 10 pitches should be measured', category='error')
            else:
                NewChainCondData = LiftingChain(
                    equip_no=EquipNo,
                    chain_length=ChainLength,
                    chain_condition=ChainCondition,
                    chain_pitch_length=ChainPitchLength,
                    mean_measured_pitch_length=MeanMeasuredPitchLength,
                    pitches_measured=PitchesMeasured,
                    chain_health_score=ChainHealthScore,
                    chain_passed=ChainPassed,
                    user_id=current_user.id)
            db.session.add(NewChainCondData)
            db.session.commit()
            flash('Chain data successfully added', category='success')

        except ValueError as e:
            logging.error(f'Error processing lifting chain data: {e}')
            flash('Invalid input for numerical fields')
        except Exception as e:
            logging.error(f"Error processing lifting chain: {e}")
            flash('An Error has occured while trying to add lifting chain data. Please try again.', category='error')

    return render_template('home.html', user=current_user)

@views.route('/adminchains', methods=['GET', 'POST'])
@admin_required
def liftingchainadmin():
    try:
        liftingchain_list = db.session.query(LiftingChain, User).join(User, LiftingChain.user_id == User.id).all()
        return render_template('adminchains.html', user=current_user, liftingchain_list=liftingchain_list)
    except Exception as e:
        logging.error(f"Error fetching lifting chain data: {e}")
        flash('An Error occurred will trying to fetching the lifting chain data. Please try again.', category='error')
        return redirect(url_for('views.home'))

@views.route('/delete_chain/<int:id>', methods=['POST'])
@admin_required
def delete_chain(id):
    try:
        liftingchain = LiftingChain.query.get(id)
        if liftingchain:
            db.session.delete(liftingchain)
            db.session.commit()
        else:
            flash('Error lifting chain not found', category='error')
    except Exception as e:
        logging.error(f'Error deleting chain with id {id}: {e}')
        flash('An Error occurred trying to delete the lifting chain data.Please try again.', category='error')
    return liftingchainadmin()

@views.route('/adminusers', methods=['GET', 'POST'])
@admin_required
def useradmin():
    try:
        user_list = User.query.all()
        return render_template('adminusers.html', user=current_user, user_list=user_list)
    except Exception as e:
        logging.error(f'Error get user data: {e}')
        flash('An Error occurred trying to retrieve user data. Please try again.', category='error')
        return redirect(url_for('views.home'))

@views.route('/delete_user/<int:id>', methods=['POST'])
@admin_required
def delete_user(id):
    try:
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            flash('Error user not found', category='error')
    except Exception as e:
        logging.error(f'An Error occurred while trying to delete user with id {id}: {e}')
        flash('An Error occurred while trying to delete the user. Please try again.', category='error')
    return useradmin()

@views.route('/update_role/<int:id>', methods=['POST'])
@admin_required
def update_role(id):
    try:
        new_role = request.form.get('role')
        if new_role not in ['admin', 'contracteng', 'standard']:
            flash('Error invalid role choice', category='error')
            return useradmin()

        user = User.query.get(id)
        if user:
            user.role = new_role
            db.session.commit()
        else:
            flash('User not found', category='error')
    except Exception as e:
        logging.error(f"An Error occurred while trying to update role for user with id {id}: {e}")
        flash('An Error occured while trying to update user role', category='error')
    return useradmin()

@views.route('/contengchains', methods=['GET'])
@contracteng_required
def liftingchainconteng():
    try:
        liftingchain_list = db.session.query(LiftingChain, User).join(User, LiftingChain.user_id == User.id).filter(LiftingChain.chain_health_score < 60).all()
        return render_template('contengchains.html', user=current_user, liftingchain_list=liftingchain_list)
    except Exception as e:
        logging.error(f"An Error occurred while trying to fetch the lifting chain data for Contract Engineer: {e}")
        flash('An Error occurred while tyring to fetching lifting chain data', category='error')
        return redirect(url_for('views.home'))
