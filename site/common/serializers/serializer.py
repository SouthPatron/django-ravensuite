
from StringIO import StringIO

from django.utils.encoding import smart_unicode


class Serializer( object ):

	@staticmethod
	def get_enc( enc ):
		if enc == 'json':
			from json_serializer import Serializer as sert
			return sert

		raise RuntimeError( 'Not yet Implemented Serialization Format: {}'.format( enc ) )
	
	@staticmethod
	def serialize( enc, queryset, **kwargs ):
		cl = Serializer.get_enc( enc )
		return cl().serialize( queryset, **kwargs )



