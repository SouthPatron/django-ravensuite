from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect

from singleobjectview import SingleObjectView
from listview import ListView

from ..models import *

class ClientList( ListView ):
	template_name = 'pages/org/client/index'

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid' ], **kwargs )
		obj_list = Client.objects.filter( organization__refnum = mid.oid )
		return obj_list
	
	def create_object_json( self, request, data, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid' ], **kwargs )

		# TODO: select_for_update()
		sc = OrganizationCounter.objects.get( organization__refnum = mid.oid )
		refnum = sc.client_no
		sc.client_no += 1
		sc.save()

		newclient = Client()
		newclient.organization = Organization.objects.get( refnum = mid.oid )
		newclient.refnum = refnum
		newclient.trading_name = data[ 'trading_name' ]
		newclient.save()

		return redirect( 'org-client-single', oid = mid.oid, cid = refnum )


class ClientSingle( SingleObjectView ):
	template_name = 'pages/org/client/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )
		return get_object_or_404( Client, refnum = mid.cid, organization__refnum = mid.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'org-client-list', oid = ob.organization.refnum )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		obj.trading_name = data.get( 'trading_name', obj.trading_name )
		obj.save()
		return redirect( 'org-client-single', oid = obj.organization.refnum, cid = obj.refnum )


