
/*
 *
 * Namespaces:
 *
 * 	afes.ex				 - External stuff
 * 	afes.ex.table		 - The table methods
 * 	afes.ex.table._data	 - Data associated with the tables
 * 	afes.ex.table._stubs - Stubs for the callbacks
 *
 * 	Methods:
 *
 *
 * 		afes.ex.table.init( elem, settings )
 *		afes.ex.table.get_data( elem )
 *		afes.ex.table.getCellNum( cell )
 *		afes.ex.table.getRowNum( row )
 *		afes.ex.table.getNextCell( elem, editable )
 *		afes.ex.table.getNextEditableCell( event )
 *		afes.ex.table.newCell( settings )
 *		afes.ex.table.newFormField( settings )
 *		afes.ex.table.setEditingState( cell, settings )
 *		afes.ex.table.getRowCount( elem )
 *		afes.ex.table.appendRow( elem, values )
 *		afes.ex.table.appendDefaultRow( elem )
 *		afes.ex.table.insertRow( elem, values )
 *		afes.ex.table.deleteMyRow( elem )
 *		afes.ex.table.deleteRow( elem, num )
 *
 *		afes.ex.table._stubs.common( target )
 *		afes.ex.table._stubs.onFocus( event, val )
 *		afes.ex.table._stubs.onUpdate( event, oldVal, newVal )
 *		afes.ex.table._stubs.onChange( event, val )
 *		afes.ex.table._stubs.onEnter( event )
 *		afes.ex.table._stubs.onCancel( event )
 *		afes.ex.table._stubs.onNext( event )
 *		afes.ex.table._stubs.onFocusOut( event, val )
 * 
 *
 * Data structure kept in afes.ex.table._data
 *
 * 	settings  ( any part can be overridden by init method settings param )
 *	 	min_rows
 * 		max_rows
 * 		initial_rows
 * 		action_on_final_next : "nothing,extend,loop"
 * 		columns
 * 			type : text/currency/select
 * 			initial : initial (text)
 * 			options
 * 				"key" : "value"
 * 				...
 * 			class : "" (space separated list of additional classes)
 * 			editable : true/false (can edit)
 * 			
 * 			callbacks
 *				onFocus( event, val )
 *				onUpdate( event, oldVal, newVal )
 *				onChange( event, val )
 *				onEnter( event )
 *				onCancel( event )
 *				onNext( event )
 *				onFocusOut( event, val )
 *
 *
 *
 * CSS classes:
 *
 * 	afes-table
 *
 * 	afes-table-head-row
 * 	afes-table-head-row-first
 * 	afes-table-head-row-last
 *
 * 	afes-table-head-cell
 * 	afes-table-head-cell-first
 * 	afes-table-head-cell-last
 *
 * 	afes-table-body-row
 * 	afes-table-body-row-first
 * 	afes-table-body-row-last
 *
 * 	afes-table-body-cell
 * 	afes-table-body-cell-first
 * 	afes-table-body-cell-last
 * 	afes-table-body-cell-num-#	( where # is the column number )
 *
 * 	afes-table-body-cell-div-form
 *
 * 	afes-table-body-cell-edit-true
 * 	afes-table-body-cell-edit-false
 *
 * 	afes-table-body-cell-type-currency
 * 	afes-table-body-cell-type-text
 * 	afes-table-body-cell-type-select
 *
 *
 * Requires:
 * 
 *		. Afes
 *
 */


if ( ! afes.ex ) afes.ex = {}
if ( ! afes.ex.table ) afes.ex.table = {}
if ( ! afes.ex.table._data ) afes.ex.table._data = {}
if ( ! afes.ex.table._stubs ) afes.ex.table._stubs = {}



afes.ex.table.get_data = function( elem ) {
	var id = $( elem ).attr( "id" );

	if ( ! id )
		throw "afes.ex.table.get_data on element without id attribute";
	

	if ( ! afes.ex.table._data[ id ] )
	{
		afes.ex.table._data[ id ] = {
			settings : {
				min_rows: 0,
				max_rows : -1,
				initial_rows : 1,
				action_on_final_next : "loop"
			}
		};
	}

	return afes.ex.table._data[ id ];
}

