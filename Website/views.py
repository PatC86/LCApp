from . import db
from .models import User
from .models import LiftingChain
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .admin import admin_required

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        EquipNo = request.form.get('equip_no')
        ChainLength = request.form.get('chain_length')
        ChainCondition = request.form.get('chain_condition')
        MeanMeasuredPitchLength = request.form.get('mean_measured_pitch_length')
        PitchesMeasured = request.form.get('pitches_measured')
        ChainHealthScore = 80
        ChainPassed = True

        if 1 > int(ChainCondition) > 5:
            flash('Chain Condition should be a whole number from 1 to 5', category='error')
        elif int(PitchesMeasured) < 10:
            flash('At least 10 pitches should be measured', category='error')
        else:
            NewChainCondData = LiftingChain(equip_no=EquipNo, chain_length=ChainLength, chain_condition=ChainCondition,
                                            mean_measured_pitch_length=MeanMeasuredPitchLength,
                                            pitches_measured=PitchesMeasured, chain_health_score=ChainHealthScore,
                                            chain_passed=ChainPassed, user_id=current_user.id)
            db.session.add(NewChainCondData)
            db.session.commit()
            flash('Chain data successfully added', category='success')
    return render_template('home.html', user=current_user)

@views.route('/adminchains', methods=['GET', 'POST'])
@login_required
@admin_required
def liftingchainadmin():
    liftingchain_list = LiftingChain.query.all()
    return render_template('adminchains.html', user=current_user, liftingchain_list=liftingchain_list)

@views.route('/adminusers', methods=['GET', 'POST'])
@login_required
@admin_required
def useradmin():
    user_list = User.query.all()
    return render_template('adminusers.html', user=current_user, user_list=user_list)