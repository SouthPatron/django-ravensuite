
$(function() {
	
	var payment_date = $( "#id_payment_date" ),
		amount = $( "#id_amount" ),
		allFields = $( [] ).add( payment_date ).add( amount ),
		tips = $( ".validateTips" ),
		modalWindow = 0;


	var views = [

		// -------- Dialog Window 1
		{
			open : function( event ) {
				$("#dialog-text").empty().append( $("#dialog-form-one").clone() );
				$("#dialog-text .payment-table-list .payment-line td" ).click( function() {
					$("#dialog-text .payment-table-list .selected-line").removeClass( "selected-line" );
					row = $(this).parent("tr");
					row.addClass( "selected-line" );

					selrefnum = row.find("input.refnum").first().attr("value");
					seltotal = row.find("input.total").first().attr("value");
					selfree = row.find("input.free").first().attr("value");

					$( "#id-payment-refnum" ).attr( "value", selrefnum );
					$( "#id-payment-total" ).attr( "value", seltotal );
					$( "#id-payment-free" ).attr( "value", selfree );
				});
			},

			verify : function() {
				selval = $( "#id-payment-refnum" ).attr( "value" );

				if ( selval < 0 )
				{
					validation.updateTips( tips, "Please select a payment from which you wish to allocate funds." );
					return false;
				}

				return true;
			},
		},

		// -------- Dialog Window 2
		{
			open : function( event ) {
				$( "#dialog-text" ).empty().append( $("#dialog-form-two").clone() );

				$( event.target ).text( "Allocate" );
			},
			verify : function() {
				return true;
			}
		}

	];

	$( "#dialog-form" ).dialog({
		autoOpen: false,
		height: 700,
		width: 600,
		modal: true,

		open : function( event, ui ) {
			views[ modalWindow ].open();
		},

		buttons: {
			"Next": function( event ) {
				var bValid = true;
				allFields.removeClass( "ui-state-error" );

				bValid = views[ modalWindow ].verify();

				if ( bValid ) {
					modalWindow = ( modalWindow + 1 ) % views.length;
					views[ modalWindow ].open( event );
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


//@ sourceURL=componentScript.js


