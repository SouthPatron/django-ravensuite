

(function( $ ){

var settings = {
}

function load_external( )
{
}



var methods = {
	init : function( options ) {
		if ( options ) {
			$.extend( settings, options );
		}

		return this;
	},

	load_component : function( url ) {

		id = $(this).attr("id");

		divname = 'smktools-component-' + id;
		classname = '.' +divname;

		this.empty();
		$( classname ).remove();


		// ---- Load stylesheet
		var link = $("<link>");
		link.attr({
			type : 'text/css',
			rel : 'stylesheet',
			media : 'screen',
			href : url + '?part=stylesheet',
			class : divname
		});
		$( "head" ).append( link );

		// ---- Load HTML
		this.load( url + '?part=html', function (){
				// ---- Load JavaScript
				$.getScript( url + '?part=javascript' );
			}
		);

		return this;
	},

	load_modal : function( url ) {

		this.click( function() {

			id = $(this).attr("id");

			divname = 'smktools-modal-' + id;
			refname = '#' + divname;
			classname = '.' +divname;

			// ---- Clear the older version
			$( refname ).remove();
			$( "body" ).first().append( '<div id="' + divname + '" class="smktools-hidden">&nbsp;</div>' );
			$( classname ).remove();

			// ---- Load stylesheet
			var link = $("<link>");
			link.attr({
				type : 'text/css',
				rel : 'stylesheet',
				media : 'screen',
				href : url + '?part=stylesheet',
				class : divname
			});
			$( "head" ).append( link );

			// ---- Load HTML
			$( refname ).load( url + '?part=html', function (){
						// ---- Load JavaScript
						$.getScript( url + '?part=javascript' );
					}
				);

		});

		return this;
	}
}


$.fn.smkTools = function( method ) {
	if ( methods[method] ) {
		return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
	} else if ( typeof method === 'object' || ! method ) {
		return methods.init.apply( this, arguments );
	} else {
		$.error( 'Method [' +  method + '] does not exist on jQuery.smkTools' );
	}    
}
})( jQuery );



