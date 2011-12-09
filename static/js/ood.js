
var OOD = new function() {

	this.URL = new function() {


		this.Clients = function( oid ) {
			return '/org/' + oid + '/clients';
		};

		this.Client = function( oid, cid ) {
			return '/org/' + oid + '/client/' + cid;
		};

		this.Account = function( oid, cid ) {
			return '/org/' + oid + '/client/' + cid + '/account';
		};

		this.Invoices = function( oid, cid ) {
			return '/org/' + oid + '/client/' + cid + '/account/invoices';
		};

		this.Component = function( base, name ) {
			return base + '.pc.' + name;
		};
	};
};


