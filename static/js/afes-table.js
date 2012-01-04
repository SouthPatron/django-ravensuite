
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
 *		afes.ex.table.appendDefaultRow( elem )
 *		afes.ex.table.appendRow( elem, values )
 *
 * 
 *
 * Data structure kept in afes.ex.table._data
 *
 * 	row_counter
 * 	settings  ( any part can be overridden by init method settings param )
 *	 	min_rows
 * 		max_rows
 * 		initial_rows
 * 		columns
 * 			type : text/currency/select
 * 			default : default (text)
 * 			options
 * 				"key" : "value"
 * 				...
 * 			class : "" (space separated list of additional classes)
 * 			editable : true/false (can edit)
 * 			
 * 			callbacks
 *				onFocus( event, value )
 *				onUpdate( event, oldVal, newVal )
 *				onChange( event )
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
 * 	afes-table-body-cell-#	( where # is the column number )
 *
 * 	afes-table-body-cell-currency
 * 	afes-table-body-cell-text
 * 	afes-table-body-cell-select
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

	if ( ! id ) alert( "afes.ex.table.get_data on element without id attribute" );

	if ( ! afes.ex.table._data[ id ] )
	{
		afes.ex.table._data[ id ] = {
			row_counter : 0,
			settings : {
				min_rows: 0,
				max_rows : -1,
				initial_rows : 1
			}
		};
	}

	return afes.ex.table._data[ id ];
}

afes.ex.table.init = function( elem, settings ) {

	var data = afes.ex.table.get_data( elem );

	data.settings = $.extend( true, data.settings, settings );	// deep copy

	var ds = data.settings;
	var initial_rows = ds.initial_rows;

	for ( var i = 0; i < initial_rows; i++ )
		afes.ex.table.appendDefaultRow( elem );

	// CSS Classes

	$( elem ).addClass( "afes-table" );

	$( elem ).find( "thead tr" ).first().addClass( "afes-table-head-row-first" );
	$( elem ).find( "thead tr" ).last().addClass( "afes-table-head-row-last" );
	$( elem ).find( "thead tr" ).addClass( "afes-table-head-row" );

	$( elem ).find( "thead tr td, thead tr th" ).first().addClass( "afes-table-head-cell-first" );
	$( elem ).find( "thead tr td, thead tr th" ).last().addClass( "afes-table-head-cell-last" );
	$( elem ).find( "thead tr td, thead tr th" ).addClass( "afes-table-head-cell" );

}


afes.ex.table.appendDefaultRow = function( elem ) {
	var data = afes.ex.table.get_data( elem );
	var ds = data.settings;
	var column_count = ds.columns.length;

	var new_data = [];

	for ( var i = 0; i < column_count; i++ )
		new_data.push( ds.columns.default );

	afes.ex.table.appendRow( elem, new_data );
}


afes.ex.table.appendRow = function( elem, values ) {

	var data = afes.ex.table.get_data( elem );
	var ds = data.settings;
	var column_count = ds.columns.length;

	var rownum = data.row_counter++;	// Increment data.row_counter

	var cur_rowid = "afes-table-" + $(elem).attr("id") + "-r" + rownum;

	var row = $( "<tr />", { id : cur_rowid } );

	$( elem ).find( "tbody" ).append( row );

	for ( var col = 0; col < column_count; col++ )
	{
		var cinfo = ds.columns[ col ];

		var cellid = cur_rowid + "c" + col;
		var nextid = false;

		if ( col < (column_count-1) )
			nextid = cur_rowid + "c" + (col+1);

		var cell = $( "<td />", { id : cellid } );

		var def = cinfo.default;
		if ( def ) cell.html( def );

		row.append( cell );

		var canEdit = true;
		if ( typeof( cinfo.editable ) !== "undefined" )
			canEdit = ( cinfo.editable === true );


		if ( cinfo.type == "text" )
		{
			if ( canEdit )
			{
				afes.textInput( cell,
					{
						behaviour: {
							next : "#" + nextid
						},
						callbacks : afes.ex.table._stubs
					}
				);
			}

			$( cell ).addClass( "afes-table-body-cell-text" );
		}

		if ( cinfo.type == "currency" )
		{
			if ( canEdit )
			{
				afes.currencyInput( cell,
					{
						behaviour: {
							next : "#" + nextid
						},
						callbacks : afes.ex.table._stubs
					}
				);
			}
			
			$( cell ).addClass( "afes-table-body-cell-currency" );
		}

		if ( cinfo.type == "select" )
		{
			if ( canEdit )
			{
				afes.selectInput( cell,
					{
						behaviour: {
							next : "#" + nextid
						},
						options : cinfo.options,
						callbacks : afes.ex.table._stubs
					}
				);
			}

			$( cell ).addClass( "afes-table-body-cell-select" );
		}

		// Add column number to class
		$( cell ).addClass( "afes-table-body-cell-" + col );

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

}



/*               STUBS FOR CALLBACKS                             */


afes.ex.table._stubs.onUpdate = function( event, oldVal, newVal )
{
	var elem = $( event.target ).parents( ".afes-table" ).first();
	var data = afes.ex.table.get_data( elem );
	var ds = data.settings;

	var target = $( event.target ).parents( "td" ).first();

	var classes = ("" + target.attr( "class" )).split( /\s+/ );

	for ( var i = 0; i < classes.length; i++ )
	{
		var matches = classes[i].match( /afes\-table\-body\-cell\-(\d+)/ );

		if ( matches )
		{
			col = matches[1];
			if ( ds.columns[ col ].callbacks )
			{
				callbacks = ds.columns[ col ].callbacks;
				if ( callbacks.onUpdate )
					return callbacks.onUpdate( event, oldVal, newVal );
			}
		}
	}

	return true;
}



/*		onFocus( event, value )
 *		onUpdate( event, oldVal, newVal )
 *		onChange( event )
 *		onEnter( event )
 *		onCancel( event )
 *		onNext( event )
 *		onFocusOut( event, val )
 *
 */




