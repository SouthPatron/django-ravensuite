
var OOD = new function() {

	this.URL = new function() {

		this.Client = function( oid, cid ) {
			return '/org/' + oid + '/client/' + cid;
		};

		this.Account = function( oid, cid ) {
			return '/org/' + oid + '/client/' + cid + '/account';
		};

		this.Component = function( base, name ) {
			return base + '.pc.' + name;
		};
	};
};



