
from common.views.restfulview import RestForbidden
from common.models import *

from sp.api.views import RestfulLogic


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

	def get_object( self, request, *args, **kwargs ):
		return Organization.objects.get( pk = self.url_kwargs.oid )

