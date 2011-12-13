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
					selfree = row.find("input.free").first().attr("value");
					seldate = row.find("input.date").first().attr("value");

					$( "#id-payment-refnum" ).attr( "value", selrefnum );
					$( "#id-payment-total" ).attr( "value", seltotal );
					$( "#id-payment-free" ).attr( "value", selfree );
					$( "#id-payment-date" ).attr( "value", seldate );
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
				selrefnum = $( "#id-payment-refnum" ).attr( "value" );
				seltotal = $( "#id-payment-total" ).attr( "value" );
				selfree = $( "#id-payment-free" ).attr( "value" );
				seldate = $( "#id-payment-date" ).attr( "value" );

				nam = new Number( selfree.replace( ',', '' ) );

				invout = new Number( "{{ instance.get_amount_outstanding|decshow }}" );

				if ( invout < nam )
					nam = invout;

				$( "#dialog-text #id-text-refnum" ).text( selrefnum );
				$( "#dialog-text #id-text-total" ).text( seltotal );
				$( "#dialog-text #id-text-free" ).text( selfree );
				$( "#dialog-text #id-text-date" ).text( seldate );
				$( "#dialog-text #id-payment-amount" ).attr( "value", nam.toFixed(2) );

				$( event.target ).text( "Allocate" );
			},

			verify : function() {

				selfree = $( "#id-payment-free" ).attr( "value" );

				selfree = selfree.replace( ',', '' );

				if ( isNaN( selfree ) )
				{
					validation.updateTips( tips, "There is an strange error happening. Please take a screenshot and forward it through to us." );
					return false;
				}

				selfree = new Number( selfree );


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

				if ( proposedamount > selfree )
				{
					validation.updateTips( tips, "The amount allocated exceeds the payment's available amount." );
					return false;
				}


				invout = new Number( "{{ instance.get_amount_outstanding|decshow }}" );

				if ( proposedamount > invout )
				{
					validation.updateTips( tips, "The amount allocated exceeds the oustanding amount on the invoice." );
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


