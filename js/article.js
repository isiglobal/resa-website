
var Article = Backbone.Model.extend({
	urlRoot: '/api/articles',
	defaults: {
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
	url: '/api/articles',
});

