
def enum(*args, **kwargs):
	return type('Enum', (object), dict((y, x) for x, y in enumerate(args), **kwargs)) 


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

	def __getattr__( self, name ):
		return object.__getattribute__( self, "_vals" )[ name ][ 0 ]

	def __setattr__( self, name, value ):
		object.__setattr__( self, "_vals" )[ name ][ 0 ] = value

	def __delattr__( self, name ):
		del object.__setattr__( self, "_vals" )[ name ]



