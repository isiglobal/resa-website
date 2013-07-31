#!/usr/bin/env python

"""
West GA Resa Website
Copyright 2013 Brandon Thomas <bt@brand.io>

	+ requires +
		flask
		flask-login
		markdown
"""

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
from werkzeug.exceptions import HTTPException, NotFound

# ----------------
# APPLICATION CODE
# ----------------

from app import *
from web_views import *
from api_views import *

# --------------
# EVENT HANDLERS 
# --------------

@app.errorhandler(404)
@app.route('/404')
def error_404(e=None):
	if e:
		return render_template('404.html'), 404
	return render_template('404.html')

#####@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

#####@login_manager.user_loader
def load_user(userid):
	return User()

class User(UserMixin):
	def __init__(self):
		pass
	def get_id(self):
		return 1
	def is_active(self):
		return True
	def is_authenticated(self):
		return True

# -----------------
# DEVELOPMENT TOOLS
# -----------------

def is_dev():
	return (app.config['ENVIRONMENT'] == 'dev')

def cache_buster():
	if not app.config['ENVIRONMENT'] or app.config['ENVIRONMENT'] != 'dev':
		return ''
	return '?%s' % str(random.randint(500, 9000000))

def format_datetime(dateStr, fmt=None):
	if not dateStr:
		return 'No date'
	dateStr = str(dateStr) # FIXME: Already a date object?
	date = dateutil.parser.parse(dateStr)
	if not fmt:
		fmt = '%b %d, %H:%M'
	return date.strftime(fmt)

def js_escape_string(string, squo=True):
	s = ''
	try:
		s = '\\n'.join(string.split('\n'))
		if squo:
			s = s.replace('\'', '\\\'')
		else:
			s = s.replace('\"', '\\\"')

	except:
		s = ''
	return s

app.jinja_env.globals.update(is_dev=is_dev)
app.jinja_env.globals.update(cache_buster=cache_buster)
app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['use_in_js'] = js_escape_string

def main(port=5000):
	app.run(
		port = port,
		host = '0.0.0.0',
		use_reloader = True,
		debug = is_dev(),
	)

if __name__ == '__main__':
	port = 5000 if len(sys.argv) < 2 else int(sys.argv[1])
	main(port=port)

