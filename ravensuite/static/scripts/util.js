/* UTIL
 *
 * Global store of active objects or collections.
 *
 *
 *
 */

(function(){

	var root = this;
	var previousUTIL = root.UTIL;

	var UTIL;
	if (typeof exports !== 'undefined') {
		UTIL = exports;
	} else {
		UTIL = root.UTIL = {};
	}

	UTIL.VERSION = '0.0.1';
	var $ = root.jQuery;

	/* ------------------------------------------------------------- */

	var parseCurrency = UTIL.parseCurrency = function( amount ) {
		var wka = '' + amount;
		wka = wka.replace(/ /gi, '');
		wka = wka.replace(/,/gi, '');

		var flv = parseFloat( wka ) * 100;
		if ( isNaN( flv ) ) return 0;
		var tmp = parseInt( flv );
		if ( (flv - tmp) >= 0.5 ) tmp = tmp + 1;
		return ( tmp / 100 );
	}

	var formatCurrency = UTIL.formatCurrency = function( amount, options ) {
		var tsep = ( options && options[ 'separator' ] ) || ',';
		var str = '' + parseInt( amount ) + '.';
		var dec = parseInt( amount * 100 ) % 100;
		if ( dec < 10 ) str = str + '0';
		str = str + dec;

		var reg = new RegExp( '(\\d)(\\d\\d\\d)([.' + tsep + '])', 'gi' );

		for ( var i = 0; i < 128; i++ )
		{
			var wka = str.replace( reg, '$1' + tsep + '$2$3' );
			if ( wka == str ) return str;
			str = wka;
		}


		return str;
	}

	// Returns minutes
	var parseDuration = UTIL.parseDuration = function( duration ) {

		var dr = duration;
		dr = dr.replace(/hours|hour|hrs|hr|h|:/gi, 'h');
		dr = dr.replace(/minutes|minute|mins|min|m/gi, 'm');
		dr = dr.replace(/h+/gi, 'h');
		dr = dr.replace(/m+/gi, 'm');

		dr = dr.replace(/\s/g, '');			// single spaces

		if (match = /^(\d+)h(\d+)m$/.exec(dr)) {
			return parseInt(match[1]) * 60 + parseInt(match[2]);
		} else if (match = /^(\d+)h(\d+)$/.exec(dr)) {
			return parseInt(match[1]) * 60 + parseInt(match[2]);
		} else if (match = /^(\d+)h$/.exec(dr)) {
			return parseInt(match[1]) * 60;
		} else if (match = /^(\d+)\.(\d+)$/.exec(dr)) {
			return parseInt(match[1]) * 60 + parseInt( parseFloat( '0.' + match[2]) * 60 );
		} else if (match = /^\.(\d+)$/.exec(dr)) {
			return parseInt( parseFloat( '0.' + match[1]) * 60 );
		} else if (match = /^(\d+)m$/.exec(dr)) {
			return parseInt(match[1]);
		} else if (match = /^(\d+)$/.exec(dr)) {
			return parseInt(match[1]) * 60;
		} else {
			return null;
		}
	}

	// Takes minutes
	var formatDuration = UTIL.formatDuration = function( duration ) {
		var str = '';
		var rem = duration;

		if ( rem >= (60) )
		{
			str = str + parseInt(rem / 60) + 'h ';
		}

		rem = rem % (60);
		str = str + rem + 'm';
		return str;
	}

	var parseMonth = UTIL.parseMonth = function( month ) {
		if ( month.match( /^jan|january$/i ) ) return 0;
		if ( month.match( /^feb|february$/i ) ) return 1;
		if ( month.match( /^mar|march$/i ) ) return 2;
		if ( month.match( /^apr|april$/i ) ) return 3;
		if ( month.match( /^may$/i ) ) return 4;
		if ( month.match( /^jun|june$/i ) ) return 5;
		if ( month.match( /^jul|july$/i ) ) return 6;
		if ( month.match( /^aug|august$/i ) ) return 7;
		if ( month.match( /^sep|september$/i ) ) return 8;
		if ( month.match( /^oct|october$/i ) ) return 9;
		if ( month.match( /^nov|november$/i ) ) return 10;
		if ( month.match( /^dec|december$/i ) ) return 11;

		var now = new Date();
		return now.getMonth();
	}

	var parseYear = UTIL.parseYear = function( year ) {
		var myy = parseInt( year );
		if ( myy >= 1900 ) return myy;
		if ( (myy > 0) && (myy < 100) ) return myy + 2000;
		var now = new Date();
		return now.getFullYear();
	}

	// Returns minutes
	var parseDate = UTIL.parseDate = function( date ) {
		var now = new Date();

		if ( date === undefined ) return now;

		var dr = date;
		dr = dr.replace(/\s/g, '');			// single spaces

		var day = now.getDate();
		var month = now.getMonth();
		var year = now.getFullYear();

		var match;

		if (match = /^(\d+)(\D+)(\d+)$/.exec(dr)) {
			day = parseInt( match[1] );
			month = parseMonth( match[2] );
			year = parseYear( match[3] );
		} else if (match = /^(\d+)(\D+)$/.exec(dr)) {
			day = parseInt( match[1] );
			month = parseMonth( match[2] );
		} else if (match = /^(\d+)$/.exec(dr)) {
			day = parseInt( match[1] );
		}

		now.setFullYear( year );
		now.setMonth( month );
		now.setDate( day );
		return now;
	}

	// Takes minutes
	var formatDate = UTIL.formatDate = function( date ) {
		return moment( date ).format( 'DD MMM YYYY' );
	}

}).call(this);

