#!/usr/bin/env python

"""
West GA Resa Website
Copyright 2013 Brandon Thomas <bt@brand.io>
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

""" TODO: ENABLE THESE
# XXX: You must create a non-versioned config file defining
# the following: SECRET_KEY, USERS (list of username/passhash dicts)
import config

import database
from model import *
"""

# -------------
# CONFIGURATION
# -------------

app = Flask(__name__)

""" TODO: ENABLE THESE
app.secret_key = config.SECRET_KEY
app.config['USERS'] = config.USERS

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

# -------------
# WEBSITE PAGES
# -------------

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		user = request.form['user']
		hsh = hashlib.sha1(request.form['pass']).hexdigest()
		authenticated = False
		error = 'Wrong username/password.'

		for u in app.config['USERS']:
			if user != u['username']:
				continue
			if hsh == u['passhash']:
				authenticated = True
				break

		if authenticated:
			login_user(User(), remember=False)
			return redirect('/locations')

	return render_template('login.html', error=error)

@app.route('/locations', methods=['GET', 'POST'])
#####@login_required
def locations():
	location = None
	if request.form and len(request.form):

		location = Location(
			position_x = request.form['position_x'],
			position_y = request.form['position_y'],
			name = request.form['name'],
			email = request.form['email'],
			phone = request.form['phone'],
			school = request.form['school'],
		)

		database.session.add(location)
		database.session.commit()

		return redirect('/locations')

	locations = database.session.query(Location).all()
	return render_template('location_overview.html',
			locations=locations)


@app.route('/location/<int:locId>',
			methods=['GET', 'UPDATE', 'DELETE'])
#####@login_required
def location(locId):
	location = None
	try:
		location = database.session.query(Location) \
						.filter_by(id=locId) \
						.one()
	except:
		return 'ERROR'

	if request.method == 'DELETE':
		database.session.delete(location)
		database.session.commit()
		return 'DELETED'

	elif request.method == 'UPDATE':
		return 'TODO'

	#return render_template('location_show.html', location=location)
	return 'TODO'

# ----------------
# AJAX API GATEWAY
# ----------------

@app.route('/api/locations', methods=['GET', 'POST'])
def page_location_list():
	if request.method == 'POST':
		location = Location(
			position_x = request.json['position_x'],
			position_y = request.json['position_y'],
			name = request.json['name'],
			email = request.json['email'],
			phone = request.json['phone'],
			school = request.json['school'],
		)

		database.session.add(location)
		database.session.commit()

		return 'OK' # TODO: status msg.

	else:
		locations = None
		try:
			locations = database.session.query(Location).all()
		except:
			pass

		if not len(locations):
			return '{}'

		return json.dumps([x.serialize() for x in locations])

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
	if not app.config['ENVIRONMENT_DEV']:
		return ''
	return '?%s' % str(random.randint(500, 9000000))

def format_datetime(dateStr, fmt=None):
	dateStr = str(dateStr) # FIXME: Already a date object?
	date = dateutil.parser.parse(dateStr)
	if not fmt:
		fmt = '%b %d, %H:%M'
	return date.strftime(fmt)

app.jinja_env.globals.update(is_dev=is_dev)
app.jinja_env.globals.update(cache_buster=cache_buster)
app.jinja_env.filters['datetime'] = format_datetime

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

