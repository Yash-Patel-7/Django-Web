# HTML template context functions
from modules import *
globals().update(import_modules('home.context', globals()))


def index_vars():
    index_vars = {
        'example': True,
    }
    
    return index_vars


def TOSAPP_vars():
    TOSAPP_vars = {
        'example': True,
    }

    return TOSAPP_vars


def login_vars():
    login_vars = {
        'example': True,
    }
    
    return login_vars


def OTPP_vars(OTPP_session_id):
    OTPP_vars = {
        'OTPP_session_id': OTPP_session_id,
    }
    
    return OTPP_vars


def notif_verify_email_vars():
    notif_verify_email_vars = {
        'example': True,
    }

    return notif_verify_email_vars


def terms_of_service_vars():
    terms_of_service_vars = {
        'example': True,
    }

    return terms_of_service_vars


def privacy_policy_vars():
    privacy_policy_vars = {
        'example': True,
    }

    return privacy_policy_vars

