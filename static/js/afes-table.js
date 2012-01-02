
/*
 *
 * Requires:
 * 
 *		. Afes
 *
 */


if ( ! afes.ex ) afes.ex = {}

afes.ex.table = {}

afes.ex.table.init = function( elem, settings ) {

	var column_count = settings.columns.length;

	var initial_rows = 0;
	if ( settings.initialRows ) initial_rows = settings.initialRows;


	for ( var rowInitCount = 0; rowInitCount < initial_rows; rowInitCount++ )
	{
		var current_rowid = "afes-table-r" + rowInitCount;
		var next_rowid = "afes-table-r" + (rowInitCount+1);

		var row = $( "<tr />", { id : current_rowid } );

		$( elem ).find( "tbody" ).append( row );

		for ( var col = 0; col < column_count; col++ )
		{
			var cinfo = settings.columns[ col ];

			var cellid = current_rowid + "c" + col;
			var nextid = false;

			if ( col < (column_count-1) )
			{
				nextid = current_rowid + "c" + (col+1);
			}
			else
			{
				if ( rowInitCount < (initial_rows - 1) )
				{
					nextid = next_rowid + "c" + 0;
				}
			}


			var cell = $( "<td />", { id : cellid } );

			var def = cinfo.default;
			if ( def ) cell.html( def );

			row.append( cell );

			if ( cinfo.type == "text" )
			{
				afes.textInput( cell,
					{
						behaviour: {
							next : "#" + nextid
						},
						callbacks : {
							onNext : function( event ) {
							}
						}
					}
				);
			}

			if ( cinfo.type == "currency" )
			{
				afes.currencyInput( cell,
					{
						behaviour: {
							next : "#" + nextid
						}
					}
				);
			}

			if ( cinfo.type == "select" )
			{
				afes.selectInput( cell,
					{
						behaviour: {
							next : "#" + nextid
						},
						options : cinfo.options
					}
				);
			}

		}
	}

}





