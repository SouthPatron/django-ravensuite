
$(function() {
	
	var payment_date = $( "#id_payment_date" ),
		amount = $( "#id_amount" ),
		allFields = $( [] ).add( payment_date ).add( amount ),
		tips = $( ".validateTips" );

	$( "#dialog-form" ).dialog({
		autoOpen: false,
		height: 700,
		width: 600,
		modal: true,
		buttons: {
			"Finished": function() {
				var bValid = true;
				allFields.removeClass( "ui-state-error" );

				// bValid = bValid && validation.length( tips, trading_name, "Trading Name", 3, 192 );

				if ( bValid ) {
					$( "#allocate-new-form" ).submit();
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

