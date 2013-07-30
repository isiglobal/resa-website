
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
			this.$el = $(args.el);
		}

		this.listenTo(this, 'changeMode', this.changeMode);
	},

	initialize: function(args) {
		this._init(args);
		this.render();
	},

	render: function() {
		this.$displayEl.html(this.modelGetDisplayable());
		this.$editEl.html(this.modelGetEditable());
	},
	changeMode: function() {
		console.log('changed mode');
		this.render();
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
		if(this.mode == 'edit') {
			return;
		}
		this.mode = 'edit';
		this.trigger('changeMode');
	},
	enterView: function() {
		if(this.mode == 'view') {
			return;
		}
		this.mode = 'view';
		this.trigger('changeMode');
	},

	save: function() {
		var that = this,
			valMod = this.modelGetEditable(),
			valDom = this.domGetEditable();
	
		if(valMod == valDom) {
			this.enterView();
			return;
		}

		// Sync DOM to model (XXX: Don't bind model:change!)
		this.modelSetEditable(valDom);

		this.model.save({
			// XXX: Backbone is stupid and expects an attrib hash in 
			// order for CBs to fire! (WTF, Backbone?!)
		}, {
			//patch: true,
			success: function(model, resp, opts) {
				that.enterView();
			},
			failure: function(model, xhr, opts) {
				console.log('model.save() error!');
			},
		});
	},
});

