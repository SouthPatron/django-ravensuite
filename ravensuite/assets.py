
import pkg_resources
version = pkg_resources.require( 'django-ravensuite' )[0].version

assets = {
	'ravensuite-core' :	{
		'output' : 'ravensuite-core-{}.min.js'.format( version ),

		'order' : [
			'json2',
			'jquery',
			'underscore',
			'backbone',
			'backbone-tastypie',
			'backbone-relational',
			'handlebars',
			'moment',
			'oss',
			'bootstrap',
			'bootbox',
			'datepicker',
			'util',
			'highcharts',
		],

		'max_files' : {
			'json2' : 'scripts/ravensuite/json2.js',
			'jquery' : 'scripts/ravensuite/jquery.js',
			'underscore' : 'scripts/ravensuite/underscore.js',
			'backbone' : 'scripts/ravensuite/backbone.js',
			'backbone-tastypie' : 'scripts/ravensuite/backbone-tastypie.js',
			'backbone-relational' : 'scripts/ravensuite/backbone-relational.js',
			'handlebars' : 'scripts/ravensuite/handlebars.js',
			'moment' : 'scripts/ravensuite/moment.min.js',
			'oss' : 'scripts/ravensuite/oss.js',
			'bootstrap' : 'scripts/ravensuite/bootstrap/js/bootstrap.js',
			'bootbox' : 'scripts/ravensuite/bootbox.min.js',
			'datepicker' : 'scripts/ravensuite/datepicker/js/bootstrap-datepicker.js',
			'util' : 'scripts/ravensuite/util.js',
			'highcharts' : 'scripts/ravensuite/highcharts/js/highcharts.src.js',
		},
		'min_files' : {
			'highcharts' : 'scripts/ravensuite/highcharts/js/highcharts.js',
		},
	},

	'ravensuite-css' : {
		'files' : [
			'scripts/ravensuite/bootstrap/css/bootstrap.css',
			'scripts/ravensuite/datepicker/css/datepicker.css',
		],
	},
}
