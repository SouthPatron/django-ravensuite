
import pkg_resources
version = pkg_resources.require( 'django-ravensuite' )[0].version

assets = {
	'ravensuite-core' :	{
		'output' : 'ravensuite-core-{}.min.js'.format( version ),
		'files' : [
				'scripts/ravensuite/json2.js',
				'scripts/ravensuite/jquery.js',
				'scripts/ravensuite/underscore.js',
				'scripts/ravensuite/backbone.js',
				'scripts/ravensuite/backbone-tastypie.js',
				'scripts/ravensuite/backbone-relational.js',
				'scripts/ravensuite/handlebars.js',
				'scripts/ravensuite/moment.min.js',
				'scripts/ravensuite/oss.js',
				'scripts/ravensuite/bootstrap/js/bootstrap.js',
				'scripts/ravensuite/bootbox.min.js',
				'scripts/ravensuite/datepicker/js/bootstrap-datepicker.js',
				'scripts/ravensuite/util.js',
		],
	},

	'ravensuite-css' : {
		'files' : [
			'scripts/ravensuite/bootstrap/css/bootstrap.css',
			'scripts/ravensuite/datepicker/css/datepicker.css',
		],
	},
}
