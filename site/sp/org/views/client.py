from django.shortcuts import get_object_or_404

from common.views.pageview import PageView
from common.models import *

class ClientList( PageView ):
	template_name = 'pages/org/client/index'

	def get_object( self, request, *args, **kwargs ):
		return Organization.objects.get( refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		return Client.objects.filter( organization__refnum = self.url_kwargs.oid )

class ClientSingle( PageView ):
	template_name = 'pages/org/client/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Client, refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )


