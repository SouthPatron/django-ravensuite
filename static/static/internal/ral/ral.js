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
 * 		. jQuery UI
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
	alert( 'ERROR: (RAL) ral requires jQuery to be loaded' );
	exit();
}

if ( jQuery.fn.jquery < '1.6.2' ) {
	alert( 'ERROR: (RAL) ral has only been tested against jQuery 1.6.2. Please upgrade.' );
	exit();
}

if (typeof Crypto == 'undefined') {
	alert( 'ERROR: (RAL) ral requires Crypto to be loaded' );
	exit();
}

if (typeof Crypto.MD5 == 'undefined') {
	alert( 'ERROR: (RAL) ral requires Crypto.MD5 to be loaded' );
	exit();
}



/* ------------------------------------------------------- */

ral = {}
ral.version = '1.0.0';

ral.html = {}

ral.html.fetchObject = function( url, pdata, success ) {
	jQuery.get( url, pdata, function(data, textStatus, x) {
		success( data );
	});
}

ral.html.applyObject = function( url, pdata, success ) {
	jQuery.post( url, pdata, function(data, textStatus, x) {
		success( data );
	});
}

ral.html.createContainer = function( url ) {
	var digest = Crypto.MD5( url );

	$(document).find( "#" + digest ).detach();

	var newdiv = jQuery( '<div id="' + digest + '" class="ral_container"><div class="ral_background">&nbsp;</div><div class="ral_box"></div>' );

	$(document).find( "body" ).append( newdiv );

	return newdiv;
}

ral.html.destroyContainer = function( url ) {
	var digest = Crypto.MD5( url );
	var mybox = $(document).find( "#" + digest ).detach();
}

ral.html.showContainer = function( url ) {
	var digest = Crypto.MD5( url );

	$(document).find( "#" + digest ).find( ".ral_box" ).css( "visibility", "visible" );
}

ral.html.updateContainer = function( url, newhtml ) {
	var digest = Crypto.MD5( url );

	var mybox = $(document).find( "#" + digest ).find( ".ral_box" );

	var newcont = jQuery( newhtml );

	mybox.empty().append( newcont );

	var mleft = "-" + (mybox.outerWidth()/2) + "px";
	var mtop = "-" + (mybox.outerHeight()/2) + "px";

	mybox.css( 'margin-left' , mleft ).css( 'margin-top', mtop );

	var wleft = "" + ($(window).width() / 2) + "px";
	var wtop = "" + ($(window).height() / 2) + "px";
	
	mybox.css( 'top', wtop ).css( 'left', wleft );
}

ral.html.resizeContainerContent = function( url ) {
	var digest = Crypto.MD5( url );
	var mybox = $(document).find( "#" + digest ).find( ".ral_box" );

	if ( mybox ) {
		// Set Margin if buttonbar is present
		var botmargin = 0;
		mybox.find( ".ral_dialog_buttonbar" ).each( function() {
			botmargin += $(this).outerHeight( true );
		});
		mybox.find( ".ral_dialog_content" ).css( 'margin-bottom', botmargin + 'px' );

		// Set Height
		var availableHeight = mybox.height();

		mybox.find( ".ral_dialog_titlebar" ).each( function() {
			availableHeight -= $(this).outerHeight( true );
		});

		mybox.find( ".ral_dialog_buttonbar" ).each( function() {
			availableHeight -= $(this).outerHeight( true );
		});

		mybox.find( ".ral_dialog_content" ).height( availableHeight  );
	}
}

ral.html.fetchContainer = function( url, pdata, success ) {
	ral.html.fetchObject( url, pdata, function( obj ) {
		ral.html.updateContainer( url, obj );
		ral.html.resizeContainerContent( url );
		success( url );
	});
}

ral.html.applyContainer = function( url, pdata, success ) {
	ral.html.applyObject( url, pdata, function( obj ) {
		ral.html.updateContainer( url, obj );
		ral.html.resizeContainerContent( url );
		success( url );
	});
}



ral.html.hookContainer = function( url ) {
	var digest = Crypto.MD5( url );
	var mybox = $(document).find( "#" + digest ).find( ".ral_box" );

	// Draggable

	mybox.draggable( 
		{
			handle: '.ral_dialog_titlebar',
			opacity: 0.90
		}
	);

	// Form submission

	mybox.find( "form" ).submit( function( ev ) {
		ev.preventDefault();

		mybox.find( ".ral_dialog_buttonbar button" ).attr("disabled", "true");

		var newdata = $(this).serializeArray();

		ral.html.applyContainer( url, newdata, function( url ) {
			ral.html.showContainer( url );
			ral.html.hookContainer( url );
		});

		return false;
	});

	// Actions

	mybox.find( ".ral_action_close" ).click( function() {
		ral.html.destroyContainer( url );
	});

	mybox.find( ".ral_action_submit" ).click( function() {
		mybox.find( "form" ).submit();
	});
}


ral.html.getContainer = function( url ) {
	var digest = Crypto.MD5( url );
	var mybox = $(document).find( "#" + digest ).first();
	return mybox;
}

ral.html.keyUpHook = function( e ) {
	if (e.keyCode == 27)
	{
		var url = e.data.url;
		ral.html.destroyContainer( url );
		$(document).unbind( "keyup", ral.html.keyUpHook );
	} 
}

ral.html.fetch = function( url, pdata ) {

	if ( ! pdata ) var pdata = {};

	var newdiv = ral.html.createContainer( url );

	ral.html.fetchContainer( url, pdata, function( url ) {
		ral.html.showContainer( url );
		ral.html.hookContainer( url );

		$(document).keyup( { 'url' : url }, ral.html.keyUpHook );
	});
}

ral.html.post = function( url, pdata ) {

	if ( ! pdata ) var pdata = {};

	var newdiv = ral.html.createContainer( url );

	ral.html.applyContainer( url, pdata, function( url ) {
		ral.html.showContainer( url );
		ral.html.hookContainer( url );

		$(document).keyup( { 'url' : url }, ral.html.keyUpHook );
	});
}

ral.html.load = function( url, pdata ) {
	ral.html.fetch( url, pdata );
}



