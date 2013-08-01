from app import *
from werkzeug.exceptions import HTTPException, NotFound

# -------------------
# MISC WEBSITE PAGES
# -------------------

@app.route('/')
def index():
	try:
		page = database.session.query(Page) \
					.filter_by(url_key='index').one()
		return render_template('index.html', page=page)
	except:
		pass

	return render_template('index.html')


@app.route('/address')
def address():
	return render_template('address.html')


# ---------------
# ARTICLE SYSTEM
# ---------------

@app.route('/article', methods=['GET', 'POST', 'PUT'])
def articles():
	articles = None
	print 'view entered'

	try:
		if request.method == 'POST' \
		and request.form and len(request.form):

			article = Article(
				title = request.form['title'],
				content_mkdown =request.form['content_mkdown'],
			)

			article.generate_url_key() # TODO: Autogenerate when dirty
			article.generate_html() # TODO: Not yet implemented

			database.session.add(article)
			database.session.commit()

			return redirect('/article')

		articles = database.session.query(Article).all()

	except Exception as e:
		print 'exception', e
		raise e

	print 'articles queried...'
	print articles

	return render_template('article_list.html', articles=articles)

@app.route('/article_new', methods=['GET', 'POST', 'PUT'])
def article_new():
	if request.method == 'POST' \
	and request.form and len(request.form):

		article = Article(
			title = request.form['title'],
			content_mkdown =request.form['content_mkdown'],
		)

		article.generate_url_key() # TODO: Autogenerate when title dirty
		article.generate_html() # TODO: Not yet implemented

		database.session.add(article)
		database.session.commit()

		return redirect('/article')

	return render_template('article_new.html')


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


# ------------
# PAGE SYSTEM 
# ------------

@app.route('/page/list', methods=['GET', 'POST', 'PUT'])
def pages():
	if request.method == 'POST' \
	and request.form and len(request.form):

		page = Page(
			name = request.form['name'],
			content_mkdown =request.form['content_mkdown'],
		)

		page.generate_url_key() # TODO: Autogenerate when title dirty
		page.generate_html() # TODO: Not yet implemented

		database.session.add(page)
		database.session.commit()

		return redirect('/page/list')

	pages = database.session.query(Page).all()
	return render_template('pages/list.html', pages=pages)

@app.route('/page/new', methods=['GET', 'POST', 'PUT'])
def page_new():
	if request.method == 'POST' \
	and request.form and len(request.form):

		page = Page(
			name = request.form['name'],
			content_mkdown =request.form['content_mkdown'],
		)

		page.generate_url_key() # TODO: Autogenerate when title dirty
		page.generate_html() # TODO: Not yet implemented

		database.session.add(page)
		database.session.commit()

		return redirect('/page/list')

	return render_template('pages/create.html')


@app.route('/page/<url_key>')
def page_view(url_key):
	page = None
	try:
		#pageId = url_key.split('-')[0]
		pageId = url_key
		page = database.session.query(Page) \
					.filter_by(url_key=pageId).one()
	except:
		raise NotFound

	return render_template('pages/view.html', page=page)

@app.route('/page/edit/<url_key>')
def page_edit(url_key):
	page = None
	try:
		#pageId = url_key.split('-')[0]
		pageId = url_key
		page = database.session.query(Page) \
					.filter_by(url_key=pageId).one()
	except:
		raise NotFound

	return render_template('pages/edit.html', page=page)


# ---------------
# AUTHENTICATION 
# ---------------

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


