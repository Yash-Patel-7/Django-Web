# Miscellaneous functions
from modules import *
globals().update(import_modules('home.misc', globals()))


def secret_url():
    return token_urlsafe(100)

