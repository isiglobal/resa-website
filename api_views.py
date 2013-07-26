from app import *

# ----------------
# AJAX API GATEWAY
# ----------------

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

	elif request.method == 'PATCH':
		print 'PATCH'
		return 'TODO'
		pass

	elif request.method in ['PUT', 'POST']:
		try:
			article = database.session.query(Article) \
						.filter_by(id=artId).one()

			article.set_from_json(request.json)

			#database.session.add(article)
			database.session.commit()
			return json.dumps(article.serialize())

		except Exception as e:
			print 'exception', e
			return 'FAIL' # TODO FAILURE RESPONSE CODE
		print request.json
		print 'UPDATE'
		return 'TODO'


