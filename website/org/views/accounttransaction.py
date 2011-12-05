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
		return Account.objects.get( client__organization__refnum = self.url_kwargs.oid, client__refnum = self.url_kwargs.cid )

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )

		obj_list = AccountTransaction.objects.filter( account__client__refnum = mid.cid, account__client__organization__refnum = mid.oid )
		return obj_list


class AccountTransactionSingle( SingleObjectView ):
	template_name = 'pages/org/account_transaction/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'tid' ], **kwargs )
		return get_object_or_404( AccountTransaction, refnum = mid.tid, account__client__refnum = mid.cid, account__client__organization__refnum = mid.oid )




