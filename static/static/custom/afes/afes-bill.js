
if ( typeof afes.ex.table == 'undefined') {
	alert( 'ERROR: afes.cust.bill needs afes-table.' );
	exit();
}

/* ------------------------------------------------------- */


if ( ! afes.cust ) afes.cust = {}
if ( ! afes.cust.bill ) afes.cust.bill = {}
if ( ! afes.cust.bill._data ) afes.cust.bill._data = {}
if ( ! afes.cust.bill._support ) afes.cust.bill._support = {}


afes.cust.bill._data.mapping = {}

/*
--------- Example Mapping ---------------------------
{
	amount : [ 'div.qty input', 'div.unit-price input' ],

	tax : {
		selector : 'div.tax-rate input',
		rates : {
			'0' : false,
			'1' : [ true, '0.14' ],
			'2' : [ false, '0.14' ],
			'3' : false,
		}
	},

	display : {
		row : {
			tax : '.tax-amount',
			amount : '.amount'
		},
		total : {
			tax : '#summary_tax',
			amount : '#summary_amount',
			total : '#summary_total'
		}
	}
};
*/



afes.cust.bill._support.parse_number = function( num )
{
	var sam = num + '';
	sam = sam.replace( /,/g, '' );
	return (new Number(sam));
}

afes.cust.bill._support.format_number = function( num )
{
	var sam = num.toFixed(2);
	var nuwe = '';
	var gotDecimal = false;
	var count = 0;

	for ( var i = (sam.length - 1); i >= 0; --i )
	{
		nuwe = sam[i] + nuwe;

		if ( gotDecimal === false )
		{
			if ( sam[i] == '.' ) gotDecimal = true;
			continue;
		}

		if ( i > 0 )
		{
			if ( (sam[i-1] == '+') || (sam[i-1] == '-') )
			{
				count = 0;
				continue;
			}
		}

		count += 1;

		if ( ((count % 3) == 0) && (i != 0) )
		{
			nuwe = ',' + nuwe;
		}
	}

	return nuwe;
}


afes.cust.bill._support.calculate_row = function( row_elem )
{
	var amount = 1;
	var mapping = afes.cust.bill._data.mapping;

	for ( var i = 0; i < mapping.amount.length; i++ )
	{
		var temp = 1;

		var elem = $(row_elem).find( mapping.amount[i] );
		if ( elem.is( "input" ) )
		{
			temp = afes.cust.bill._support.parse_number( elem.attr("value") );
			elem.attr( "value", afes.cust.bill._support.format_number( temp ) );
		}
		else
		{
			temp = afes.cust.bill._support.parse_number( elem.text() );
			elem.text( afes.cust.bill._support.format_number( temp ) );
		}

		amount = amount * temp;
	}

	return amount;
};


afes.cust.bill._support.determine_tax = function( row_elem, amount )
{
	var mapping = afes.cust.bill._data.mapping;

	if ( (! mapping.tax) || (! mapping.tax.selector) || (! mapping.tax.rates) )
		return { 'amount' : amount, 'tax' : ( new Number(0) ) };

	var option = $(row_elem).find( mapping.tax.selector );
	if ( option.is( "input" ) ) option = option.attr("value");
	else option = option.text();

	if ( ! mapping.tax.rates[ option ] )
		return { 'amount' : amount, 'tax' : ( new Number(0) ) };

	var ropts = mapping.tax.rates[ option ];

	var rate = ( new Number( ropts[1] ) );

	if ( ropts[0] )
	{
		var new_amount = amount / (rate + 1);
		var tax = (amount - new_amount);
		return { 'amount' : (new_amount), 'tax' : tax };
	}
	else {
		var tax = amount * rate;
		return { 'amount' : amount, 'tax' : tax };
	}
};

afes.cust.bill._support.update_row = function( row_elem, adjusted )
{
	var mapping = afes.cust.bill._data.mapping;

	if ( ! mapping.display ) return;
	if ( ! mapping.display.row ) return;

	if ( mapping.display.row.tax )
	{
		var tax = afes.cust.bill._support.format_number( adjusted['tax'] );
		$(row_elem).find( mapping.display.row.tax ).text( tax );
	}

	if ( mapping.display.row.amount )
	{
		var amount = afes.cust.bill._support.format_number( adjusted['amount'] );
		$(row_elem).find( mapping.display.row.amount ).text( amount );
	}
}

afes.cust.bill._support.update_totals = function( body_elem )
{
	var mapping = afes.cust.bill._data.mapping;

	var total_tax = (new Number(0));
	var total_amount = (new Number(0));

	if ( mapping.display.row.tax )
	{
		$(body_elem).find( mapping.display.row.tax ).each( function() {
			var val = afes.cust.bill._support.parse_number( $(this).text() );
			total_tax += val;
		});
	}

	if ( mapping.display.row.amount )
	{
		$(body_elem).find( mapping.display.row.amount ).each( function() {
			var val = afes.cust.bill._support.parse_number( $(this).text() );
			total_amount += val;
		});
	}

	if ( mapping.display.total.amount )
		$( mapping.display.total.amount ).empty().append( afes.cust.bill._support.format_number( total_amount ) );

	if ( mapping.display.total.tax )
		$( mapping.display.total.tax ).empty().append( afes.cust.bill._support.format_number( total_tax ) );

	if ( mapping.display.total.total )
	{
		var total = total_tax + total_amount;
		$( mapping.display.total.total ).empty().append( afes.cust.bill._support.format_number( total ) );
	}
}


afes.cust.bill.init =  function( mapping )
{
	afes.cust.bill._data.mapping = mapping;
}


afes.cust.bill.hooks =  {
	onFocusOut : function( event, val ) {
		var cell_elem = $(this);
		if ( cell_elem.hasClass( "afes-input-type-currency" ) )
			cell_elem.text( afes.cust.bill._support.format_number( afes.cust.bill._support.parse_number( val ) ) );

		var row_elem = $(this).parents( ".afes-table-body-row" ).first();

		var amount = afes.cust.bill._support.calculate_row( row_elem );
		var adjusted = afes.cust.bill._support.determine_tax( row_elem, amount );

		afes.cust.bill._support.update_row( row_elem, adjusted );

		var body_elem = $(row_elem).parent( "tbody" );

		afes.cust.bill._support.update_totals( body_elem );

		return true;
	}
};


