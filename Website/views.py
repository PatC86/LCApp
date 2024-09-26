# Name: views
# Author: Patrick Cronin
# Date: 02/08/2024
# Updated: 24/09/2024
# Purpose: Define views.

from . import db
from .models import User, LiftingChain, Locations
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .liftingchainhealthscore import *
from .userrolewrappers import admin_required, contracteng_required
import logging

MIN_EQUIP_NO = 8000
MAX_EQUIP_NO = 999999999999
MIN_CHAIN_LENGTH = 1.0
MAX_CHAIN_LENGTH = 50.0
MIN_PITCH_LENGTH = 100
MAX_PITCH_LENGTH = 500
MIN_CHAIN_CONDITION = 1
MAX_CHAIN_CONDITION = 5
MIN_PITCHES_MEASURED = 10

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    locations_list = Locations.query.all()

    if request.method == 'POST':
        try:
            EquipNo = request.form.get('equip_no')
            ChainLength = request.form.get('chain_length')
            ChainCondition = request.form.get('chain_condition')
            ChainPitchLength = request.form.get('chain_pitch_length')
            MeanMeasuredPitchLength = request.form.get('mean_measured_pitch_length')
            PitchesMeasured = request.form.get('pitches_measured')
            Location = request.form.get('location')

            if not all([EquipNo, ChainLength, ChainCondition, ChainPitchLength, MeanMeasuredPitchLength, PitchesMeasured, Location]):
                flash('All fields required to be completed', category='error')
                return render_template('home.html', user=current_user, locations_list=locations_list)

            PercentWare = percentagewear(MeanMeasuredPitchLength, ChainPitchLength)
            ChainHealthScore = liftingchainhealthscore(PercentWare, ChainCondition)
            ChainPassed = chainpass(ChainHealthScore)

            if not MIN_EQUIP_NO <= int(EquipNo) <= MAX_EQUIP_NO:
                flash('Equip No will be a whole number between 8000 and less than 999999999999 (inclusive)', category='error')
            elif not MIN_CHAIN_LENGTH <= float(ChainLength) <= MAX_CHAIN_LENGTH:
                flash('Chain length should be between 1m and 50m (inclusive)', category='error')
            elif not MIN_PITCH_LENGTH <= int(ChainPitchLength) <= MAX_PITCH_LENGTH:
                flash('Chain pitch length should be between 100mm and 500mm (inclusive)', category='error')
            elif int(ChainPitchLength) > int(MeanMeasuredPitchLength):
                flash('Mean measured pitch length will be greater than the original chain pitch length', category='error')
            elif MIN_CHAIN_CONDITION > int(ChainCondition) > MAX_CHAIN_CONDITION:
                flash('Chain Condition should be a whole number from 1 to 5', category='error')
            elif int(PitchesMeasured) < MIN_PITCHES_MEASURED:
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
                    user_id=current_user.id,
                    location_id=Location)
                db.session.add(NewChainCondData)
                db.session.commit()
                flash('Chain data successfully added', category='success')

        except ValueError as e:
            logging.error(f'Error processing lifting chain data: {e}')
            flash('Invalid input for numerical fields', category='error')
        except Exception as e:
            logging.error(f"Error processing lifting chain: {e}")
            flash('An Error has occurred while trying to add lifting chain data. Please try again.', category='error')

    return render_template('home.html', user=current_user, locations_list=locations_list)


@views.route('/adminchains', methods=['GET', 'POST'])
@admin_required
def liftingchainadmin():
    try:
        liftingchain_list = db.session.query(LiftingChain, User, Locations).join(User, LiftingChain.user_id == User.id).join(Locations, LiftingChain.location_id == Locations.id).all()
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
        liftingchain_list = db.session.query(LiftingChain, User, Locations).join(User, LiftingChain.user_id == User.id).join(Locations, LiftingChain.location_id == Locations.id).filter(LiftingChain.chain_health_score < 60).all()
        return render_template('contengchains.html', user=current_user, liftingchain_list=liftingchain_list)
    except Exception as e:
        logging.error(f"An Error occurred while trying to fetch the lifting chain data for Contract Engineer: {e}")
        flash('An Error occurred while tyring to fetching lifting chain data', category='error')
        return redirect(url_for('views.home'))

@views.route('/chainrecords', methods=['GET', 'POST'])
@login_required
def chainrecords():
    try:
        liftingchain_list = db.session.query(LiftingChain, User, Locations).join(User, LiftingChain.user_id == User.id).join(Locations, LiftingChain.location_id == Locations.id).all()
        return render_template('chainrecords.html', user=current_user, liftingchain_list=liftingchain_list)
    except Exception as e:
        logging.error(f"Error fetching lifting chain data: {e}")
        flash('An Error occurred will trying to fetching the lifting chain data. Please try again.', category='error')
        return redirect(url_for('views.home'))

@views.route('/locations', methods=['GET'])
@login_required
def locations():
    try:
        locations_list = Locations.query.all()
        return render_template('locations.html', user=current_user, locations_list=locations_list)
    except Exception as e:
        logging.error(f"Error fetching lifting chain data: {e}")
        flash('An Error occurred will trying to fetching the locations data. Please try again.', category='error')
        return redirect(url_for('views.home'))


@views.route('/save_inspection/<int:id>', methods=['POST'])
@login_required
def save_inspection(id):
    data = request.get_json()

    try:
        liftingchain = LiftingChain.query.get(id)

        if not liftingchain:
            return jsonify({'error': 'Record not found'}), 404

        chain_condition = int(data['chain_condition'])
        chain_pitch_length = float(data['chain_pitch_length'])
        mean_measured_pitch_length = float(data['mean_measured_pitch_length'])
        pitches_measured = int(data['pitches_measured'])

        if not MIN_PITCH_LENGTH <= chain_pitch_length <= MAX_PITCH_LENGTH:
            return jsonify({'error': 'Chain pitch length should be between 100mm and 500mm (inclusive)'}), 400

        if chain_pitch_length > mean_measured_pitch_length:
            return jsonify({'error': 'Mean measured pitch length should be greater than or equal to the original chain pitch length'}), 400

        if not MIN_CHAIN_CONDITION <= chain_condition <= MAX_CHAIN_CONDITION:
            return jsonify({'error': 'Chain condition should be a whole number between 1 and 5'}), 400

        if pitches_measured < MIN_PITCHES_MEASURED:
            return jsonify({'error': 'At least 10 pitches should be measured'}), 400

        PercentWare = percentagewear(mean_measured_pitch_length, chain_pitch_length)
        ChainHealthScore = liftingchainhealthscore(PercentWare, chain_condition)
        ChainPassed = chainpass(ChainHealthScore)

        liftingchain.chain_condition = chain_condition
        liftingchain.chain_pitch_length = chain_pitch_length
        liftingchain.mean_measured_pitch_length = mean_measured_pitch_length
        liftingchain.pitches_measured = pitches_measured
        liftingchain.chain_health_score = ChainHealthScore
        liftingchain.chain_passed = ChainPassed

        db.session.commit()

        return jsonify({'success': 'Chain inspection record updated successfully'}), 200

    except ValueError as e:
        return jsonify({'error': 'Invalid input for numerical fields'}), 400

    except Exception as e:
        logging.error(f"Error updating lifting chain record: {e}")
        return jsonify({'error': 'An error occurred while trying to update the record. Please try again later.'}), 500
