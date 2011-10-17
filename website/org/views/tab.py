from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect

from singleobjectview import SingleObjectView
from listview import ListView

from ..models import *

class TabList( ListView ):
	template_name = 'pages/org/tab/index'

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )
		obj_list = Tab.objects.filter( client__refnum = mid.cid, client__organization__refnum = mid.oid )
		return obj_list
	
	def create_object_json( self, request, data, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )

		# TODO: select_for_update()
		sc = SystemCounter.objects.get( id = 1 )
		refnum = sc.account_no
		sc.account_no += 1
		sc.save()

		newacc = Tab()
		newacc.client = Client.objects.get( refnum = mid.cid, organization__refnum = mid.oid )
		newacc.refnum = refnum
		newacc.is_enabled = data.get( 'is_enabled', True )
		newacc.min_balance = data.get( 'min_balance', 0 )
		newacc.name = data[ 'name' ]
		newacc.save()

		return redirect( 'org-client-tab-single', oid = mid.oid, cid = mid.cid, aid = refnum )


class TabSingle( SingleObjectView ):
	template_name = 'pages/org/tab/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid' ], **kwargs )

		return get_object_or_404( Tab, refnum = mid.aid, client__refnum = mid.cid, client__organization__refnum = mid.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'org-client-tab-list', cid = ob.client.refnum, oid = ob.client.organization.refnum )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		obj.name = data.get( 'name', obj.name )
		obj.is_enabled = data.get( 'is_enabled', obj.is_enabled )
		obj.min_balance = data.get( 'min_balance', obj.min_balance )
		obj.save()
		return redirect( 'org-client-tab-single', oid = obj.client.organization.refnum, cid = obj.client.refnum, aid = obj.refnum )



