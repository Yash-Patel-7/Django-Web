# HTML template context functions
from modules import *
globals().update(import_modules('account.context', globals()))


def dashboard_vars(session_id):
    dashboard_vars = {
        'session_id': session_id,
    }

    return dashboard_vars


def reset_password_vars(url):
    reset_password_vars = {
        'url': url,
    }

    return reset_password_vars


def admin_vars():
    admin_vars = {
        'example': True,
    }

    return admin_vars

