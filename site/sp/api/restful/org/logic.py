
from common.views.restfulview import RestfulLogic
from common.models import *


class Index( RestfulLogic ):

	def get_object( self, request, *args, **kwargs ):
		umems = UserMembership.objects.filter( user = request.user )

		newobj_list = []
		for obj in umems:
			org = obj.organization
			org.membership = obj
			newobj_list.append( org )

		return newobj_list
	

class View( RestfulLogic ):

	class Meta:
		allow_update = True
		readonly = ( 'refnum', )
		fields = ( 'trading_name', 'telephone_number', 'fax_number' )

	def get_object( self, request, *args, **kwargs ):
		return Organization.objects.get( pk = self.url_kwargs.oid )


