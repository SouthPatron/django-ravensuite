from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.models import *
from common.utils.dbgdatetime import datetime

class AccountTransactionList( ListView ):
	template_name = 'pages/org/account_transaction/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Account.objects.get( client__organization__refnum = self.url_kwargs.oid, client__refnum = self.url_kwargs.cid, refnum = self.url_kwargs.aid )

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid' ], **kwargs )

		obj_list = AccountTransaction.objects.filter( account__refnum = mid.aid, account__client__refnum = mid.cid, account__client__organization__refnum = mid.oid )
		return obj_list


class AccountTransactionSingle( SingleObjectView ):
	template_name = 'pages/org/account_transaction/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid', 'tid' ], **kwargs )
		return get_object_or_404( AccountTransaction, refnum = mid.tid, account__refnum = mid.aid, account__client__refnum = mid.cid, account__client__organization__refnum = mid.oid )


	def update_object_json( self, request, obj, data, *args, **kwargs ):
		if data.has_key( 'amount' ):
			return HttpResponseForbidden()

		obj.group = data.get( 'group', obj.group )
		obj.description = data.get( 'description', obj.description )
		obj.save()

		if data.has_key( 'data' ):
			tdata = AccountTransactionData.objects.get( transaction = obj )
			tdata.data = data.get( 'data' )
			tdata.save()

		return redirect( 'org-client-account-transaction-single', oid = obj.account.client.organization.refnum, cid = obj.account.client.refnum, aid = obj.account.refnum, tid = obj.refnum )



