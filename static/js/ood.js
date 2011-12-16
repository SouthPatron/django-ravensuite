
var OOD = new function() {

	this.URL = new function() {

		this.Organizations = function() {
			return '/org/';
		};

		this.Organization = function( oid ) {
			return '/org/' + oid;
		};

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

		this.Invoice = function( oid, cid, iid ) {
			return '/org/' + oid + '/client/' + cid + '/account/invoice/' + iid;
		};

		this.Payment = function( oid, cid, payid ) {
			return '/org/' + oid + '/client/' + cid + '/account/payment/' + payid;
		};

		this.Component = function( base, name ) {
			return base + '.pc.' + name + '?q=';
		};
	};
};



