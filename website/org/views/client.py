from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect

from singleobjectview import SingleObjectView
from listview import ListView

from ..models import *

class ClientList( ListView ):
	template_name = 'pages/org/client/index'

	def get_object_list( self, request, *args, **kwargs ):
		oid = kwargs.get( 'oid', None )
		if oid is None:
			self.not_found()

		obj_list = Client.objects.filter( organization = oid )
		return obj_list
	
	def create_object_json( self, request, data, *args, **kwargs ):
		oid = kwargs.get( 'oid', None )
		if oid is None:
			self.not_found()

		# TODO: select_for_update()
		sc = OrganizationCounter.objects.get( organization = oid )
		refnum = sc.client_no
		sc.client_no += 1
		sc.save()

		newclient = Client()
		newclient.organization = Organization.objects.get( id = oid )
		newclient.refnum = refnum
		newclient.trading_name = data[ 'trading_name' ]
		newclient.save()

		return redirect( 'org-client-single', oid = oid, cid = refnum )


class ClientSingle( SingleObjectView ):
	template_name = 'pages/org/client/single'

	def get_object( self, request, *args, **kwargs ):
		oid = kwargs.get( 'oid', None )
		if oid is None:
			self.not_found()

		cid = kwargs.get( 'cid', None )
		if cid is None:
			self.not_found()

		return get_object_or_404( Client, refnum = cid, organization = oid )



