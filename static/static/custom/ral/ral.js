
ral.html.custom = {}

ral.html.custom.attach_fetch = function( id, modal_name, pdata ) {
	jQuery( id ).click( function() {
		var url = '/modals/' + modal_name;
		ral.html.fetch( url, pdata );
	});
}

ral.html.custom.attach_post = function( id, modal_name, pdata ) {
	jQuery( id ).click( function() {
		var url = '/modals/' + modal_name;
		ral.html.post( url, pdata );
	});
}



