
ral.html.custom = {}

ral.html.custom.attach_fetch = function( id, modal_name, pdata ) {
	$( id ).click( function() {
		var tokens = modal_name.split('.');
		var url = '/' + tokens[0] + '/modals/' + modal_name;
		ral.html.fetch( url, pdata );
	});
}

ral.html.custom.attach_post = function( id, modal_name, pdata ) {
	$( id ).click( function() {
		var tokens = modal_name.split('.');
		var url = '/' + tokens[0] + '/modals/' + modal_name;
		ral.html.post( url, pdata );
	});
}

$(document).ready( function() {

	// Hook call modal classes. Eg usage:
	// 	<button class="raltag_modal_org_new_organization">Hola</button>

	$('*[class*="raltag_modal_"]').click( function() {
		var matches = $(this).attr('class').match( /raltag_modal_(\S+)[\s\$]?/ );
		var modal_name = matches[1].replace( /_/g, '.' );
		var tokens = modal_name.split('.');
		var url = '/' + tokens[0] + '/modals/' + modal_name;
		ral.html.load( url );
	});
});


