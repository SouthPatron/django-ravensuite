import os.path

from django import template
from django.conf import settings

from common.busobj.org.factory import Factory
from common.utils.enum import enum

register = template.Library()

RL = enum( 'IN', 'EX', 'CU' );

def get_address( lotype, fname ):
	if lotype == RL.IN:
		inex = 'internal'
	elif lotype == RL.EX:
		inex = 'external'
	elif lotype == RL.CU:
		inex = 'custom'

	return os.path.join( settings.STATIC_URL, inex, fname )


def pi( fname ):
	return get_address( RL.IN, fname )

def pe( fname ):
	return get_address( RL.EX, fname )

def pc( fname ):
	return get_address( RL.CU, fname )


rely_graph = {

	'reset' : {
			'js' : [],
			'css' : [ pe( 'reset/css/reset.css' ) ],
			'deps' : []
		},

	'superfish' : {
		'js' : [
				pe( 'jquery.superfish/superfish.js' ),
				pe( 'jquery.superfish/supersubs.js' ),
				pe( 'jquery.superfish/hoverIntent.js' )
			],
		'css' : [ pe( 'jquery.superfish/css/superfish.css' ), ],
		'deps' : [ 'jquery' ]
		},

	'superfish-navbar' : {
		'js' : [],
		'css' : [ pe( 'jquery.superfish/css/superfish-navbar.css' ), ],
		'deps' : [ 'superfish' ]
		},

	'superfish-vertical' : {
		'js' : [],
		'css' : [ pe( 'jquery.superfish/css/superfish-vertical.css' ), ],
		'deps' : [ 'superfish' ]
		},

	'date' : {
			'js' : [ pe( 'date/date.js' ) ],
			'css' : [],
			'deps' : []
		},

	'jquery' : {
			'js' : [ pe( 'jquery/jquery.js' ) ],
			'css' : [],
			'deps' : []
		},

	'jquery.ui' : {
			'js' : [ pe( 'jquery.ui/jquery-ui.custom.min.js' ) ],
			'css' : [ pe( 'jquery.ui/css/jquery-ui.custom.css' ) ],
			'deps' : [ 'jquery' ]
		},

	'jquery.tools' : {
			'js' : [ pe( 'jquery.tools/jquery.tools.min.js' ) ],
			'css' : [],
			'deps' : [ 'jquery' ]
		},

	'afes' : {
			'js' : [ pi( 'afes/afes.js' ) ],
			'css' : [],
			'deps' : [ 'jquery', 'date' ]
		},

	'afes-table' : {
			'js' : [ pi( 'afes/afes-table.js' ) ],
			'css' : [],
			'deps' : [ 'afes' ]
		},

	'formfit' : {
			'js' : [ pi( 'formfit/formfit.js' ) ],
			'css' : [ pi( 'formfit/css/formfit.css' ) ],
			'deps' : [ 'jquery.ui', 'jquery.tools' ]
		},

	'datatables' : {
			'js' : [ pe( 'jquery.datatables/jquery.dataTables.min.js' ) ],
			'css' : [
				pe( 'jquery.datatables/css/datatables.css' ),
				pc( 'jquery.datatables/css/datatables.css' ),
			],
			'deps' : [ 'jquery' ]
		},


	'modeload' : {
			'js' : [
				pi( 'modeload/modeload.js' ),
			],
			'css' : [],
			'deps' : [ 'jquery' ]
		},

	'sitekit' : {
			'js' : [
				pc( 'sitekit/string.js' ),
				pc( 'sitekit/sitekit.js' ),
				pc( 'sitekit/ood.js' ),
				pc( 'sitekit/smktools.js' ),
				pc( 'sitekit/validations.js' )
			],
			'css' : [
				pc( 'sitekit/css/smktools.css' ),
			],
			'deps' : [ 'jquery' ]
		}
}


def sub_render( name, seen ):
	if name in seen:
		return ''		# nop

	ans = '\n'

	# TODO: This should maybe be more tolerant one day
	if name not in rely_graph:
		raise KeyError( 'No such rely option: {}'.format( name ) )

	for dep in rely_graph[ name ][ 'deps' ]:
		rc = sub_render( dep, seen )
		ans = '{}{}'.format( ans, rc )

	for js in rely_graph[ name ][ 'js' ]:
		ans = '{}\n<script type="text/javascript" src="{}"></script>'.format( ans, js )

	for css in rely_graph[ name ][ 'css' ]:
		ans = '{}\n<link rel="stylesheet" type="text/css" href="{}" media="screen" />'.format( ans, css )

	seen[ name ] = True
	return ans



class RelyOn( template.Node ):
	def __init__( self, deps ):
		self.deps = deps

	def render( self, context ):
		ans = ''
		seen = {}
		for dep in self.deps.split():
			rc = sub_render( dep, seen )
			ans = '{}{}'.format( ans, rc )
		return ans


@register.tag( name='rely' )
def rely( parser, token ):
	""" Brings in javascript, css, etc files as needed into a template.

	"""
	try:
		tag_name, deps = token.contents.split( None, 1 )
	except ValueError:
		raise template.TemplateSyntaxError( '{} tag requires arguments'.format( token.contents.split()[0] ) )

	return RelyOn( deps )




class RelyOnIndirect( template.Node ):
	def __init__( self, deps ):
		self.deps = template.Variable( deps )
	
	def render( self, context ):
		try:
			deps = self.deps.resolve( context )
		except:
			pass

		ans = ''
		seen = {}
		for dep in deps.split():
			rc = sub_render( dep, seen )
			ans = '{}{}'.format( ans, rc )
		return ans

@register.tag( name='relyindirect' )
def relyindirect( parser, token ):
	""" Encapsulates the SourceDocument model provided into a Business Object.

	"""

	try:
		tag_name, deps = token.contents.split( None, 1 )
	except ValueError:
		raise template.TemplateSyntaxError( '{} tag requires arguments'.format( token.contents.split()[0] ) )

	return RelyOnIndirect( deps )

