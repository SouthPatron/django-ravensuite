
from sptools.utils.dbgdatetime import datetime

def pnumparse( val ):
	""" Parses formatted numbers with commas 

	"""
	newval = val
	newval = newval.replace( ',', '' )
	newval = newval.replace( ' ', '' )
	return long(float(newval) * 100)


def pdateparse( val ):
	""" Parses dates of dd Month YYYY format

	"""
	return datetime.datetime.strptime( val, '%d %b %Y' )

def pdate( val ):
	return datetime.datetime.strftime( val, '%d %b %Y' )

