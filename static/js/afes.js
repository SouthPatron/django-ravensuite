

/*
 *
 * Requires:
 * 
 *		. JavaScript Number
 *
 * 		. jQuery
 * 		. jQuery UI datepicker
 * 		. Date library
 */


/*
 * Settings Object passed to thingies
 *
 * 	behaviour
 *		next - string or function
 *		form_update - update a field in a form with the selector
 *
 *	hooks
 *		onFocus( event, value )
 *		onChange( event, oldVal, newVal )
 *		onEnter( event )
 *		onCancel( event )
 *		onNext( event )
 *		onFocusOut( event, val )
 *
 */


/*
 * Methods
 *
 *
 *  currencyInput( elem, settings );
 *  textInput( elem, settings );
 *
 *
 */



var afes = new function() {


	this.date_settings = {
		dateFormat: 'd M yy',
		onClose: function( theDate ) {
			requested_date = Date.parse( theDate );
			if ( requested_date != null )
				$(this).val( $.datepicker.formatDate( 'd M yy', requested_date ) );
			else
				$(this).val( $.datepicker.formatDate( 'd M yy', Date.today() ) );
		}
	}

	this.prepareDateInput = function( elem ) {
		$( elem ).datepicker( datesettings );
		return this;
	}

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

	this.ih.text = function() {}
	
	this.ih.text.activate = function( elem, event, opset ) {
		var dsval = $(elem).html();
		opset.scratchpad.original_value = dsval;

		var callbacks = opset.settings.callbacks;

		if ( callbacks.onFocus )
		{
			if ( callbacks.onFocus.call( elem, event, dsval ) === false )
			{
				$(elem).one(
					'click',
					{ 'opset' : opset },
					opset.functional.activate
				);
				return false;
			}
		}

		var sam = $( "<input/>", { text: "text", value: dsval } );

		$(elem).empty().append( sam );

		sam.focus()
			.focusout( { 'opset' : opset }, afes.stubs.ih.update )
			.keydown( { 'opset' : opset }, afes.stubs.ih.keystroke );

		return false;
	}


	this.ih.text.update = function( elem, event, opset ) {
		var dsval = $(elem).val();
		var callbacks = opset.settings.callbacks;

		if ( callbacks.onChange )
		{
			var rc = callbacks.onChange.call( elem, event, dsval );

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
			callbacks.onFocusOut.call( elem, event, dsval );

		return false;
	}

	this.ih.text.cancel = function( elem, event, opset ) {
		var dsval = $(elem).val();
		var callbacks = opset.settings.callbacks;

		if ( callbacks.onCancel )
		{
			var rc = callbacks.onCancel.call( elem, event, dsval );

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
				elem,
				event,
				opset.scratchpad.original_value
			);

		return false;

	}

	this.ih.text.keystroke = function( elem, event, opset ) {

		var callbacks = opset.settings.callbacks;
		var next = opset.settings.behaviour.next;

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

			var dc = opset.functional.update( elem, event, opset );

			if ( opset.settings.behaviour.next )
			{
				if ( typeof( opset.settings.behaviour.next ) === 'function' )
				{
					var rc = opset.settings.behaviour.next.call( this, event );
					if ( typeof( rc ) === 'string' )
						$( rc ).click();
				}
				else
				{
					$( opset.settings.behaviour.next ).click();
				}
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

	}


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
		return afes;
	}

}



