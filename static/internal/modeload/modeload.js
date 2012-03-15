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
 * 		. Crypto-JS.MD5
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

if (typeof Crypto == 'undefined') {
	alert( 'ERROR: (MODELOAD) modeload requires Crypto to be loaded' );
	exit();
}

if (typeof Crypto.MD5 == 'undefined') {
	alert( 'ERROR: (MODELOAD) modeload requires Crypto.MD5 to be loaded' );
	exit();
}



/* ------------------------------------------------------- */

modeload = {}

modeload.version = '1.0.0';


modeload.html = {}
modeload.html.static_post_data = {};

modeload.html.setStaticPostData = function( mydict ) {
	modeload.html.static_post_data = jQuery.extend( true, {}, mydict );
}

modeload.html.fetchObject = function( url, pdata, success ) {
	var newpdata = jQuery.extend( true, {}, modeload.html.static_post_data, pdata );
	jQuery.post( url, newpdata, function(data, textStatus, x) {
		success( data );
	});
}

modeload.html.applyObject = function( url, pdata, success ) {
	jQuery.post( url, pdata, function(data, textStatus, x) {
		success( data );
	});
}

modeload.html.createContainer = function( url ) {
	var digest = Crypto.MD5( url );

	$(document).find( "#" + digest ).detach();

	var newdiv = jQuery( '<div id="' + digest + '" class="modeload_container"><div class="ml_background">&nbsp;</div><div class="ml_box"></div>' );

	$(document).find( "body" ).append( newdiv );

	return newdiv;
}

modeload.html.destroyContainer = function( url ) {
	var digest = Crypto.MD5( url );
	var mybox = $(document).find( "#" + digest ).detach();
}

modeload.html.showContainer = function( url ) {
	var digest = Crypto.MD5( url );

	$(document).find( "#" + digest ).find( ".ml_box" ).css( "visibility", "visible" );
}

modeload.html.updateContainer = function( url, newhtml ) {
	var digest = Crypto.MD5( url );

	var mybox = $(document).find( "#" + digest ).find( ".ml_box" );

	var newcont = jQuery( newhtml );

	mybox.empty().append( newcont );

	var mleft = "-" + (mybox.outerWidth()/2) + "px";
	var mtop = "-" + (mybox.outerHeight()/2) + "px";

	mybox.css( 'margin-left' , mleft ).css( 'margin-top', mtop ).css( 'top', '50%' ).css( 'left', '50%' );
}

modeload.html.resizeContainerContent = function( url ) {
	var digest = Crypto.MD5( url );
	var mybox = $(document).find( "#" + digest ).find( ".ml_box" );
	var content = mybox.find( ".ml_dialog_content" );

	mybox.find( ".ml_dialog_buttonbar" ).each( function() {
		var buttonbar_height = $(this).outerHeight( true );
		mybox.find( ".ml_dialog_content" ).css( 'margin-bottom', buttonbar_height + 'px' );
	});
}

modeload.html.fetchContainer = function( url, pdata, success ) {
	modeload.html.fetchObject( url, pdata, function( obj ) {
		modeload.html.updateContainer( url, obj );
		modeload.html.resizeContainerContent( url );
		success( url );
	});
}

modeload.html.applyContainer = function( url, pdata, success ) {
	modeload.html.applyObject( url, pdata, function( obj ) {
		modeload.html.updateContainer( url, obj );
		success( url );
	});
}




modeload.html.hookContainer = function( url ) {
	var digest = Crypto.MD5( url );
	var mybox = $(document).find( "#" + digest ).find( ".ml_box" );

	// Draggable

	mybox.draggable( 
		{
			handle: '.ml_dialog_titlebar',
			opacity: 0.90
		}
	);

	// Form submission

	mybox.find( "form" ).submit( function( ev ) {
		ev.preventDefault();

		var newdata = $(this).serializeArray();

		modeload.html.applyContainer( url, newdata, function( url ) {
			modeload.html.showContainer( url );
			modeload.html.hookContainer( url );
		});

		return false;
	});

	// Actions

	mybox.find( ".ml_action_close" ).click( function() {
		modeload.html.destroyContainer( url );
	});

	mybox.find( ".ml_action_submit" ).click( function() {
		mybox.find( "form" ).submit();
	});

}


modeload.html.getContainer = function( url ) {
	var digest = Crypto.MD5( url );
	var mybox = $(document).find( "#" + digest ).first();
	return mybox;
}

modeload.html.keyUpHook = function( e ) {
	if (e.keyCode == 27)
	{
		var url = e.data.url;
		modeload.html.destroyContainer( url );
		$(document).unbind( "keyup", modeload.html.keyUpHook );
	} 
}

modeload.html.load = function( url, pdata ) {

	if ( ! pdata ) var pdata = {};

	var newdiv = modeload.html.createContainer( url );

	modeload.html.fetchContainer( url, pdata, function( url ) {
		modeload.html.showContainer( url );
		modeload.html.hookContainer( url );

		$(document).keyup( { 'url' : url }, modeload.html.keyUpHook );
	});

}



