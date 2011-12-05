from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.models import *
from common.utils.dbgdatetime import datetime
from common.utils.objroute import ObjRoute


class AccountTransactionList( ListView ):
	template_name = 'pages/org/account_transaction/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Account.objects.get( client__organization__refnum = self.url_kwargs.oid, client__refnum = self.url_kwargs.cid )

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )

		obj_list = AccountTransaction.objects.filter( account__client__refnum = mid.cid, account__client__organization__refnum = mid.oid )
		return obj_list



def account_transaction_router( request, oid, cid, tid ):
	actrans = AccountTransaction.objects.get( refnum = tid, account__client__refnum = cid, account__client__organization__refnum = oid )
	newobj = ObjRoute.get( actrans.originating_route )
	return redirect( newobj.get_single_url() )

