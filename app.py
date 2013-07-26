import os
import sys
import random
import getpass
import hashlib
import datetime
import dateutil
import dateutil.parser
from flask import Flask, render_template, url_for, request
from flask import send_from_directory, send_file, redirect
from flask import json, jsonify
from flask.ext.login import LoginManager, UserMixin
from flask.ext.login import login_user, login_required

# XXX: You must create a non-versioned config file defining
# the following: SECRET_KEY, USERS (list of username/passhash dicts)
import config

import database
from model import *

# -------------
# CONFIGURATION
# -------------

app = Flask(__name__)


app.secret_key = config.SECRET_KEY
#####app.config['USERS'] = config.USERS # TODO ENABLE THESE

""" TODO: ENABLE THESE
login_manager = LoginManager()
login_manager.init_app(app)
"""

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['ENVIRONMENT'] = 'production'

FLASK_PATH = os.path.dirname(os.path.abspath(__file__))

uname = getpass.getuser()

if uname in ['brandon']:
	app.config['ENVIRONMENT'] = 'dev'
elif uname in ['isimobile', 'root']:
	#app.config['ENVIRONMENT'] = 'production'
	pass

