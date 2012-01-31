{% load decshift %}
{% load sourcedoc %}
{% get_document_obj instance as doc %}

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
				$( "#dialog-text" ).empty().append( $("#dialog-form-one").clone() );

				$( "#dialog-text #id-chosen-date" ).attr( 'value', Date.today().toString( 'dd MMM yyyy' ) );
			},

			verify : function() {

				var thedate = $( "#dialog-text #id-chosen-date" ).val();

				thedate = Date.parse( thedate ).toString( 'dd MMM yyyy' );

				var orig = $( "#dialog-text #id-chosen-amount" ).val();
				var refa = orig.replace( ',', '' );

				if ( isNaN( refa ) )
				{
					validation.updateTips( tips, "The amount you wish to refund is not valid." );
					return false;
				}

				refa = (new Number( refa )) * 100;

				if ( refa <= 0 )
				{
					validation.updateTips( tips, "You need to refund an amount larger than zero." );
					return false;
				}

				if ( refa > ((new Number( "{{ doc.getTotals.getUnallocated }}" ))))
				{
					validation.updateTips( tips, "The amount entered exceeds the amount available to refund." );
					return false;
				}

				$( "#id-refund-amount" ).val( orig );
				$( "#id-refund-date" ).val( thedate );

				return true;
			},
		},

		// -------- Dialog Window 2
		{
			open : function( event ) {
				$( "#dialog-text" ).empty().append( $("#dialog-form-two").clone() );
			},

			verify : function() {
				return true;
			}
		},

		// -------- Dialog Window 3
		{
			open : function( event ) {
				$( "#refund-form" ).submit();
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


