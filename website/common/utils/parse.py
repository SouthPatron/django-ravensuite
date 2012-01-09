

def pnumparse( val ):
	""" Parses formatted numbers with commas 

	"""
	newval = val
	newval = newval.replace( ',', '' )
	newval = newval.replace( ' ', '' )
	return long(float(newval) * 100)

