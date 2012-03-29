/* <script type='text/javascript'> */

// Define columns
// 		onChange events
// 		Define tax rate input and output
// 	Define target total outputs
//

function parse_number( num )
{
	var sam = num + '';
	sam = sam.replace( ',', '' );
	return (new Number(sam));
}

function format_number( num )
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


function calculate_row( row_elem )
{
	var amount = 1;

	for ( var i = 0; i < mapping.amount.length; i++ )
	{
		var temp = 1;

		var elem = $(row_elem).find( mapping.amount[i] );
		if ( elem.is( "input" ) )
		{
			temp = parse_number( elem.attr("value") );
			elem.attr( "value", format_number( temp ) );
		}
		else
		{
			temp = parse_number( elem.text() );
			elem.text( format_number( temp ) );
		}

		amount = amount * temp;
	}

	return amount;
};


function determine_tax( row_elem, amount )
{
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

function update_row( row_elem, adjusted )
{
	if ( ! mapping.display ) return;
	if ( ! mapping.display.row ) return;

	if ( mapping.display.row.tax )
	{
		var tax = format_number( adjusted['tax'] );
		$(row_elem).find( mapping.display.row.tax ).text( tax );
	}

	if ( mapping.display.row.amount )
	{
		var amount = format_number( adjusted['amount'] );
		$(row_elem).find( mapping.display.row.amount ).text( amount );
	}
}

function update_totals( body_elem )
{
	var total_tax = (new Number(0));
	var total_amount = (new Number(0));

	if ( mapping.display.row.tax )
	{
		$(body_elem).find( mapping.display.row.tax ).each( function() {
			var val = parse_number( $(this).text() );
			total_tax += val;
		});
	}

	if ( mapping.display.row.amount )
	{
		$(body_elem).find( mapping.display.row.amount ).each( function() {
			var val = parse_number( $(this).text() );
			total_amount += val;
		});
	}

	if ( mapping.display.total.amount )
		$( mapping.display.total.amount ).empty().append( format_number( total_amount ) );

	if ( mapping.display.total.tax )
		$( mapping.display.total.tax ).empty().append( format_number( total_tax ) );

	if ( mapping.display.total.total )
	{
		var total = total_tax + total_amount;
		$( mapping.display.total.total ).empty().append( format_number( total ) );
	}
}


	var updateHooks = {
		onFocusOut : function( event, val ) {
			var cell_elem = $(this);
			if ( cell_elem.hasClass( "afes-input-type-currency" ) )
				cell_elem.text( format_number( parse_number( val ) ) );

			var row_elem = $(this).parents( ".afes-table-body-row" ).first();

			var amount = calculate_row( row_elem );
			var adjusted = determine_tax( row_elem, amount );

			update_row( row_elem, adjusted );

			var body_elem = $(row_elem).parent( "tbody" );

			update_totals( body_elem );

			return true;
		}
	};


/*  / script> */
