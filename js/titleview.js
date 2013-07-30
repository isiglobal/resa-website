

var EditableContentView = Editable.extend({

	events: {
		'click .content_edit_link': 'editContent',
		'dblclick .content': 'editContent',
	},

	initialize: function(args) {
		this._init(args);
		console.log('$el', this.$el);

		this.$displayEl = this.$el.find('.content');
		this.$editEl = this.$el.find('.content_edit');

		this.listenTo(this.model, 'change', this.render);
		this.delegateEvents();

		this.render();

	},

	render: function() {
		console.log('render');

		this.$displayEl.html(this.modelGetDisplayable());
		this.$editEl.html(this.modelGetEditable());
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

var EditableTextarea = Editable.extend({
	// Accessors that abstract away DOM details
	domGetEditable: function() {
		return this.$editEl.val();
	},
	domSetEditable: function(val) {
		this.$editEl.val(val);
	}
});

