
from common.views.restfulview import RestfulLogic
from common.models import *


class Index( RestfulLogic ):

	class Meta:
		name_map = { 'refnum' : 'id' }
		exclude = ( 'organization', )

	def get_object( self, request, *args, **kwargs ):
		return Client.objects.filter( organization = self.url_kwargs.oid )
	

class View( RestfulLogic ):

	class Meta:
		allow_update = True
		name_map = { 'refnum' : 'id' }
		readonly = ( 'refnum', )


	def get_object( self, request, *args, **kwargs ):
#		return { 'cpu_usage' : '50%' }
		return Client.objects.get( refnum = self.url_kwargs.cid, organization = self.url_kwargs.oid )

