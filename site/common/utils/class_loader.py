
import logging

logger = logging.getLogger( __name__ )

class ClassLoader( object ):

	@staticmethod
	def load( full_path ):
		parts = full_path.split('.')

		try:
			m = __import__( parts[0] )
			del parts[0]
		except ImportError:
			return None

		try:
			while len( parts ) > 0:
				m = getattr( m, parts[0] )
				del parts[0]
			return m
		except AttributeError:
			pass

		classname = ""
		for mystr in parts:
			classname = "{}{}".format( classname, mystr.capitalize() )

		try:
			m = getattr( m, classname )
		except AttributeError:
			logger.warning( 'Unable to load class {}'.format( classname ) )
			return None

		return m


