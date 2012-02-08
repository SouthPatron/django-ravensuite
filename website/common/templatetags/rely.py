from django import template
from django.conf import settings

from common.busobj.org.factory import Factory

register = template.Library()



rely_graph = {

	'reset' : {
			'js' : [],
			'css' : [ 'stylesheets/reset.css' ],
			'deps' : []
		},

	'date' : {
			'js' : [ 'js/external/date/date.js' ],
			'css' : [],
			'deps' : []
		},


	'jquery' : {
			'js' : [ 'js/external/jquery/jquery.js' ],
			'css' : [],
			'deps' : []
		},


	'jquery.ui' : {
			'js' : [ 'js/external/jquery.ui/jquery-ui.custom.min.js' ],
			'css' : [ 'js/external/jquery.ui/css/jquery-ui.custom.css' ],
			'deps' : []
		},


	'afes' : {
			'js' : [ 'js/internal/afes/afes.js' ],
			'css' : [ ],
			'deps' : [ 'jquery', 'date' ]
		},


	'afes-table' : {
			'js' : [ 'js/internal/afes/afes-table.js' ],
			'css' : [ ],
			'deps' : [ 'afes' ]
		},

}


class RelyOn( template.Node ):
	def __init__( self, deps ):
		self.deps = deps
		self.seen = {}


	def sub_render( self, name ):

		if name in self.seen:
			return ''		# nop

		ans = '\n'

		if name in rely_graph:
			for dep in rely_graph[ name ][ 'deps' ]:
				rc = self.sub_render( dep )
				ans = '{}{}'.format( ans, rc )

			for js in rely_graph[ name ][ 'js' ]:
				ans = '{}\n<script type="text/javascript" src="{}"></script>'.format( ans, js )


			for css in rely_graph[ name ][ 'css' ]:
				ans = '{}\n<link rel="stylesheet" type="text/css" href="{}" media="screen" />'.format( ans, css )


		self.seen[ name ] = True
		return ans

		


	def render( self, context ):

		ans = ''

		for dep in self.deps.split():
			rc = self.sub_render( dep )
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


