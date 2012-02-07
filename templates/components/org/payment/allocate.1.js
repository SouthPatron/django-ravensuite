{% load decshift %}

$(function() {
	
	var tips = $( ".validateTips" );

	var	open = function() {
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
	};

	var verify = function() {
		selval = $( "#id-invoice-refnum" ).attr( "value" );

		if ( selval < 0 )
		{
			validation.updateTips( tips, "Please select a payment from which you wish to allocate funds." );
			return false;
		}

		return true;
	};


	$( "#dialog-form" ).dialog({
		autoOpen: false,
		height: 400,
		width: 600,
		modal: true,

		open : function( event, ui ) {
			open();
		},

		buttons: {
			"Next": function( event ) {
				var bValid = true;

				bValid = verify();

				if ( bValid ) {
					$("#dialog-form").find("form").submit();
				}

			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		},
		close: function() {
		}
	});


	$( "#dialog-form" ).dialog( "open" );
});


//@ sourceURL=componentScript.js


