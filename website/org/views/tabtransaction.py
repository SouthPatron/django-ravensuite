from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden

from singleobjectview import SingleObjectView
from listview import ListView

from ..models import *
from ..utils.dbgdatetime import datetime

class TabTransactionList( ListView ):
	template_name = 'pages/org/tab_transaction/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Tab.objects.get( refnum = self.url_kwargs.tabid, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )


	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'tabid' ], **kwargs )

		obj_list = TabTransaction.objects.filter( tab__refnum = mid.tabid, tab__client__refnum = mid.cid, tab__client__organization__refnum = mid.oid )
		return obj_list
	


class TabTransactionSingle( SingleObjectView ):
	template_name = 'pages/org/tab_transaction/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid', 'tid' ], **kwargs )
		return get_object_or_404( TabTransaction, refnum = mid.tid, account__refnum = mid.aid, account__client__refnum = mid.cid, account__client__organization__refnum = mid.oid )


	def update_object_json( self, request, obj, data, *args, **kwargs ):
		if data.has_key( 'amount' ):
			return HttpResponseForbidden()

		obj.group = data.get( 'group', obj.group )
		obj.description = data.get( 'description', obj.description )
		obj.is_grouped = data.get( 'is_grouped', obj.is_grouped )
		obj.save()

		if data.has_key( 'data' ):
			tdata = TabTransactionData.objects.get( transaction = obj )
			tdata.data = data.get( 'data' )
			tdata.save()

		return redirect( 'org-client-tab-transaction-single', oid = obj.account.client.organization.refnum, cid = obj.account.client.refnum, aid = obj.account.refnum, tid = obj.refnum )