afes.ex.table.init = function( elem, settings ) {

	var data = afes.ex.table.get_data( elem );

	data.settings = $.extend( true, data.settings, settings );	// deep copy

	// CSS Classes

	$( elem ).addClass( "afes-table" );

	$( elem ).find( "thead tr" ).first().addClass( "afes-table-head-row-first" );
	$( elem ).find( "thead tr" ).last().addClass( "afes-table-head-row-last" );
	$( elem ).find( "thead tr" ).addClass( "afes-table-head-row" );

	$( elem ).find( "thead tr td, thead tr th" ).first().addClass( "afes-table-head-cell-first" );
	$( elem ).find( "thead tr td, thead tr th" ).last().addClass( "afes-table-head-cell-last" );
	$( elem ).find( "thead tr td, thead tr th" ).addClass( "afes-table-head-cell" );

	// Set up the initial rows

	var ds = data.settings;
	var initial_rows = ds.initial_rows;

	for ( var i = 0; i < initial_rows; i++ )
		afes.ex.table.appendDefaultRow( elem );

}



afes.ex.table.getCellNum = function( cell )
{
	var classes = ("" + cell.attr( "class" )).split( /\s+/ );

	for ( var i = 0; i < classes.length; i++ )
	{
		var matches = classes[i].match( /afes\-table\-body\-cell\-num\-(\d+)/ );
		if ( matches ) return parseInt( matches[1] );
	}

	return false;
}

afes.ex.table.getRowNum = function( row )
{
	var classes = ("" + row.attr( "class" )).split( /\s+/ );

	for ( var i = 0; i < classes.length; i++ )
	{
		var matches = classes[i].match( /afes\-table\-body\-row\-num\-(\d+)/ );
		if ( matches ) return parseInt( matches[1] );
	}

	return false;
}


afes.ex.table.getNextCell = function( elem, editable ) {

	var tafel = $( elem ).parents( ".afes-table" ).first();
	var data = afes.ex.table.get_data( tafel );

	var cell = elem;

	if ( $( cell ).is( "td" ) == false )
		cell = $(cell).parents( "td" ).first();

	if ( ! cell )
		throw "Unable to get parent cell";

	var row = $( cell ).parents( "tr" ).first();

	if ( ! row )
		throw "Unable to get parent row";

	var body = $( row ).parents( "tbody" ).first();

	if ( ! body )
		throw "Unable to get table tbody";

	var cellNum = afes.ex.table.getCellNum( cell );
	var rowNum = row.prevAll( "tr" ).length;

	if ( (cellNum === false) || (rowNum === false) )
		throw "Cell row+col was not identifiable.";

	var ds = data.settings;

	var max_rows = body.find( "tr" ).length;
	var max_cols = ds.columns.length;

	var my_col = cellNum + 1;
	var my_row = rowNum;

	var looped_around = 0;

	while ( looped_around < 2 )
	{
		looped_around += 1;

		while ( my_row < max_rows )
		{
			while ( my_col < max_cols )
			{
				var cinfo = ds.columns[ my_col ];

				if ( ! editable )
				{
					return ($((body.children( "tr" ))[ my_row ]).children("td"))[ my_col ];
				}

				var canEdit = true;
				if ( typeof( cinfo.editable ) != "undefined" ) canEdit = cinfo.editable;

				if ( editable == canEdit )
				{
					return ($((body.children( "tr" ))[ my_row ]).children("td"))[ my_col ];
				}

				my_col += 1;
			}

			my_col = 0;
			my_row += 1;
		}


		// Handle the run-out

		if ( ds.action_on_final_next == "loop" )
		{
			my_row = 0;
			my_col = 0;
		}
		else if ( ds.action_on_final_next == "extend" )
		{
			if ( afes.ex.table.appendDefaultRow( tafel ) == false )
			{
				// If we can't extend, loop.
				my_row = 0;
				my_col = 0;
			}
			else
			{
				max_rows += 1;
			}
		}
		else	// nothing, so break;
		{
			break;
		}
	}

	return false;
}

afes.ex.table.getNextEditableCellCallback = function( event ) {
	return afes.ex.table.getNextCell( $(this), true );
}


