from django import template
from django.conf import settings


from ..assets import *

register = template.Library()

@register.simple_tag
def raven_js():
	rc = '<!-- raven_js: start, debug mode {} -->'.format( settings.DEBUG )

	if settings.DEBUG is True:

		for jsname in assets[ 'ravensuite-core' ][ 'order' ]:
			fname = assets['ravensuite-core' ][ 'max_files' ][ jsname ]
			rc = rc + '<script type="text/javascript" src="{}{}"></script>'.format( settings.STATIC_URL, fname )
	else:
		rc = rc + '<script type="text/javascript" src="{}{}{}"></script>'.format(
			settings.STATIC_URL,
			"scripts/ravensuite/",
			assets[ 'ravensuite-core' ][ 'output' ],
		)

	rc = rc + '<!-- raven_js: end -->'
	return rc


@register.simple_tag
def raven_css():
	rc = '<!-- raven_css: start, debug mode {} -->'.format( settings.DEBUG )

	for fname in assets[ 'ravensuite-css' ][ 'files' ]:
		rc = rc + '<link rel="stylesheet" href="{}{}" media="screen" />'.format( settings.STATIC_URL, fname )
			
	rc = rc + '<!-- raven_css: end -->'
	return rc


@register.tag(name='captureas')
def captureas(parser, token):
	try:
		tag_name, args = token.contents.split(None, 1)
	except ValueError:
		raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
	nodelist = parser.parse(('endcaptureas',))
	parser.delete_first_token()
	return CaptureasNode(nodelist, args)

class CaptureasNode(template.Node):
	def __init__(self, nodelist, varname):
		self.nodelist = nodelist
		self.varname = varname

	def render(self, context):
		output = self.nodelist.render(context)
		context[self.varname] = output
		return ''



@register.simple_tag
def isactive( request, pattern ):
	import re
	if re.search( pattern, request.path ):
		return 'active'
	return ''


@register.tag(name='ifapp')
def ifapp(parser, token):
	try:
		tag_name, args = token.contents.split(None, 1)
	except ValueError:
		raise template.TemplateSyntaxError("'ifapp' node requires an app name.")
	nodelist = parser.parse(('endifapp',))
	parser.delete_first_token()
	return IfAppNode(nodelist, args)

class IfAppNode(template.Node):
	def __init__(self, nodelist, appname):
		self.nodelist = nodelist
		self.appname = appname

	def render(self, context):
		from django.conf import settings
		if self.appname in settings.INSTALLED_APPS:
			return self.nodelist.render(context)
		return ''

@register.simple_tag
def settings_value( attrname ):
	from django.conf import settings
	return getattr( settings, attr, '' )

