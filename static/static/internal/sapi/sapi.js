/* Sapi - South Patron API Classes
 * Copyright (c) 2012 SMK Software CC
 *
 * Version 1.0.0
 *
 * This code is private and not for distribution by any party besides
 * the original authors and in the manner they intended.
 *
 */

/*
 *
 * Requires:
 * 
 * 		. jQuery
 */


/* ----------------- Dependency Checks ------------------- */

if (typeof jQuery == 'undefined') {
	alert( 'ERROR: (SAPI) requires jQuery to be loaded' );
	exit();
}

if ( jQuery.fn.jquery < '1.6.2' ) {
	alert( 'ERROR: (SAPI) only been tested against jQuery 1.6.2. Please upgrade.' );
	exit();
}


/* ------------------------------------------------------- */

sapi = {}

sapi.version = '1.0.0';

sapi.api = {}

/* ******* QUEUE ********************************************* */

sapi.api._ajaxqueues = { q:{}, r:null };

sapi.api.ajaxq = ( function() {

	function C() {
	}

	function ajax( queue, options ) {

		// Make sure this queue exists
		if ( typeof sapi.api._ajaxqueues.q[queue] == "undefined" )
			sapi.api._ajaxqueues.q[queue] = [];

		// If no options given, clear queue instead.
		if ( typeof options == "undefined" )
		{
			if ( sapi.api._ajaxqueues.r )
			{
				sapi.api._ajaxqueues.r.abort();
				sapi.api._ajaxqueues.r = null;
			}
			sapi.api._ajaxqueues.q[ queue ] = [];
			return;
		}

		// Make a copy of options. We're going to override complete.
		var newOptions = jQuery.extend( true, {}, options );

		var originalComplete = newOptions.complete;

		newOptions.complete = function( request, status )
		{
			sapi.api._ajaxqueues.q[ queue ].shift();
			sapi.api._ajaxqueues.r = null;

			if ( originalComplete ) originalComplete( request, status );

			if ( sapi.api._ajaxqueues.q[ queue ].length > 0 )
				sapi.api._ajaxqueues.r = jQuery.ajax(
						sapi.api._ajaxqueues.q[ queue ][ 0 ]
					);
		}

		// Add in the new query
		sapi.api._ajaxqueues.q[ queue ].push( newOptions );

		// Start it, if first one.
		if ( sapi.api._ajaxqueues.q[ queue ].length == 1 )
			sapi.api._ajaxqueues.r = jQuery.ajax( options );
	}

	C.prototype.ajax = ajax;

	return C;
}());

/* ******* API *********************************************** */


sapi.api.restful = ( function() {

	function C() {
		this.ajaxq = new sapi.api.ajaxq();
	}

	function getOrganizations() {
		var objects = false;

		this.ajaxq.ajax( "_api", {
			url: '/api/restful/org',
			type: 'GET',
			data: { bob: 5, sam: '24234' },
			success: function(result) {
					objects = result;
				},
			timeout: 60000,
			async: false,
			error: function( xhr, textStatus, errorThrown ) {
				if ( textStatus )
				{
					if ( textStatus === "timeout" )
					{
						alert( "Timeout occurred" );
					}
					else if ( textStatus === "error" )
					{
						alert( "Error: " + errorThrown );
					}
					else if ( textStatus === "abort" )
					{
						alert( "Aborted!" );
					}
					else if ( textStatus === "parseerror" )
					{
						alert( "Parse error!" );
					}
					else
					{
						alert( "Unknown error" );
					}
				}
			},
			complete: function() {
				alert( 'Complete called' );
			}
		});

		return objects;
	}

	C.prototype.getOrganizations = getOrganizations;

	return C;
}());


