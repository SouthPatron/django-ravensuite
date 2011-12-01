from django import template

register = template.Library()

@register.filter
def decshift( value ):
	try:
		return (float(value) / 100)
	except:
		return value



