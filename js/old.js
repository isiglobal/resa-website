var ArticleView = Backbone.View.extend({
	$el: null,
	$title: null,
	$title_edit: null,
	$content: null,
	$content_edit: null,
	events: {
		'click .title_edit_link': 'editTitle',
		'dblclick .title': 'editTitle',
		'click .content_edit_link': 'editContent',
		'dblclick .content': 'editContent',
	},
	initialize: function() {
		this.$el = $('#article');
		this.$title = this.$el.find('.title');
		this.$title_edit = this.$el.find('.title_edit');
		this.$content = this.$el.find('.content');
		this.$content_edit = this.$el.find('.content_edit');

		this.render();

		this.listenTo(this.model, 'change', this.render);
		this.delegateEvents();
	},
	render: function() {
		console.log('render');

		this.$el.find('.title').html(this.model.get('title'));
		this.$el.find('.title_edit').val(this.model.get('title'));

		this.$el.find('.content').html(this.model.get('content_html'));
		this.$el.find('.content_edit').html(this.model.get('content_mkdown'));
	},
	save: function() {
		console.log('SAVE()');
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
		var that = this,
			$textarea = this.$el.find('.content_edit'),
			$content = this.$el.find('.content');

		$content.hide();
		$textarea.show()
			.focus()
			.val($textarea.val())
			.on('blur', function() {
				console.log('blur event');
				that.model.set('content_mkdown', $(this).val());

				// XXX: Backbone is stupid and expects attrib hash for CBs
				that.model.save({
					//title: $(this).val(),
				}, {
					//patch: true,
					success: function(model, resp, opts) {
						console.log('model.save() success!');
						$textarea.hide();
						$content.show();
					},
					failure: function(model, xhr, opts) {
						console.log('model.save() error!');
					},
				});
			});
	},
});

