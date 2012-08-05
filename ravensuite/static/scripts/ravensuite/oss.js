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

	/* ------- Internal methods for management of pools and ids ---- */

	var retrieve = OSS.retrieve = function( pool, id ) {
		if ( this.dictionary[ pool ] === undefined ) return null;
		if ( this.dictionary[ pool ][ id ] === undefined ) return null;
		return this.dictionary[ pool ][ id ];
	}

	var store = OSS.store = function( pool, id, obj ) {
		if ( this.dictionary[ pool ] === undefined ) {
			this.dictionary[ pool ] = {};
		}

		if ( this.dictionary[ pool ][ id ] !== undefined ) {
			delete this.dictionary[ pool ][ id ];
		}

		this.dictionary[ pool ][ id ] = obj;
	}

	var remove = OSS.remove = function( pool, id ) {
		if ( this.dictionary[ pool ] === undefined )
			return null;

		if ( this.dictionary[ pool ][ id ] !== undefined ) {
			var obj = this.dictionary[ pool ][ id ];
			delete this.dictionary[ pool ][ id ];
			return obj;
		}
	}

	var getPool = OSS.getPool = function( pool ) {
		if ( this.dictionary[ pool ] === undefined ) {
			return {}
		}

		return this.dictionary[ pool ];
	}

	/* ------- Support methods for easier access ---- */

	var getApp = OSS.getApp = function() {
		return this.retrieve( 'app', 'router' );
	}

	var setApp = OSS.setApp = function( app ) {
		return this.store( 'app', 'router', app );
	}


}).call(this);

