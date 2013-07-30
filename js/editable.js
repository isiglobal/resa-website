
var Editable = Backbone.View.extend({
	$displayEl: null,
	$editEl: null,
	model: null,
	editableField: null,
	displayableField: null,
	mode: 'view', // state: view || edit 

	_init: function(args) {
		var that = this,
			import = function(key) {
				if(key in args) {
					that[key] = args[key];
				}
			};

		import('$displayEl');
		import('$editEl');
		import('editableField');
		import('displayableField');

		if('el' in args) {
			console.log('el', args.el);
			this.$el = $(args.el);
		}
	},

	initialize: function(args) {
		this._init(args);
		this.render();
	},

	render: function() {
		this.$displayEl.html(this.modelGetDisplayable());
		this.$editEl.html(this.modelGetEditable());
	},

	// Accessors that abstract away DOM details
	domGetEditable: function() {
		return this.$editEl.val();
	},
	domSetEditable: function(val) {
		this.$editEl.val(val);
	},
	modelGetEditable: function() {
		return this.model.get(this.editableField);
	},
	modelSetEditable: function(val) {
		this.model.set(this.editableField, val);
	},
	modelGetDisplayable: function() {
		return this.model.get(this.displayableField);
	},
	modelSetDisplayable: function(val) {
		this.model.set(this.displayableField, val);
	},

	isChanged: function() {
		return this.domGetEditable() != this.modelGetEditable();
	},

	enterEdit: function() {
		this.mode = 'edit';
	},
	exitEdit: function() {
		this.mode = 'view';
	},

	save: function() {
	},
});

