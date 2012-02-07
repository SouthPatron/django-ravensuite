
(function( $ ){

var settings = {
	'holaSenior' : 'red'
};


function performFormDescription( elem ) {
	elem.children( 'p' ).addClass( 'jFormDescription' );
}

function performFocusHighlight( elem ) {
	elem.find( 'div.JFFOCUSHIGHLIGHT' ).each( function(index,domEle) {

		var highlightTarget = $(this);

		$(this).find( ':input' ).each( function(index,domEle) {

			$(this).focus( function() {
				$(highlightTarget).addClass( 'jFormComponentHighlight' );
			});

			$(this).blur( function() {
				$(highlightTarget).removeClass( 'jFormComponentHighlight' );
			});
		});
	});
}

function performFields( elem ) {
	elem.find( 'div.JFFIELD' ).has( 'input[type="text"],input[type="password"],select' ).addClass('jFormComponent jFormComponentSingleLineText').each( function(index,domEle) {

		$(this).children( 'label' ).each( function(index, domEle) {

			if ($(this).hasClass( 'JFREQUIRED' ) )
				$(this).append( '<span class="jFormComponentLabelRequiredStar"> * </span>' );	

			$(this).addClass( 'jFormComponentLabel' );	
		});
	});

	elem.find( 'div.JFFIELD' ).has( 'input[type="checkbox"]' ).addClass('jFormComponent jFormComponentMultipleChoice').each( function(index,domEle) {

		$(this).children( 'label' ).each( function(index, domEle) {
			if ($(this).hasClass( 'JFREQUIRED' ) )
				$(this).append( '<span class="jFormComponentLabelRequiredStar"> * </span>' );	

			$(this).addClass('choiceLabel');
			$(this).parent().append( $(this).detach() );
		});
	});
}




function performGroupFields( elem ) {
	elem.find( 'div.JFGROUPFIELD' ).each( function(index,domEle) {

		$(this).children( 'label' ).each( function(index,domEle) {

			$(this).addClass( 'jFormComponentSublabel' );

			var extra = '';

			if ($(this).hasClass( 'JFREQUIRED' ) )
				extra = '<span class="jFormComponentLabelRequiredStar"> * </span>';

			$(this).parent().append( '<div class="jFormComponentSublabel"><p>' + $(this).text() + extra + '</p></div>' );
			$(this).detach();
		});
	});
}


function performGroups( elem ) {
	elem.find( 'div.JFGROUP' ).addClass( 'jFormComponent' ).each( function(index,domEle) {
		$(this).children( 'label' ).addClass( 'jFormComponentLabel' );
	});
}


function performInvalidIcons( elem ) {

	elem.find( 'div.JFINVALID' ).has( ':not(div:.JFINVALID)' ).children( 'label' ).each( function(index,domEle) {

		$(this).addClass( 'jFormComponentValidationFailed' );

	});


	elem.children( 'div:.JFGROUP' ).has( 'div:.JFINVALID' ).children( 'label' ).each( function(index,domEle) {

		$(this).addClass( 'jFormComponentValidationFailed' );

	});

	elem.children( 'div:not(.JFGROUP):.JFINVALID' ).children( 'label' ).each( function(index,domEle) {

		$(this).addClass( 'jFormComponentValidationFailed' );

	});
};



var methods = {
	init : function( options ) {
		if ( options ) {
			$.extend( settings, options );
		}

		return this;
	},

	formify : function() {
		this.addClass( 'jForms' );

		performFormDescription( this );
		performFields( this );
		performGroupFields( this );
		performFocusHighlight( this );
		performGroups( this );
		performInvalidIcons( this );

		this.wrapInner( '<div class="jFormSection" />' );
		return this;
	}
};

$.fn.jForms = function( method ) {

	if ( methods[method] ) {
		return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
	} else if ( typeof method === 'object' || ! method ) {
		return methods.init.apply( this, arguments );
	} else {
		$.error( 'Method ' +  method + ' does not exist on jQuery.jForms' );
	}    

};
})( jQuery );

