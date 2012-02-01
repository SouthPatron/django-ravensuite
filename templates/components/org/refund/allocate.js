{% load decshift %}
{% load sourcedoc %}
{% get_document_obj instance as doc %}

$(function() {
	
	var refund_date = $( "#id_refund_date" ),
		amount = $( "#id_amount" ),
		allFields = $( [] ).add( refund_date ).add( amount ),
		tips = $( ".validateTips" ),
		modalWindow = 0;


	var views = [

		// -------- Dialog Window 1
		{
			open : function( event ) {
				$("#dialog-text").empty().append( $("#dialog-form-one").clone() );
				$("#dialog-text .refund-table-list .refund-line td" ).click( function() {
					$("#dialog-text .refund-table-list .selected-line").removeClass( "selected-line" );
					row = $(this).parent("tr");
					row.addClass( "selected-line" );

					selrefnum = row.find("input.refnum").first().attr("value");
					seltotal = row.find("input.total").first().attr("value");
					selavailable = row.find("input.available").first().attr("value");
					selavfdate = row.find("input.avf-date").first().attr("value");

					$( "#id-avf-refnum" ).attr( "value", selrefnum );
					$( "#id-avf-total" ).attr( "value", seltotal );
					$( "#id-avf-available" ).attr( "value", selavailable );
					$( "#id-avf-avf-date" ).attr( "value", selavfdate );
				});
			},

			verify : function() {
				selval = $( "#id-avf-refnum" ).attr( "value" );

				if ( selval < 0 )
				{
					validation.updateTips( tips, "Please select a refund from which you wish to allocate funds." );
					return false;
				}

				return true;
			},
		},

		// -------- Dialog Window 2
		{
			open : function( event ) {
				$( "#dialog-text" ).empty().append( $("#dialog-form-two").clone() );
				selrefnum = $( "#id-avf-refnum" ).attr( "value" );
				seltotal = $( "#id-avf-total" ).attr( "value" );
				selavailable = $( "#id-avf-available" ).attr( "value" );
				selavfdate = $( "#id-avf-avf-date" ).attr( "value" );

				nam = new Number( selavailable.replace( ',', '' ) );

				avail = new Number( "{{ doc.getTotals.getUnallocated|decshow }}" );

				if ( avail < nam )
					nam = avail;

				$( "#dialog-text #id-text-refnum" ).text( selrefnum );
				$( "#dialog-text #id-text-date" ).text( selavfdate );
				$( "#dialog-text #id-text-total" ).text( seltotal );
				$( "#dialog-text #id-text-unallocated" ).text( selavailable );

				$( "#dialog-text #id-amount" ).attr( "value", nam.toFixed(2) );

				$( event.target ).text( "Allocate" );
			},

			verify : function() {

				selavailable = $( "#id-avf-available" ).attr( "value" );
				selavailable = selavailable.replace( ',', '' );

				if ( isNaN( selavailable ) )
				{
					validation.updateTips( tips, "There is an strange error happening. Please take a screenshot and forward it through to us." );
					return false;
				}

				selavailable = new Number( selavailable );

				proposedamount = $( "#dialog-text #id-amount" ).attr( "value" );

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

				if ( proposedamount > selavailable )
				{
					validation.updateTips( tips, "The amount allocated exceeds the source's outstanding amount." );
					return false;
				}


				invout = new Number( "{{ doc.getTotals.getUnallocated|decshow }}" );

				if ( proposedamount > invout )
				{
					validation.updateTips( tips, "The amount allocated exceeds the refund amount free." );
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


