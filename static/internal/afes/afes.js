/* Afes - Advanced Field Entering System
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
 *		. JavaScript Number
 * 		. jQuery
 * 		. jQuery UI datepicker
 * 		. Date library
 */


/*
 * Settings Object passed to thingies
 *
 * 	behaviour
 *		next - string or function. Function looks like:
 *				function (event)
 *					this = elem container
 *		form_update - update a field in a form with the selector
 *
 *	options	- array or object (kvp) with selections
 *
 *	callbacks
 *		onFocus( event, val )
 *				return:
 *					true - proceed with value
 *					false - do not allow focus
 *					<string> - value to replace val
 *
 *		onUpdate( event, oldVal, newVal )
 *				return:
 *					true - proceed with new value
 *					false - do not allow update
 *					<string> - value to replace new value
 *		onChange( event, val )
 *		onEnter( event )
 *		onCancel( event )
 *		onNext( event )
 *		onFocusOut( event, val )
 *
 * CSS classes:
 *
 * 	afes-input
 *
 * 	afes-input-type-text
 * 	afes-input-type-currency
 * 	afes-input-type-select
 * 	afes-input-type-date
 *
 *
 * 
 *
 */


/*
 * Methods
 *
 *
 *  currencyInput( elem, settings );
 *  textInput( elem, settings );
 *  selectInput( elem, settings, options );
 *
 *
 */


/* ----------------- Dependency Checks ------------------- */

if (typeof jQuery == 'undefined') {
	alert( 'ERROR: (AFES) afes requires jQuery to be loaded' );
	exit();
}

if ( jQuery.fn.jquery < '1.6.2' ) {
	alert( 'ERROR: (AFES) afes has only been tested against jQuery 1.6.2. Please upgrade.' );
	exit();
}

if ( typeof jQuery().datepicker == 'undefined' ) {
	alert( 'ERROR: (AFES) afes requires the jQuery datepicker plugin.' );
	exit();
}

if ( typeof Date == 'undefined' ) {
	alert( 'ERROR: (AFES) afes requires the Date javascript library' );
	exit();
}

/* ------------------------------------------------------- */

