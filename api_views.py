from app import *

# ----------------
# AJAX API GATEWAY
# ----------------

@app.route('/api/article/<url_key>',
		methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def api_article(url_key):
	artId = url_key.split('-')[0] # TODO: Not safe. Error prone
	article = None

	if request.method == 'GET':
		try:
			article = database.session.query(Article) \
						.filter_by(id=artId).one()
		except:
			pass
		return json.dumps(article.serialize())

	elif request.method in ['PUT', 'POST', 'PATCH']:
		try:
			article = database.session.query(Article) \
						.filter_by(id=artId).one()
			article.set_from_json(request.json)
			database.session.commit()

		except Exception as e:
			print 'exception', e
			return 'FAIL' # TODO FAILURE RESPONSE CODE

		return json.dumps(article.serialize())

@app.route('/api/page/<pid>',
		methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def api_page(pid):
	#pageId = url_key.split('-')[0] # TODO: Not safe. Error prone
	page = None

	if request.method == 'GET':
		try:
			page = database.session.query(Page) \
						.filter_by(id=pid).one()
		except:
			pass
		return json.dumps(page.serialize())

	elif request.method in ['PUT', 'POST', 'PATCH']:
		try:
			page = database.session.query(Page) \
						.filter_by(id=pid).one()
			page.set_from_json(request.json)
			database.session.commit()

		except Exception as e:
			print 'exception', e
			return 'FAIL' # TODO FAILURE RESPONSE CODE

		return json.dumps(page.serialize())



# TODO: THIS IS DEPRECATED, I THINK
# TODO: THIS IS DEPRECATED, I THINK
# TODO: THIS IS DEPRECATED, I THINK
# TODO: THIS IS DEPRECATED, I THINK
@app.route('/api/articles', methods=['GET', 'POST', 'PATCH', 'PUT'])
def api_articles():
	if request.method == 'POST':
		article = Article(
			title = request.json['title'],
			content_mkdown =request.json['content_mkdown'],
		)

		article.generate_url_key() # TODO: Autogenerate when title dirty
		article.generate_html() # TODO: Not yet implemented

		database.session.add(article)
		database.session.commit()

		return 'OK' # TODO: status msg.

	else:
		articles = None
		try:
			articles = database.session.query(Article).all()
		except:
			pass

		if not len(locations):
			return '{}'

		return json.dumps([x.serialize() for x in articles])

