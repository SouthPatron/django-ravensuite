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

sapi = {
	version : '1.0.0',
	api : {}
}

/* ------- SUPPORT ------------------------------------------- */

String.prototype.sapi_format = function() {
	var formatted = this;
	for (var i = 0; i < arguments.length; i++) {
		var regexp = new RegExp('\\{'+i+'\\}', 'gi');
		formatted = formatted.replace(regexp, arguments[i]);
	}
	return formatted;
};

/* ******* QUEUE ********************************************* */

sapi.api._ajaxqueues = { q:{}, r:null };

sapi.api.ajaxq = function() {}

sapi.api.ajaxq.prototype = {

	ajax : function( queue, options ) {


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
			{
				sapi.api._ajaxqueues.r = jQuery.ajax(
						sapi.api._ajaxqueues.q[ queue ][ 0 ]
					);
			}
		}

		// Add in the new query
		sapi.api._ajaxqueues.q[ queue ].push( newOptions );

		// Start it, if first one.
		if ( sapi.api._ajaxqueues.q[ queue ].length == 1 )
			sapi.api._ajaxqueues.r = jQuery.ajax( newOptions );
	}

}

/* ******* API *********************************************** */


sapi.api.restful = function( options ) {
	this.ajaxq = new sapi.api.ajaxq();

	this.default_options = {
		timeout: 60000,
		async: true,
		dataType: 'json',
		contentType: 'application/json',
		success: function( data, status, xhr ) {},
		error: function( xhr, textStatus, errorThrown ) {}

	};

	if ( options )
		this.default_options = jQuery.extend( {}, this.default_options, options );
}


sapi.api.restful.prototype = {

	_ajax : function( url, options, add_options ) {
		var newOptions = jQuery.extend( {}, this.default_options, options, add_options, { url : url } );
		this.ajaxq.ajax( "_api", newOptions );
	},

	_delete : function( url, options ) {
		this._ajax( url, options, { type : 'DELETE' } );
	},

	_get : function( url, options ) {
		this._ajax( url, options, { type : 'GET' } );
	},

	_post : function( url, data, options ) {
		this._ajax( url, options,
			{
				type : 'POST',
				data : JSON.stringify( data )
			}
		);
	},

	_put : function( url, data, options ) {
		this._ajax( url, options,
			{
				type : 'PUT',
				data : JSON.stringify( data )
			}
		);
	},

	/* ************ API ************************************* */

	getOrganizationList : function( success, error ) {
		this._get(
			'/api/restful/org',
			{ success: success, error: error }
		);
	},

	getOrganization : function( ref, success, error ) {
		this._get(
			'/api/restful/org/{0}'.sapi_format( ref.oid ),
			{ success: success, error: error }
		);
	},

	updateOrganization : function( ref, data, success, error ) {
		this._put(
			'/api/restful/org/{0}'.sapi_format( ref.oid ),
			data,
			{ success: success, error: error }
		);
	},

	getClientList : function( ref, success, error ) {
		this._get(
			'/api/restful/org/{0}/clients'.sapi_format( ref.oid ),
			{ success: success, error: error }
		);
	},

	getClient : function( ref, success, error ) {
		this._get(
			'/api/restful/org/{0}/client/{1}'.sapi_format( ref.oid, ref.cid ),
			{ success: success, error: error }
		);
	},

	updateClient : function( ref, data, success, error ) {
		this._put(
			'/api/restful/org/{0}/client/{1}'.sapi_format( ref.oid, ref.cid ),
			data,
			{ success: success, error: error }
		);
	},


	getProjectList : function( ref, success, error ) {
		this._get(
			'/api/restful/org/{0}/client/{1}/projects'.sapi_format( ref.oid, ref.cid ),
			{ success: success, error: error }
		);
	},

	getProject : function( ref, success, error ) {
		this._get(
			'/api/restful/org/{0}/client/{1}/project/{2}'.sapi_format( ref.oid, ref.cid, ref.pid ),
			{ success: success, error: error }
		);
	},

	getActivityList : function( ref, success, error ) {
		this._get(
			'/api/restful/org/{0}/activities'.sapi_format( ref.oid ),
			{ success: success, error: error }
		);
	},

	getActivity : function( ref, success, error ) {
		this._get(
			'/api/restful/org/{0}/activity/{1}'.sapi_format( ref.oid, ref.actid ),
			{ success: success, error: error }
		);
	},

	getTaskList : function( ref, success, error ) {
		this._get(
			'/api/restful/org/{0}/activity/{1}/tasks'.sapi_format( ref.oid, ref.actid ),
			{ success: success, error: error }
		);
	},

	getTask : function( ref, success, error ) {
		this._get(
			'/api/restful/org/{0}/activity/{1}/task/{2}'.sapi_format( ref.oid, ref.actid, ref.taskid ),
			{ success: success, error: error }
		);
	},

}


