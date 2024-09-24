# Name: userrolewrappers
# Author: Patrick Cronin
# Date: 22/09/2024
# Updated: 24/09/2024
# Purpose: Define user role wrappers for the admin and contract engineer roles.

from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user, login_required
import logging


def admin_required(f):
    """Wrap with this to ensure current user is logged in and has admin access before calling view."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        try:
            if not current_user.role.upper() == 'ADMIN':
                flash('Admin Role required for access', category='error')
                abort(403)
        except AttributeError as e:
            logging.error(f"Error while checking admin role: {e}")
            flash('An Error has occurred. Please try again.', category='error')
            return redirect(url_for('auth.login'))
        except Exception as e:
            logging.error(f"Error in admin_required decorater: {e}")
            flash('An Error has occurred. Please try again.')
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return decorated_function

def contracteng_required(f):
    """Wrap with this to ensure current user is logged in and has contract engineer access before calling view."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        try:
            if not current_user.role.upper() == 'CONTRACTENG':
                flash('Contract Engineer Role required for access', category='error')
                abort(403)
        except AttributeError as e:
            logging.error(f"Error while checking contract engineer role: {e}")
            flash('An Error has occurred. Please try again.', category='error')
            return redirect(url_for('auth.login'))
        except Exception as e:
            logging.error(f"Error in contracteng_required decorater: {e}")
            flash('An Error has occurred. Please try again.', category='error')
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return decorated_function