afes.ex.table.newCell = function( settings, ival ) {

	var cell = $( "<td></td>" );

	var def = ival;
	if ( ! def ) def = "";

	cell.html( def );

	return cell;
}

afes.ex.table.newFormField = function( settings, ival ) {

	var def = ival
	if ( ! def ) def = "";

	// Find the select value
	if ( settings.type == "select" )
	{
		for ( var key in settings.options )
		{
			if ( def == key )
			{
				def = settings.options[ key ];
				break;
			}
		}
	}


	var field = $( "<div />",
				{
					class : "afes-table-body-cell-div-form",
					style : "display : none; visibility : hidden "
				}
			);
	var field_hidden = $( "<input />",
						{
							type : "hidden",
							value : def,
							name : settings.form_name
						}
					);
	field.append( field_hidden );
	return field;
}

afes.ex.table.setEditingState = function( cell, settings ) {

	var canEdit = true;
	if ( typeof( settings.editable ) !== "undefined" )
		canEdit = ( settings.editable === true );

	if ( ! canEdit )
	{
		$( cell ).addClass( "afes-table-body-cell-no-edit" );
		return;
	}

	var behav = {
		next : afes.ex.table.getNextEditableCellCallback
	}

	$( cell ).addClass( "afes-table-body-cell-can-edit" );

	if ( settings.type == "text" )
	{
		afes.textInput( cell,
			{
				behaviour: behav,
				callbacks : afes.ex.table._stubs
			}
		);
		return;
	}

	if ( settings.type == "currency" )
	{
		afes.currencyInput( cell,
			{
				behaviour: behav,
				callbacks : afes.ex.table._stubs
			}
		);
		return;
	}

	if ( settings.type == "select" )
	{
		afes.selectInput( cell,
			{
				behaviour: behav,
				options : settings.options,
				callbacks : afes.ex.table._stubs
			}
		);
		return;
	}
}

afes.ex.table.getRowCount = function( elem ) {
	
	var myelem = elem;

	if ( ! $( myelem ).hasClass( "afes-table" ) )
		myelem = $( myelem ).parents( ".afes-table" ).first();

	if ( ! myelem )
		throw "getRowCount called on non-table element";

	return $( myelem ).find( "tbody" ).find( "tr" ).length;
}

afes.ex.table.appendRow = function( elem, values ) {
	return afes.ex.table.insertRow( elem, values );
}

afes.ex.table.appendDefaultRow = function( elem ) {
	var data = afes.ex.table.get_data( elem );
	var ds = data.settings;
	var column_count = ds.columns.length;

	var new_data = new Array();

	for ( var i = 0; i < column_count; i++ )
		new_data.push( ds.columns[i].initial );

	return afes.ex.table.appendRow( elem, new_data );
}



afes.ex.table.insertRow = function( elem, values, pos ) {

	var data = afes.ex.table.get_data( elem );
	var ds = data.settings;
	var column_count = ds.columns.length;

	// Enough room for another one?
	var row_count = afes.ex.table.getRowCount( elem );
	if ( ds.max_rows && ds.max_rows >= 0 )
		if ( row_count >= ds.max_rows )
			return false;


	// Insert into the correct location
	var row = $( "<tr />" );

	if ( (typeof( pos ) == "undefined") || (pos >= row_count) )
	{
		$( elem ).find( "tbody" ).append( row );
	}
	else if ( pos < 0 )
	{
		$( elem ).find( "tbody" ).prepend( row );
	}
	else
	{
		$( $( elem ).find( "tbody" ).find( "tr" ).get( pos ) ).before( row );
	}


	// Build row

	for ( var col = 0; col < column_count; col++ )
	{
		var cinfo = ds.columns[ col ];
		var cell = afes.ex.table.newCell( cinfo, values[ col ] );

		row.append( cell );

		if ( cinfo.form_name )
		{
			ffield = afes.ex.table.newFormField( cinfo, values[ col ] );

			if ( cinfo.class )
				$( ffield ).addClass( cinfo.class );

			row.append( ffield );
		}

		afes.ex.table.setEditingState( cell, cinfo );

		// Add cell type
		$( cell ).addClass( "afes-table-body-cell-type-" + cinfo.type );

		// Add column number to class
		$( cell ).addClass( "afes-table-body-cell-num-" + col );

		// Add user requested class to column
		if ( cinfo.class )
			$( cell ).addClass( cinfo.class );

	}


	// CSS Classes

	if ( $(elem).find( "tbody tr" ).length == 1 )
		$( row ).addClass( "afes-table-body-row-first" );

	$( elem ).find( ".afes-table-body-row-last" ).removeClass( "afes-table-body-row-last" );
	$( row ).addClass( "afes-table-body-row-last afes-table-body-row" );

	$( row ).find("td").first().addClass( "afes-table-body-cell-first" );
	$( row ).find("td").last().addClass( "afes-table-body-cell-last" );
	$( row ).find("td").addClass( "afes-table-body-cell" );

	return true;
}



