from django import template
from django.conf import settings

register = template.Library()


ICON_REGISTRY = {
		'success' : { 'stub' : 'message_tick.png', },
		'error' : { 'stub' : 'message_error.png', },
		'info' : { 'stub' : 'message_info.png', },
		'warning' : { 'stub' : 'message_warning.png', },
	}


class ImageIcon( template.Node ):
	def __init__( self, names ):
		self.names = names

	def render( self, context ):
		ans = ''
		seen = {}
		for name in self.names.split():
			rc = '{}local/images/icons/{}'.format(
						settings.STATIC_URL,
						ICON_REGISTRY[ name ][ 'stub' ]
					)
			ans = '{}{}'.format( ans, rc )
		return ans


@register.tag( name='image_icon' )
def image_icon( parser, token ):
	""" Translates an icon's short name into a URL """
	try:
		tag_name, names = token.contents.split( None, 1 )
	except ValueError:
		raise template.TemplateSyntaxError( '{} tag requires arguments'.format( token.contents.split()[0] ) )

	return ImageIcon( names )



