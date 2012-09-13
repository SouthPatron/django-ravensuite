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


