

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