afes.ex.table.deleteMyRow = function( elem ) {

	var myelem = elem;

	if ( ! $( myelem ).hasClass( "afes-table-body-row" ) )
		myelem = $( myelem ).parents( ".afes-table-body-row" ).first();


	if ( $( myelem ).hasClass( "afes-table-body-row" ) )
	{
		myelem.remove();
		return true;
	}

	return false;
}

afes.ex.table.deleteRow = function( elem, num ) {
	$( $( elem ).find( "tbody" ).find( "tr" ).get( num ) ).remove();
	return true;
}




/*               STUBS FOR CALLBACKS                             */


afes.ex.table._stubs.common = function( target )
{
	var elem = $( target ).parents( ".afes-table" ).first();
	var data = afes.ex.table.get_data( elem );

	var targ = target;
	
	if ( ! targ.is( "td" ) )
		targ = $( target ).parents( "td" ).first();

	var col = afes.ex.table.getCellNum( targ );

	if ( col < 0 || col >= data.settings.columns.length )
		throw "Column number exceeded configured column amount";

	return data.settings.columns[ col ];
}

afes.ex.table._stubs.onFocus = function( event, val )
{
	var rc = afes.ex.table._stubs.common( $(this) );
	if ( rc.callbacks && rc.callbacks.onFocus )
		return rc.callbacks.onFocus.call( $(this), event, val );
	return true;
}

afes.ex.table._stubs.onUpdate = function( event, oldVal, newVal )
{
	var rc = afes.ex.table._stubs.common( $(this) );

	var nuwe = true;

	if ( rc.callbacks && rc.callbacks.onUpdate )
		nuwe = rc.callbacks.onUpdate.call( $(this), event, oldVal, newVal );

	if ( nuwe !== false )
	{
		var toBe = nuwe;

		if ( toBe === true ) toBe = newVal;

		// Update the form field, if present
		if ( rc.form_name )
		{
			var ffield = $( event.target ).parents( "td" ).first().next();

			if ( ! ffield.is( "div" ) )
				throw "Form field was not found correctly. It should be next.";

			ffield.find( "input" ).val( toBe );
		}
	}

	return nuwe;
}

afes.ex.table._stubs.onChange = function( event, val )
{
	var rc = afes.ex.table._stubs.common( $(this) );
	if ( rc.callbacks && rc.callbacks.onChange )
		return rc.callbacks.onChange.call( $(this), event, val );
	return true;
}

afes.ex.table._stubs.onEnter = function( event )
{
	var rc = afes.ex.table._stubs.common( $(this) );
	if ( rc.callbacks && rc.callbacks.onEnter )
		return rc.callbacks.onEnter.call( $(this), event );
	return true;
}

afes.ex.table._stubs.onCancel = function( event )
{
	var rc = afes.ex.table._stubs.common( $(this) );
	if ( rc.callbacks && rc.callbacks.onCancel )
		return rc.callbacks.onCancel.call( $(this), event );
	return true;
}

afes.ex.table._stubs.onNext = function( event )
{
	var rc = afes.ex.table._stubs.common( $(this) );
	if ( rc.callbacks && rc.callbacks.onNext )
		return rc.callbacks.onNext.call( $(this), event );
	return true;
}

afes.ex.table._stubs.onFocusOut = function( event, val )
{
	var rc = afes.ex.table._stubs.common( $(this) );
	if ( rc.callbacks && rc.callbacks.onFocusOut )
		return rc.callbacks.onFocusOut.call( $(this), event, val );
	return true;
}



