var Article = Backbone.Model.extend({
	urlRoot: '/api/article',
	defaults: {
		id: null,
		datetime_added: null,
		datetime_edited: null,
		title: null,
		url_key: null,
		content_mkdown: null,
		content_html: null,
	},
});

var Articles = Backbone.Collection.extend({
	model: Article,
	url: '/api/article',
});

var Page = Backbone.Model.extend({
	urlRoot: '/api/page',
	defaults: {
		id: null,
		datetime_added: null,
		datetime_edited: null,
		name: null,
		url_key: null,
		content_mkdown: null,
		content_html: null,
	},
});

var Pages = Backbone.Collection.extend({
	model: Page,
	url: '/api/page',
});

