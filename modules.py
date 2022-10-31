# External modules
import sqlite3
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import hashlib
from sqlite3.dbapi2 import DatabaseError
import psycopg2
from urllib.request import urlopen
import time
from json import dumps, loads
from secrets import token_urlsafe, choice
from string import ascii_letters, digits, punctuation
from decimal import Decimal
from urllib.request import HTTPSHandler
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from csp.decorators import csp_exempt
from django.contrib.sessions.backends.db import SessionStore
from importlib import import_module


# Internal modules
def import_modules(avoid, globals):
    internal = [
        'account.context',
        'account.database',
        'account.email',
        'account.misc',
        'home.context',
        'home.database',
        'home.email',
        'home.misc',
    ]
    
    if avoid in internal:
        internal.remove(avoid)

    # Emulates "from module import *"
    for i in internal:
        try:
            mdl = import_module(i)
        except:
            continue

        if "__all__" in mdl.__dict__:
            names = mdl.__dict__["__all__"]
        else:
            names = [x for x in mdl.__dict__ if not x.startswith("_")]
        
        globals.update({k: getattr(mdl, k) for k in names})
    
    return globals

