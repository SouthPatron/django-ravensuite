
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

		this.CreditNotes = function( oid, cid ) {
			return '/org/' + oid + '/client/' + cid + '/account/credit-notes';
		};

		this.CreditNote = function( oid, cid, sdid ) {
			return '/org/' + oid + '/client/' + cid + '/account/credit-note/' + sdid;
		};

		this.Invoices = function( oid, cid ) {
			return '/org/' + oid + '/client/' + cid + '/account/invoices';
		};

		this.Invoice = function( oid, cid, sdid ) {
			return '/org/' + oid + '/client/' + cid + '/account/invoice/' + sdid;
		};

		this.Payments = function( oid, cid ) {
			return '/org/' + oid + '/client/' + cid + '/account/payments';
		};

		this.Payment = function( oid, cid, sdid ) {
			return '/org/' + oid + '/client/' + cid + '/account/payment/' + sdid;
		};

		this.PaymentAllocation = function( oid, cid, sdid, alocid ) {
			return '/org/' + oid + '/client/' + cid + '/account/payment/' + sdid + '/allocation/' + alocid;
		};


		this.Component = function( base, name ) {
			return base + '.pc.' + name + '?q=';
		};
	};
};



