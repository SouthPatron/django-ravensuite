
$(function() {
	
	var trading_name = $( "#id_trading_name" ),
		allFields = $( [] ).add( trading_name ),
		tips = $( ".validateTips" );

	$( "#dialog-form" ).dialog({
		autoOpen: false,
		height: 400,
		width: 550,
		modal: true,
		buttons: {
			"Add a new Client": function() {
				var bValid = true;
				allFields.removeClass( "ui-state-error" );

				bValid = bValid && validation.length( tips, trading_name, "Trading Name", 3, 192 );

				if ( bValid ) {
					$( "#create-new-form" ).submit();
				}
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



