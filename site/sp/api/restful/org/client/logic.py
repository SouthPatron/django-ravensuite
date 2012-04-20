
from common.views.restfulview import RestfulLogic
from common.models import *


class Index( RestfulLogic ):

	def get_object( self, request, *args, **kwargs ):
		return Client.objects.filter( organization = self.url_kwargs.oid )
	

class View( RestfulLogic ):

	def get_object( self, request, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization = self.url_kwargs.oid )

