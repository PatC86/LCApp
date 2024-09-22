from . import db
from .models import LiftingChain
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        EquipNo = int(request.form.get('equip_no'))
        ChainLength = float(request.form.get('chain_length'))
        ChainCondition = int(request.form.get('chain_condition'))
        MeanMeasuredPitchLength = int(request.form.get('mean_measured_pitch_length'))
        PitchesMeasured = int(request.form.get('pitches_measured'))
        ChainHealthScore = 80
        ChainPassed = True

        if 1 > ChainCondition > 5:
            flash('Chain Condition should be a whole number from 1 to 5', category='error')
        elif PitchesMeasured < 10:
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


