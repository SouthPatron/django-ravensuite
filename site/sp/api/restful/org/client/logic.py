
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
		return Client.objects.filter( organization = self.kwargs.oid )
	

class View( RestfulLogic ):

	def get_object( self, request, *args, **kwargs ):
		return Client.objects.get( refnum = self.kwargs.cid, organization = self.kwargs.oid )