var afes = new function() {

	this.version = '1.0.0';


	this.numberize = function( val ) {
		if ( isNaN( val ) ) return (new Number( '0.00')).toFixed(2);
		return (new Number(val)).toFixed(2);
	}

	// ----------------- Stubs ------------------------------------------


	this.stubs = function() {}
	this.stubs.ih = function() {}

	this.stubs.ih._cleanOpset = function( opset ) {
		if ( ! opset ) opset = {};
		if ( ! opset.functional ) opset.functional = {};
		if ( ! opset.settings ) opset.settings = {};
		if ( ! opset.settings.behaviour ) opset.settings.behaviour = {};
		if ( ! opset.settings.callbacks ) opset.settings.callbacks = {};
		if ( ! opset.settings.options ) opset.settings.options = {};

		if ( ! opset.scratchpad ) opset.scratchpad = {};
		if ( ! opset.scratchpad.original_value ) opset.scratchpad.original_value = "";

		return opset
	}

	this.stubs.ih.activate = function( event ) {
		var opset = afes.stubs.ih._cleanOpset( event.data[ 'opset' ] );
		return opset.functional.activate( $(this), event, opset );
	}

	this.stubs.ih.update = function( event ) {
		var opset = afes.stubs.ih._cleanOpset( event.data[ 'opset' ] );
		return opset.functional.update( $(this), event, opset );
	}

	this.stubs.ih.cancel = function( event ) {
		var opset = afes.stubs.ih._cleanOpset( event.data[ 'opset' ] );
		return opset.functional.cancel( $(this), event, opset );
	}

	this.stubs.ih.keystroke = function( event ) {
		var opset = afes.stubs.ih._cleanOpset( event.data[ 'opset' ] );
		return opset.functional.keystroke( $(this), event, opset );
	}



	// ----------------- Interface Human ------------------------------------


	this.ih = function() {}


	//						TEXT ------------------------------------------

	this.ih.text = function() {}
	
	this.ih.text.activate = function( elem, event, opset ) {
		var dsval = $(elem).html();
		opset.scratchpad.original_value = dsval;

		var callbacks = opset.settings.callbacks;

		if ( callbacks.onFocus )
		{
			var rc = callbacks.onFocus.call( elem, event, dsval );
			
			if ( rc === false )
			{
				$(elem).one(
					'click',
					{ 'opset' : opset },
					opset.functional.activate
				);
				return false;
			}

			if ( rc !== true ) dsval = rc;
		}

		var sam = $( "<input/>", { text: "text", value: dsval } );

		$(elem).empty().append( sam );

		sam.focus()
			.focusout( { 'opset' : opset }, afes.stubs.ih.update )
			.keydown( { 'opset' : opset }, afes.stubs.ih.keystroke )
			.select();

		return false;
	}


	this.ih.text.update = function( elem, event, opset ) {
		var dsval = $(elem).val();
		var callbacks = opset.settings.callbacks;

		if ( callbacks.onUpdate )
		{
			var rc = callbacks.onUpdate.call(
						elem,
						event,
						opset.scratchpad.original_value,
						dsval
					);

			if ( rc === false )
			{
				$(elem).one( 'click', { 'opset' : opset }, afes.stubs.ih.activate);
				return false;
			}

			if ( rc && rc !== true ) dsval = rc;
		}

		// Update forms entries, if specified.
		if ( opset.settings.behaviour.form_update )
			$( opset.settings.behaviour.form_update ).val( dsval );

		var par = $(elem).parent();

		par
			.empty()
			.html( dsval )
			.one( 'click', { 'opset' : opset }, afes.stubs.ih.activate );

		if ( callbacks.onFocusOut )
			callbacks.onFocusOut.call( par, event, dsval );

		return false;
	}

	this.ih.text.cancel = function( elem, event, opset ) {
		var dsval = $(elem).val();
		var callbacks = opset.settings.callbacks;

		if ( callbacks.onCancel )
		{
			var rc = callbacks.onCancel.call( elem, event );

			if ( rc === false )
			{
				$(elem).one( 'click', { 'opset' : opset }, afes.stubs.ih.activate);
				return false;
			}
		}

		var par = $(elem).parent();

		par
			.empty()
			.html( opset.scratchpad.original_value )
			.one( 'click', { 'opset' : opset }, afes.stubs.ih.activate );


		if ( callbacks.onFocusOut )
			callbacks.onFocusOut.call(
				par,
				event,
				opset.scratchpad.original_value
			);

		return false;

	}

	this.ih.text.keystroke = function( elem, event, opset ) {

		var callbacks = opset.settings.callbacks;
		var next = opset.settings.behaviour.next;
		var original_value = opset.scratchpad.original_value;

		// KEY: Enter

		if ( event.keyCode == '13') {
			event.preventDefault();

			if ( callbacks.onEnter )
				if ( callbacks.onEnter.call( elem, event ) === false )
					return false;

			return opset.functional.update( elem, event, opset );
		}

		// KEY: Tab

		if ( event.keyCode == '9') {
			event.preventDefault();

			if ( callbacks.onNext )
				if ( callbacks.onNext.call( elem, event ) === false )
					return false;

			var par = elem.parent();

			var dc = opset.functional.update( elem, event, opset );

			if ( opset.settings.behaviour.next )
			{
				var rc = opset.settings.behaviour.next;

				if ( typeof( opset.settings.behaviour.next ) === 'function' )
				{
					rc = opset.settings.behaviour.next.call( par, event );
				}

				if ( rc !== false ) $( rc ).click();
			}

			return dc;
		}

		// KEY: Escape

		if ( event.keyCode == '27') {
			event.preventDefault();

			if ( callbacks.onCancel )
				if ( callbacks.onCancel.call( elem, event ) === false )
					return false;

			return opset.functional.cancel( elem, event, opset );
		}


		if ( callbacks.onChange ) {
			var newval = elem.val();
			if ( newval != original_value )
				callbacks.onChange.call( elem, event, newval );
		}
	}


	//						CURRENCY --------------------------------------


	this.ih.currency = function() {}
	
	this.ih.currency.activate = function( elem, event, opset ) {
		var dsval = afes.numberize( $(elem).html() );
		$(elem).html( dsval );
		return afes.ih.text.activate( elem, event, opset );
	}

	this.ih.currency.update = function( elem, event, opset ) {
		var dsval = afes.numberize( $(elem).val() );
		$(elem).val( dsval );
		return afes.ih.text.update( elem, event, opset );
	}


	//						SELECT BOX ------------------------------------


	this.ih.select = function() {}
	
	this.ih.select.activate = function( elem, event, opset ) {
		var dsval = $(elem).html();
		opset.scratchpad.original_value = dsval;

		var callbacks = opset.settings.callbacks;

		if ( callbacks.onFocus )
		{
			var rc = callbacks.onFocus.call( elem, event, dsval );

			if ( rc === false )
			{
				$(elem).one(
					'click',
					{ 'opset' : opset },
					opset.functional.activate
				);
				return false;
			}

			if ( rc !== true ) dsval = rc;
		}

		var sam = $( "<select/>" );

		for ( key in opset.settings.options )
		{
			var opsie = $( "<option/>", { value : opset.settings.options[key] } );

			if ( dsval == key )
				opsie.attr( 'selected', 1 );

			opsie.html( key );
			sam.append( opsie );
		}

		$(elem).empty().append( sam );

		sam.focus()
			.focusout( { 'opset' : opset }, afes.stubs.ih.update )
			.keydown( { 'opset' : opset }, afes.stubs.ih.keystroke );

		return false;
	}


	this.ih.select.update = function( elem, event, opset ) {
		var dsval = $(elem).val();
		var callbacks = opset.settings.callbacks;

		if ( callbacks.onUpdate )
		{
			var rc = callbacks.onUpdate.call(
						elem,
						event,
						opset.scratchpad.original_value,
						dsval
					);


			if ( rc === false )
			{
				$(elem).one( 'click', { 'opset' : opset }, afes.stubs.ih.activate);
				return false;
			}

			if ( rc && rc !== true ) dsval = rc;
		}

		// Update forms entries, if specified.
		if ( opset.settings.behaviour.form_update )
			$( opset.settings.behaviour.form_update ).val( dsval );

		var par = $(elem).parent();
		var text = $(elem).find(":selected").html();

		par
			.empty()
			.html( text )
			.one( 'click', { 'opset' : opset }, afes.stubs.ih.activate );

		if ( callbacks.onFocusOut )
			callbacks.onFocusOut.call( par, event, dsval );

		return false;
	}



	//						DATE INPUT ------------------------------------


	this.ih.date = function() {}
	
	this.ih.date.activate = function( elem, event, opset ) {
		var dsval = Date.parse( $(elem).html() );
		if ( dsval == null ) dsval = Date.today();
		dsval = dsval.toString( "d MMM yyyy" );
		$(elem).html( dsval );
		return afes.ih.text.activate( elem, event, opset );
	}

	this.ih.date.update = function( elem, event, opset ) {

		var gooba = $(elem).val();

		var dsval = Date.parse( gooba );
		if ( dsval == null ) dsval = Date.parse( opset.scratchpad.original_value );
		dsval = dsval.toString( "d MMM yyyy" );

		$(elem).val( dsval );
		return afes.ih.text.update( elem, event, opset );
	}


	// ----------------- Methods ----------------------------------------


	this.textInput = function( elem, thesettings ) {

		var opset = {
			functional : {
				activate : afes.ih.text.activate,
				update : afes.ih.text.update,
				cancel : afes.ih.text.cancel,
				keystroke : afes.ih.text.keystroke
			},
			settings : thesettings
		};

		$( elem ).one( 'click', { 'opset' : opset }, afes.stubs.ih.activate );

		$( elem ).addClass( 'afes-input' );
		$( elem ).addClass( 'afes-input-type-text' );

		return afes;
	}

	this.currencyInput = function( elem, thesettings ) {

		var opset = {
			functional : {
				activate : afes.ih.currency.activate,
				update : afes.ih.currency.update,
				cancel : afes.ih.text.cancel,
				keystroke : afes.ih.text.keystroke
			},
			settings : thesettings
		};

		$( elem ).one( 'click', { 'opset' : opset }, afes.stubs.ih.activate );

		$( elem ).addClass( 'afes-input' );
		$( elem ).addClass( 'afes-input-type-currency' );

		return afes;
	}

	this.selectInput = function( elem, thesettings ) {

		var opset = {
			functional : {
				activate : afes.ih.select.activate,
				update : afes.ih.select.update,
				cancel : afes.ih.text.cancel,
				keystroke : afes.ih.text.keystroke
			},
			settings : thesettings
		};

		$( elem ).one( 'click', { 'opset' : opset }, afes.stubs.ih.activate );

		$( elem ).addClass( 'afes-input' );
		$( elem ).addClass( 'afes-input-type-select' );

		return afes;
	}


	this.dateInput = function( elem, thesettings ) {
		
		var opset = {
			functional : {
				activate : afes.ih.date.activate,
				update : afes.ih.date.update,
				cancel : afes.ih.text.cancel,
				keystroke : afes.ih.text.keystroke
			},
			settings : thesettings
		};


		$( elem ).one( 'click', { 'opset' : opset }, afes.stubs.ih.activate );

		$( elem ).addClass( 'afes-input' );
		$( elem ).addClass( 'afes-input-type-date' );
		return afes;
	}



}



