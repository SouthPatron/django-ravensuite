

(function( $ ){

var settings = {
		'delete-icon' : '',
		'editable' : true
	};


var datesettings = {
		dateFormat: 'd M yy',
		onClose: function( theDate ) {
			requested_date = Date.parse( theDate );
			if ( requested_date != null )
				$(this).val( $.datepicker.formatDate( 'd M yy', requested_date ) );
			else
				$(this).val( $.datepicker.formatDate( 'd M yy', Date.today() ) );
		}
	};



function apply_edit_hooks() {
	$('.itol .item-list .item-description').one( 'click', { 'name' : 'description' }, start_field_edit );
	$('.itol .item-list .item-qty').one( 'click', { 'name' : 'units' }, start_numerical_edit );
	$('.itol .item-list .item-unit-price').one( 'click', { 'name' : 'perunit' }, start_numerical_edit );
	$('.itol .item-list .item-tax-rate').one( 'click', start_tax_edit );

	$('.itol .item-list table .item-delete-link').click( function() {
		$(this).parents( "tr" ).remove();
		update_totals();
	});
};


function add_item_line()
{
	if ( settings[ 'editable' ] == false )
		return;

	$('.itol .item-list table tbody').append( '	\
			<tr>	\
				<td class="item-description">&nbsp;<input type="hidden" name="description" value="" /></td>	\
				<td class="item-qty">&nbsp;<input type="hidden" name="units" value="" /></td>	\
				<td class="item-unit-price">&nbsp;<input type="hidden" name="perunit" value="" /></td>	\
				<td class="item-tax-rate">&nbsp;<input type="hidden" name="tax_rate" value="" /></td>	\
				<td class="item-amount"><span>&nbsp;</span><input type="hidden" name="amount" value="" /></td>	\
				<td class="item-delete"><img class="item-delete-link" src="' + settings[ 'delete-icon' ] + '" /></td>	\
			</tr>	\
		'
	);

	apply_edit_hooks();
}



function update_totals() {

	// Columns:
	//		0 - qty
	//		1 - unit price
	//		2 - tax option
	//		3 - amount
	//		4 - tax
	//		5 - total

	values = [];

	$(".itol .item-list tbody tr").each( function() {

		my_value = [];

		my_value[0] = $(this).find( ".item-qty input" ).attr( "value" );
		my_value[1] = $(this).find( ".item-unit-price input" ).attr( "value" );
		my_value[2] = $(this).find( ".item-tax-rate input" ).attr( "value" );

		if ( (isNaN( my_value[0] )) || (isNaN( my_value[1])) || ((my_value[2] ==undefined) || (my_value[2].length <= 0)) )
			return;

		my_value[5] = ((new Number( my_value[0] )) * (new Number( my_value[1] )) );

		rate = ( new Number( "0.14" ) );

		if ( my_value[2] == 'Tax Inclusive' )
		{
			my_value[3] = (new Number(my_value[5] / (rate + 1))).toFixed(2);
			my_value[4] = (new Number(my_value[5])) - (new Number(my_value[3]));
		}
		else
		{
			if ( my_value[2] == 'Tax Exclusive' )
			{
				my_value[3] = my_value[5];
				my_value[4] = (new Number(my_value[3] * rate)).toFixed(2);
				my_value[5] = ((new Number(my_value[3])) + (new Number(my_value[4])));
			}
			else
			{
				my_value[3] = my_value[5];
				my_value[4] = 0;
			}
		}
		values.push( my_value );
	});

	total_amount = new Number( 0 );
	total_tax = new Number( 0 );
	total_total = new Number( 0 );

	for ( var i = 0; i < values.length; i++ )
	{
		total_amount += (new Number(values[i][3]));
		total_tax += (new Number(values[i][4]));
		total_total += (new Number(values[i][5]));
	}


	$( "#summary_amount" ).empty().append( total_amount.toFixed(2) );
	$( "#summary_tax" ).empty().append( total_tax.toFixed(2) );
	$( "#summary_total" ).empty().append( total_total.toFixed(2) );

	$( "#id_itol_amount" ).val( total_amount.toFixed(2) );
	$( "#id_itol_tax" ).val( total_tax.toFixed(2) );
	$( "#id_itol_total" ).val( total_total.toFixed(2) );
}


function end_numerical_edit( event ) {
	oldVal = $(this).val();

	if ( (isNaN( oldVal )) || (oldVal < 0) )
	{
		oldVal = event.data[ 'original_value' ];
		if ( isNaN( oldVal ) ) oldVal = 0;
	}

	
	oldVal = (new Number( oldVal )).toFixed(2);

	par = $(this).parent( 'td' );
	par.empty();
	par.append('<span>'+oldVal+'</span><input type="hidden" name="' + event.data[ 'name' ] + '" value="' + oldVal + '" />');

	row = $(par).parent( "tr" );

	qty = $(row).find( ".item-qty input" ).val();
	price = $(row).find( ".item-unit-price input" ).val();

	if ( (isNaN( qty ) || isNaN( price )) == false )
	{
		amount = (new Number(qty * price)).toFixed(2);
		$(row).find( ".item-amount span" ).empty().append( amount );
		$(row).find( ".item-amount input" ).attr( 'value', amount );
	}

	update_totals();

	par.one( 'click', event.data, start_numerical_edit );
}

function start_numerical_edit( event ) {
	oldVal = $(this).find( 'input' ).attr( 'value' );
	$(this).empty();
	$(this).append('<input type="text" name="' + event.data[ 'name' ] + '" value="' + (new Number(oldVal)).toFixed(2) + '" />' );

	event.data[ 'original_value' ] = oldVal; 

	$(this).find( 'input' ).focus();
	$(this).find( 'input' ).focusout(
			event.data,
			end_numerical_edit
		);

	original_td = $(this);
	$(this).find( 'input' ).keydown( event.data, function(event) {
			if ( event.keyCode == '13') {
				event.preventDefault();
				$(this).focusout();
			}
			if ( event.keyCode == '9') {
				event.preventDefault();
				$(this).focusout();
				$(original_td).next( "td" ).click();
			}
			if ( event.keyCode == '27') {
				event.preventDefault();
				$(this).val( oldVal );
				$(this).focusout();
			}
		});
}



function end_field_edit( event ) {
	oldVal = $(this).val();
	par = $(this).parent( 'td' );
	par.empty();
	par.append('<span>'+oldVal+'</span><input type="hidden" name="' + event.data[ 'name' ] + '" value="' + oldVal + '" />');
	par.one( 'click', event.data, start_field_edit );
}

function start_field_edit( event ) {
	oldVal = $(this).find( 'input' ).attr( 'value' );
	$(this).empty();
	$(this).append('<input type="text" name="'+event.data['name'] + '" value="' + oldVal + '" />' );
	original_td = $(this);

	$(this).find( 'input' ).focus().focusout( event.data, end_field_edit ).keydown( event.data,  function(event) {
			if ( event.keyCode == '13') {
				event.preventDefault();
				$(this).focusout();
			}
			if ( event.keyCode == '9') {
				event.preventDefault();
				$(this).focusout();
				$(original_td).next( "td" ).click();
			}
			if ( event.keyCode == '27') {
				event.preventDefault();
				$(this).val( oldVal );
				$(this).focusout();
			}
		});
}


function end_tax_edit( event ) {
	oldVal = $(this).val();
	par = $(this).parent( 'td' );
	par.empty();
	par.append('<span>'+oldVal+'</span><input type="hidden" name="tax_rate" value="' + oldVal + '" />');

	update_totals();

	par.one( 'click', start_tax_edit );
}

function start_tax_edit( event ) {
	oldVal = $(this).find( 'input' ).attr( 'value' );

	if ( (oldVal == undefined) || (oldVal.length <= 0) )
	{
		oldVal = $("#id_default_tax").val();
	}

	$(this).empty();

	tax_brackets = [
		'No Tax',
		'Tax Inclusive',
		'Tax Exclusive',
		'Tax Exempt'
	];

	replacement = '<select name="tax_rate">';
	for ( var rate in tax_brackets )
	{
		level = tax_brackets[ rate ];

		replacement += '<option value="{0}" {1}>{0}</option>'.format( level, ((level==oldVal)?"SELECTED=\"1\" ":"") );
	}
	replacement += '</select>';

	$(this).append( replacement );

	original_td = $(this);

	$(this).find( 'select' ).focus().focusout( end_tax_edit ).change( end_tax_edit ).keydown( function(event) {

			if ( event.keyCode == '13') {
				event.preventDefault();
				$(this).focusout();
			}

			if ( event.keyCode == '9') {
				event.preventDefault();
				$(this).focusout();
				doug = $(original_td).parent("tr").next("tr");

				if ( doug.length == 0)
				{
					add_item_line();
					doug = $(original_td).parent("tr").next("tr");
				}
				
				$(doug).find(".item-description").first().click();
			}

			if ( event.keyCode == '27') {
				event.preventDefault();
				$(this).val( oldVal );
				$(this).focusout();
			}

		});

}


function itol_submit( event ) {
	if ( event.data && event.data[ 'new_state' ] )
		$("#id_itol_state").val( event.data[ 'new_state' ] );
	$("#id_itol_form").submit();
}


var methods = {
	init : function( options ) {
		if ( options ) {
			$.extend( settings, options );
		}

		return this;
	},

	prepare : function() {

		$('#id_itol_date').datepicker( datesettings );
		$('#id_due_date').datepicker( datesettings );

		if ( settings[ 'editable' ] == true )
		{
		}

		$("#id_button_save").click( itol_submit );
		$("#id_button_delete").click( { 'new_state' : 99 }, itol_submit );
		$("#id_button_approve").click( { 'new_state' : 5 }, itol_submit );
		$("#id_button_void").click( { 'new_state' : 10 }, itol_submit );

		return this;
	},

	allowEdit : function() {
		apply_edit_hooks();
		$('#id_itol_add_item_row').click( add_item_line );
		return this;
	},

	setColumns : function() {
		// Title
		// Name
		// Type
		// Editable
		// Next
	},

	addDate : function( itid ) {
		$( itid ).datepicker( datesettings );
		return this;
	},

/*
 * behaviour
 *		next - string or function
 *
 * hooks
 *		onFocus( event, value )
 *		onChange( event, oldVal, newVal )
 *		onEnter( event )
 *		onCancel( event )
 *		onNext( event )
 *		onFocusOut( event, val )
 *
 */

	prepareTextInput : function( settings ) {

		incoming = function( event ) {
			dsval = $(this).parent().find( 'input' ).attr( 'value' );

			settings = event.data['settings'];

			if ( settings && settings.hooks && settings.hooks.onFocus )
			{
				if ( settings.hooks.onFocus.call( $(this), event, dsval ) === false )
				{
					$(this).one( 'click', { 'settings' : settings }, incoming );
					return false;
				}
			}

			sam = $(this).empty().append( '<input type="text" value="' + dsval + '" />' );
			inval = $(this).find( "input" ).focus().focusout( { 'settings' : settings }, outgoing ).keydown( { 'settings' : settings }, keystroke );
			return false;
		};

		restore = function( event ) {
			oldVal = $(this).parent().parent().find( 'input' ).not(this).first().attr( 'value' );
			newVal = $(this).val();

			settings = event.data['settings'];

			if ( oldVal != newVal )
			{
				if ( settings && settings.hooks && settings.hooks.onChange )
					if ( settings.hooks.onChange.call( $(this), event, oldVal, newVal ) === false )
						return false;
			}

			par = $(this).parent();
			par.parent().find( 'input' ).not(this).first().attr( 'value', newVal);
			par.empty().append( newVal );
			par.one( 'click', { 'settings' : settings }, incoming );

			if ( settings && settings.hooks && settings.hooks.onFocusOut )
				if ( settings.hooks.onFocusOut.call( $(this), event, newVal ) === false )
					return false;

			return true;
		}

		proceed = function( event ) {
			if ( settings && settings.behaviour && settings.behaviour.next )
			{
				if ( typeof(settings.behaviour.next) === 'function' )
				{
					rc = settings.behaviour.next.call( this, event );
					if ( typeof( rc ) === 'string' )
						$( rc ).click();
				}
				else
				{
					$( settings.behaviour.next ).click();
				}
			}
		}

		outgoing = function( event ) {
			if ( restore.call( this, event ) == false ) return false;
			return false;
		};

		keystroke = function( event ) {
			if ( event.keyCode == '13') {
				event.preventDefault();

				settings = event.data['settings'];
				if ( settings && settings.hooks && settings.hooks.onEnter )
					if ( settings.hooks.onEnter.call( $(this), event ) === false )
						return false;

				if ( restore.call( this, event ) === false ) return false;
				proceed.call( this, event );
			}
			if ( event.keyCode == '9') {
				event.preventDefault();

				settings = event.data['settings'];
				if ( settings && settings.hooks && settings.hooks.onNext )
					if ( settings.hooks.onNext.call( $(this), event ) === false )
						return false;

				if ( restore.call( this, event ) === false ) return false;
				proceed.call( this, event );
			}
			if ( event.keyCode == '27') {
				event.preventDefault();

				settings = event.data['settings'];
				if ( settings && settings.hooks && settings.hooks.onCancel )
					if ( settings.hooks.onCancel.call( $(this), event ) === false )
						return false;

				$(this).val( $(this).parent().parent().find( 'input' ).not(this).first().attr( 'value' ) );

				if ( restore.call( this, event ) === false ) return false;
			}
		};

		$(this).one( 'click', { 'settings' : settings }, incoming );
		return methods;
	},


	prepareCurrencyInput : function( settings ) {

		numberize = function( val ) {
			if ( isNaN( val ) ) return (new Number( '0.00')).toFixed(2);
			return (new Number(val)).toFixed(2);
		},

		incoming = function( event ) {
			dsval = this.numberize( $(this).parent().find( 'input' ).attr( 'value' ) );

			settings = event.data['settings'];

			if ( settings && settings.hooks && settings.hooks.onFocus )
			{
				if ( settings.hooks.onFocus.call( $(this), event, dsval ) === false )
				{
					$(this).one( 'click', { 'settings' : settings }, this.incoming );
					return false;
				}
			}

			sam = $(this).empty().append( '<input type="text" value="' + dsval + '" />' );
			inval = $(this).find( "input" ).focus().focusout( { 'settings' : settings }, outgoing ).keydown( { 'settings' : settings }, keystroke );
			return false;
		};

		restore = function( event ) {
			oldVal = numberize( $(this).parent().parent().find( 'input' ).not(this).first().attr( 'value' ) );

			newVal = $(this).val();

			if ( isNaN( newVal ) ) newVal = oldVal;
			else newVal = numberize( newVal );

			settings = event.data['settings'];

			if ( oldVal != newVal )
			{
				if ( settings && settings.hooks && settings.hooks.onChange )
					if ( settings.hooks.onChange.call( $(this), event, oldVal, newVal ) === false )
						return false;
			}

			par = $(this).parent();
			par.parent().find( 'input' ).not(this).first().attr( 'value', newVal);
			par.empty().append( newVal );
			par.one( 'click', { 'settings' : settings }, incoming );

			if ( settings && settings.hooks && settings.hooks.onFocusOut )
				if ( settings.hooks.onFocusOut.call( $(this), event, newVal ) === false )
					return false;

			return true;
		}

		proceed = function( event ) {
			if ( settings && settings.behaviour && settings.behaviour.next )
			{
				if ( typeof(settings.behaviour.next) === 'function' )
				{
					rc = settings.behaviour.next.call( this, event );
					if ( typeof( rc ) === 'string' )
						$( rc ).click();
				}
				else
				{
					$( settings.behaviour.next ).click();
				}
			}
		}

		outgoing = function( event ) {
			if ( restore.call( this, event ) == false ) return false;
			return false;
		};

		keystroke = function( event ) {
			if ( event.keyCode == '13') {
				event.preventDefault();

				settings = event.data['settings'];
				if ( settings && settings.hooks && settings.hooks.onEnter )
					if ( settings.hooks.onEnter.call( $(this), event ) === false )
						return false;

				if ( restore.call( this, event ) === false ) return false;
				proceed.call( this, event );
			}
			if ( event.keyCode == '9') {
				event.preventDefault();

				settings = event.data['settings'];
				if ( settings && settings.hooks && settings.hooks.onNext )
					if ( settings.hooks.onNext.call( $(this), event ) === false )
						return false;

				if ( restore.call( this, event ) === false ) return false;
				proceed.call( this, event );
			}
			if ( event.keyCode == '27') {
				event.preventDefault();

				settings = event.data['settings'];
				if ( settings && settings.hooks && settings.hooks.onCancel )
					if ( settings.hooks.onCancel.call( $(this), event ) === false )
						return false;

				$(this).val( $(this).parent().parent().find( 'input' ).not(this).first().attr( 'value' ) );

				if ( restore.call( this, event ) === false ) return false;
			}
		};

		$(this).one( 'click', { 'settings' : settings }, incoming );
		return methods;
	}

};

$.fn.jItol = function( method ) {

	if ( methods[method] ) {
		return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
	} else if ( typeof method === 'object' || ! method ) {
		return methods.init.apply( this, arguments );
	} else {
		$.error( 'Method ' +  method + ' does not exist on jQuery.jInvoice' );
	}
};
})( jQuery );


