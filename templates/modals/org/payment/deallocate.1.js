$(function() {
	
	var 
		allFields = $( [] ),
		tips = $( ".validateTips" );

	$( "#dialog-form" ).dialog({
		autoOpen: false,
		height: 400,
		width: 600,
		modal: true,

		buttons: {
			"Deallocate": function( event ) {
				$( "#deallocate-payment-form" ).submit();
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		},
		close: function() {
			allFields.val( "" ).removeClass( "ui-state-error" );
		}
	});


	$( "#dialog-form" ).dialog( "open" );
});


//@ sourceURL=componentScript.js


