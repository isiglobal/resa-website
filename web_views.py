from app import *

# -------------
# WEBSITE PAGES
# -------------

@app.route('/')
def index():
	return render_template('index.html')

# -------------
# ARTICLE PAGES
# -------------

@app.route('/article', methods=['GET', 'POST', 'PUT'])
def articles():
	if request.method == 'POST' \
	and request.form and len(request.form):

		article = Article(
			title = request.form['title'],
			content_mkdown =request.form['content_mkdown'],
		)

		article.generate_url_key() # TODO: Autogenerate when title dirty
		article.generate_html() # TODO: Not yet implemented

		database.session.add(location)
		database.session.commit()

		return redirect('/article')

	articles = database.session.query(Article).all()
	return render_template('article_list.html', articles=articles)

@app.route('/article/<url_key>')
def article_view(url_key):
	article = None
	try:
		artId = url_key.split('-')[0]
		article = database.session.query(Article) \
					.filter_by(id=artId).one()
	except:
		pass

	return render_template('article.html', article=article)

# ----------
# MISC PAGES
# ----------

@app.route('/purchasing')
def purchasing():
	return render_template('linkout.html', linkName='Purchasing')

@app.route('/temp')
def temp():
	return render_template('temp.html')

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
