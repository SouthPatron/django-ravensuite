

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
	$('.invoice .item-list .item-description').one( 'click', { 'name' : 'description' }, start_field_edit );
	$('.invoice .item-list .item-qty').one( 'click', { 'name' : 'units' }, start_numerical_edit );
	$('.invoice .item-list .item-unit-price').one( 'click', { 'name' : 'perunit' }, start_numerical_edit );
	$('.invoice .item-list .item-tax-rate').one( 'click', start_tax_edit );

	$('.invoice .item-list table .item-delete-link').click( function() {
		$(this).parents( "tr" ).remove();
	});
};


function add_item_line()
{
	if ( settings[ 'editable' ] == false )
		return;

	$('.invoice .item-list table tbody').append( '	\
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

	$(".invoice .item-list tbody tr").each( function() {

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

	$( "#id_invoice_amount" ).val( total_amount.toFixed(2) );
	$( "#id_invoice_tax" ).val( total_tax.toFixed(2) );
	$( "#id_invoice_total" ).val( total_total.toFixed(2) );
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


function invoice_submit( event ) {
	if ( event.data && event.data[ 'new_state' ] )
		$("#id_invoice_state").val( event.data[ 'new_state' ] );
	$("#id_invoice_form").submit();
}


var methods = {
	init : function( options ) {
		if ( options ) {
			$.extend( settings, options );
		}

		return this;
	},

	invoicify : function() {

		$('#id_invoice_date').datepicker( datesettings );
		$('#id_due_date').datepicker( datesettings );

		if ( settings[ 'editable' ] == true )
		{
			apply_edit_hooks();
			$('#id_invoice_add_item_row').click( add_item_line );

		}

		$("#id_button_save").click( invoice_submit );
		$("#id_button_delete").click( { 'new_state' : 99 }, invoice_submit );
		$("#id_button_approve").click( { 'new_state' : 5 }, invoice_submit );
		$("#id_button_void").click( { 'new_state' : 10 }, invoice_submit );

		return this;
	}
};

$.fn.jInvoice = function( method, new_settings ) {

	settings[ 'delete-icon' ] = new_settings[ 'delete-icon' ]
	settings[ 'editable' ] = new_settings[ 'editable' ]
	


	if ( methods[method] ) {
		return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
	} else if ( typeof method === 'object' || ! method ) {
		return methods.init.apply( this, arguments );
	} else {
		$.error( 'Method ' +  method + ' does not exist on jQuery.jInvoice' );
	}    

};
})( jQuery );

