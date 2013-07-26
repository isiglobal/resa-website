
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

var ArticleView = Backbone.View.extend({
	$el: null,
	$title: null,
	$title_edit: null,
	$content: null,
	$content_edit: null,
	events: {
		'dblclick .title': 'editTitle',
		'dblclick .content': 'editContent',
	},
	initialize: function() {
		this.$el = $('#article');
		this.$title = this.$el.find('.title');
		this.$title_edit = this.$el.find('.title_edit');
		this.$content = this.$el.find('.content');
		this.$content_edit = this.$el.find('.content_edit');

		this.listenTo(this.model, 'change', this.render);
		this.delegateEvents();
	},
	render: function() {
		console.log('render');
		console.log('render');
		console.log('render');
		this.$el.find('.title').html(this.model.get('title'));
		this.$el.find('.content').html(this.model.get('content_html'));
	},
	save: function() {
		var that = this;
		this.$title_edit.val();
		this.$content_edit.val();
	},
	editTitle: function() {
		var that = this,
			$input = this.$el.find('.title_edit'),
			$title = this.$el.find('.title');

		$title.hide();
		$input.show()
			.focus()
			.val($input.val())
			.on('blur', function() {
				console.log('blur event');
				that.model.set('title', $(this).val());

				// XXX: Backbone is stupid and expects attrib hash for CBs
				that.model.save({
					//title: $(this).val(),
				}, {
					//patch: true,
					success: function(model, resp, opts) {
						console.log('model.save() success!');
						$input.hide();
						$title.show();
					},
					failure: function(model, xhr, opts) {
						console.log('model.save() error!');
					},
				});
			});
	},
	editContent: function() {
		console.log('edit content');
	},
});
