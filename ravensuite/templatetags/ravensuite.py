from django import template
from django.conf import settings


register = template.Library()

@register.simple_tag
def raven_include_javascript( request, base ):

	if settings.DEBUG is True:
		return '<!-- DEBUG IS TRUE ' + base + ' -->'
	else:
		return '<!-- DEBUG IS false ' + base + ' -->'



