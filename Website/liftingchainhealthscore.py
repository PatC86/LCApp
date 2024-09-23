PASS_SCORE = 60

def percentagewear(mean_measured_pitch_length, chain_pitch_length):
        percent_wear = float((int(chain_pitch_length) / int(mean_measured_pitch_length)) * 100)
        return percent_wear

def liftingchainhealthscore(percent_wear, chain_condition):
        if chain_condition == 5:
            return 1
        else:
            lifting_chain_health_score = percent_wear - (int(chain_condition) * (int(chain_condition) - 1))
            return lifting_chain_health_score

def chainpass(lifting_chain_health_score):
    if lifting_chain_health_score > PASS_SCORE:
        return True
    else:
        return False