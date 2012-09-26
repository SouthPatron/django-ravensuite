/* OSS
 *
 * Global store of active objects or collections.
 *
 *
 *
 */

(function(){

	var root = this;
	var previousOSS = root.OSS;

	var OSS;
	if (typeof exports !== 'undefined') {
		OSS = exports;
	} else {
		OSS = root.OSS = {};
	}

	OSS.VERSION = '0.0.1';
	var $ = root.jQuery;

	var dictionary = OSS.dictionary = {};

	/* ------- Internal methods for management of ids ---- */

	var retrieve = OSS.retrieve = function( id ) {
		return ( this.dictionary[ id ] || null );
	}

	var store = OSS.store = function( id, obj ) {
		this.dictionary[ id ] = obj;
	}

	var remove = OSS.remove = function( id ) {
		delete this.dictionary[ id ];
	}

	/* ------- Support methods for easier access ---- */

	var getApp = OSS.getApp = function() {
		return this.retrieve( 'app.router' );
	}

	var setApp = OSS.setApp = function( app ) {
		return this.store( 'app.router', app );
	}


}).call(this);

