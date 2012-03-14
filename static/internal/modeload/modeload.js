/* Modeload - Loading a modal view from a server.
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

/*
 * Methods
 *
 *
 *
 */


/* ----------------- Dependency Checks ------------------- */

if (typeof jQuery == 'undefined') {
	alert( 'ERROR: (MODELOAD) modeload requires jQuery to be loaded' );
	exit();
}

if ( jQuery.fn.jquery < '1.6.2' ) {
	alert( 'ERROR: (MODELOAD) modeload has only been tested against jQuery 1.6.2. Please upgrade.' );
	exit();
}

/* ------------------------------------------------------- */

var modeload = new function() {

	this.version = '1.0.0';

	this.fetchObject = function( url, pdata, success ) {
		jquery.post( url, pdata, function(data) {
			var obj = jQuery.parseJSON( data );
			success( obj );
		});
	}

	this.load = function( url, pdata ) {

		this.fetchObject( url, pdata, function( obj ) {
			alert( 'We were able to load the object: ' + obj );
		});
	}

}


