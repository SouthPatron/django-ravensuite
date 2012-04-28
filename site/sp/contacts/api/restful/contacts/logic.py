
from common.views.restfulview import RestfulLogic
from sp.contacts.models import *


class Index( RestfulLogic ):


	def create_object( self, request, data, *args, **kwargs ):
		obj = Contact()

		obj.trading_name = data.get( 'trading_name', None )
		obj.telephone_number = data.get( 'telephone_number', None )
		obj.fax_number = data.get( 'fax_number', None )
		obj.email_address = data.get( 'email_address', None )
		obj.postal_address = data.get( 'postal_address', None )
		obj.physical_address = data.get( 'physical_address', None )

		return obj;

	def get_object( self, request, *args, **kwargs ):
		return Contact.objects.all()


