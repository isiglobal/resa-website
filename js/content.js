
var EditableView = Editable.extend({

	events: {
		'click .edit_link': 'editLink',
		'dblclick .display': 'enterEdit',
		'blur .editable': 'save',
	},

	initialize: function(args) {
		this._init(args);

		this.$displayEl = this.$el.find('.display');
		this.$editEl = this.$el.find('.edit');
		this.$linkEl = this.$el.find('.edit_link');

		this.delegateEvents();

		this.editType = 'textarea';
		if(this.$editEl.prop('tagName') == 'INPUT') {
			this.editType = 'input';
		}

		this.render();
	},

	render: function() {
		this.$displayEl.html(this.modelGetDisplayable());

		if(this.editType == 'input') {
			this.$editEl.val(this.modelGetEditable());
		}
		else {
			this.$editEl.html(this.modelGetEditable());
		}

		switch(this.mode) {
			case 'edit':
				this.$displayEl.hide();
				this.$editEl.show();
				this.$linkEl.html('save ' + this.title); // next action
				break;

			case 'view':
			default:
				this.$editEl.hide();
				this.$displayEl.show();
				this.$linkEl.html('edit ' + this.title); // next action
				break;
		}
	},

	editLink: function() {
		switch(this.mode) {
			case 'edit':
				this.save();
				break;
			case 'view':
			default:
				this.enterEdit();
				break;
		}
	},
});

