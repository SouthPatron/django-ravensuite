


(function( $ ){

var settings = {
}


var methods = {
	init : function( options ) {
		if ( options ) {
			$.extend( settings, options );
		}

		return this;
	},

	load_modal : function( url ) {

		this.click( function() {
			$.getJSON( url, function( data ) {
					$("#smktools-div").empty();

					for ( var i = 0; i < data['html'].length; i++ )
						$("#smktools-div").append( data['html'][i] );

					for ( var i = 0; i < data['javascript'].length; i++ )
						$.globalEval( data['javascript'][i] );
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


$(document).ready( function() {
	$( "body" ).append( '<div id="smktools-div">&nbsp;</div>' );
});

