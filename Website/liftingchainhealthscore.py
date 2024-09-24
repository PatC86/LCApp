# Name: liftingchainhealthscore
# Author: Patrick Cronin
# Date: 22/09/2024
# Updated: 24/09/2024
# Purpose: Function to calculate percentage wear, health score and pass status of lifting chains.

import logging
from flask import flash

PASS_SCORE = 60

def percentagewear(mean_measured_pitch_length, chain_pitch_length):
    """Calculate the percentage wear of a lifting chain"""
    try:
        mean_measured_pitch_length = int(mean_measured_pitch_length)
        chain_pitch_length = int(chain_pitch_length)

        if mean_measured_pitch_length == 0:
            raise ValueError("Mean measure pitch length must be greater than 0")

        percent_wear = float((chain_pitch_length / mean_measured_pitch_length) * 100)
        return percent_wear

    except ValueError as e:
        flash('Error mean measured pitch length should be greater than 0', category='error')
        logging.error(f"Invalid input for percentagewear calculation: {e}")
        raise
    except Exception as e:
        flash('An Error has occurred during form entry. Please Try Again')
        logging.error(f"An Error has occured in percentagewear calculation: {e}")
        raise

def liftingchainhealthscore(percent_wear, chain_condition):
    """Calculate the health score of a lifting chain"""
    try:
        percent_wear = float(percent_wear)
        chain_condition = int(chain_condition)

        if chain_condition == 5:
            return 1
        else:
            lifting_chain_health_score = percent_wear - (int(chain_condition) * (int(chain_condition) - 1))
            return lifting_chain_health_score

    except Exception as e:
        flash('An Error has occurred during form entry. Please Try Again')
        logging.error(f"An Error has occured in liftingchainhealthscore calculation: {e}")
        raise

def chainpass(lifting_chain_health_score):
    """Show if lifting chain health score is pass"""

    try:
        if lifting_chain_health_score > PASS_SCORE:
            return True
        else:
            return False
    except Exception as e:
        flash('An Error has occurred during form entry. Please Try Again')
        logging.error(f"An Error has occured in chainpass calculation: {e}")
        raise