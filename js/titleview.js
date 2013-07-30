
// FIXME: Filename is inaccurate

var EditableContentView = Editable.extend({

	events: {
		'click .content_edit_link': 'enterEdit',
		'dblclick .content': 'enterEdit',
		'blur .content_edit': 'save',
	},

	initialize: function(args) {
		this._init(args);

		this.$displayEl = this.$el.find('.content');
		this.$editEl = this.$el.find('.content_edit');

		this.delegateEvents();

		this.render();
	},

	render: function() {
		console.log('render');
		
		this.$displayEl.html(this.modelGetDisplayable());
		this.$editEl.html(this.modelGetEditable());

		switch(this.mode) {
			case 'edit':
				this.$displayEl.hide();
				this.$editEl.show();
				break;

			case 'view':
			default:
				this.$editEl.hide();
				this.$displayEl.show();
				break;
		}
	},
});

