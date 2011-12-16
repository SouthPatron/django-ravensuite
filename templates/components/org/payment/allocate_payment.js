{% load decshift %}

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
					selunpaid = row.find("input.unpaid").first().attr("value");
					selinvoicedate = row.find("input.invoice-date").first().attr("value");
					selduedate = row.find("input.due-date").first().attr("value");

					$( "#id-invoice-refnum" ).attr( "value", selrefnum );
					$( "#id-invoice-total" ).attr( "value", seltotal );
					$( "#id-invoice-unpaid" ).attr( "value", selunpaid );
					$( "#id-invoice-invoice-date" ).attr( "value", selinvoicedate );
					$( "#id-invoice-due-date" ).attr( "value", selduedate );
				});
			},

			verify : function() {
				selval = $( "#id-invoice-refnum" ).attr( "value" );

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
				selrefnum = $( "#id-invoice-refnum" ).attr( "value" );
				seltotal = $( "#id-invoice-total" ).attr( "value" );
				selunpaid = $( "#id-invoice-unpaid" ).attr( "value" );
				selinvoicedate = $( "#id-invoice-invoice-date" ).attr( "value" );
				selduedate = $( "#id-invoice-due-date" ).attr( "value" );

				nam = new Number( selunpaid.replace( ',', '' ) );

				invout = new Number( selunpaid );

				if ( invout < nam )
					nam = invout;

				$( "#dialog-text #id-text-refnum" ).text( selrefnum );
				$( "#dialog-text #id-text-total" ).text( seltotal );
				$( "#dialog-text #id-text-unpaid" ).text( selunpaid );
				$( "#dialog-text #id-text-due-date" ).text( selduedate );
				$( "#dialog-text #id-text-invoice-date" ).text( selinvoicedate );
				$( "#dialog-text #id-payment-amount" ).attr( "value", nam.toFixed(2) );

				$( event.target ).text( "Allocate" );
			},

			verify : function() {

				selunpaid = $( "#id-invoice-unpaid" ).attr( "value" );
				selunpaid = selunpaid.replace( ',', '' );

				if ( isNaN( selunpaid ) )
				{
					validation.updateTips( tips, "There is an strange error happening. Please take a screenshot and forward it through to us." );
					return false;
				}

				selunpaid = new Number( selunpaid );

				proposedamount = $( "#dialog-text #id-payment-amount" ).attr( "value" );

				if ( isNaN( proposedamount ) )
				{
					validation.updateTips( tips, "The number you have entered appears to be invalid. Please try again." );
					return false;
				}

				proposedamount = new Number( proposedamount );

				if ( proposedamount <= 0 )
				{
					validation.updateTips( tips, "You need to allocated an amount larger than zero." );
					return false;
				}

				if ( proposedamount > selunpaid )
				{
					validation.updateTips( tips, "The amount allocated exceeds the invoice's outstanding amount." );
					return false;
				}


				invout = new Number( "{{ instance.get_amount_free|decshow }}" );

				if ( proposedamount > invout )
				{
					validation.updateTips( tips, "The amount allocated exceeds the payment amount free." );
					return false;
				}

				return true;
			}
		},

		// -------- Dialog Window 3
		{
			open : function( event ) {
				$( "#allocate-new-form" ).submit();
			},

			verify : function() {
				return true;
			}
		}



	];

	$( "#dialog-form" ).dialog({
		autoOpen: false,
		height: 400,
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


