
def enum(*args, **kwargs):
	return type('Enum', (object,), dict((y, x) for x, y in enumerate(args), **kwargs)) 


class ChoicesEnum( object ):
	def __init__( self, *args, **kwargs ):
		super( ChoicesEnum, self ).__init__()
		vals = {}
		for key,val in kwargs.iteritems():
			vals[ key ] = val
		object.__setattr__( self, "_vals", vals )

	def choices( self ):
		cho = []
		for key, val in object.__getattribute__( self, "_vals" ).iteritems():
			cho.append( val )
		cho.sort()
		return cho

	def contains( self, needle ):
		for key, val in object.__getattribute__( self, "_vals" ).iteritems():
			if needle == val[0]:
				return True
		return False

	def set( self, name, val ):
		object.__getattribute__( self, "_vals" )[ name ] = val

	def get( self, value ):
		for key, val in object.__getattribute__( self, "_vals" ).iteritems():
			if value == val[0]:
				return val
		return None

	def get_by_display( self, value ):
		for key, val in object.__getattribute__( self, "_vals" ).iteritems():
			if value == val[1]:
				return val
		return None

	def __getattr__( self, name ):
		return object.__getattribute__( self, "_vals" )[ name ][ 0 ]

	def __setattr__( self, name, value ):
		object.__getattribute__( self, "_vals" )[ name ][ 0 ] = value

	def __delattr__( self, name ):
		del object.__setattr__( self, "_vals" )[ name ]



