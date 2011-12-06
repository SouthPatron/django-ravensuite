from django import template

register = template.Library()

@register.filter
def decshift( value ):
	try:
		return (float(value) / 100)
	except:
		return value


@register.filter
def decshow( value ):
	try:
		val = long( value )
		newval = '{}.{:0>2}'.format( val / 100, val % 100 )
		return newval
	except:
		return value




@register.filter
def decsplay( value ):
	try:
		val = long( value )
		isNeg = ( val < 0 )
		val = abs( val )

		if val >= 100000:
			newval = '{:0>3}.{:0>2}'.format( (val / 100) % 1000, val % 100 )
		else:
			newval = '{}.{:0>2}'.format( (val / 100) % 1000, val % 100 )

		val = val / 100000

		while val > 0:
			if val > 1000:
				newval = '{:0>3},{}'.format( val % 1000, newval )
			else:
				newval = '{},{}'.format( val % 1000, newval )
			val = val / 1000

		if isNeg is True:
			newval = '-{}'.format( newval )

		return newval

	except:
		return value



