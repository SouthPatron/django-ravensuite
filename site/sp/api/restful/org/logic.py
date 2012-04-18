
from common.views.restfulview import RestForbidden
from common.models import *

from sp.api.views import RestfulLogic


class Index( RestfulLogic ):

	def create_object( self, request, data, *args, **kwargs ):
		raise RestForbidden()

	def get_extra( self, request, *args, **kwargs ):
		return None

	def get_object( self, request, *args, **kwargs ):
		return None

	def get_object_list( self, request, *args, **kwargs ):
		umems = UserMembership.objects.filter( user = request.user )

		newobj_list = []
		for obj in umems:
			org = obj.organization
			org.membership = obj
			newobj_list.append( org )

		return newobj_list
	

class View( RestfulLogic ):

	def get_object( self, request, *args, **kwargs ):
		return Organization.objects.get( pk = self.dataset[ 'kwargs' ].oid )

